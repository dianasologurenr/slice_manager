import json
import time
from dependencies import get_db
from fastapi import APIRouter, Body, Depends, Form, HTTPException
from crud import slice as crud_slice
from crud import user as crud_user
from crud import slice_user as crud_slice_user
from crud import flavor as crud_flavor
from crud import node as crud_node
from crud import port as crud_port
from crud import link as crud_link
from crud import availability_zone as az
from services import funciones as openstack
from services import vmplacement
from config import GATEWAY_IP, ADMIN_PASSWORD, ADMIN_PROJECT_NAME, ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_USERNAME,ADMIN_ID,ADMIN,READER,MEMBER,IP_VERSION, CIDR, IMAGEN_ID



import schemas.schema as schema
from typing import List, Optional

router = APIRouter(
    prefix="/slices",
    tags=["slices"],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=List[schema.Slice])
async def read_slices(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    slices = crud_slice.get_slices(db, skip=skip, limit=limit)
    return slices

@router.get("/{id}",response_model=schema.Slice)
async def read_slice(id: int, db=Depends(get_db)):
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    return db_slice

@router.post("/", response_model=schema.Slice)
async def create_slice(slice: schema.SliceBase, db=Depends(get_db)):
    db_slice = crud_slice.get_slice_by_name(db,name=slice.name)
    if db_slice:
        raise HTTPException(status_code=400, detail="There is already a slice with that name")
    return crud_slice.create_slice(db=db, slice=slice)

@router.post("/deploy/{id}")
async def desplegar_slice(id: int, db=Depends(get_db)):
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    if db_slice.status == "creating":
        raise HTTPException(status_code=400, detail="Slice is being deployed")
    
    # Update slice status
    update_slice = schema.SliceUpdate(status="creating")
    crud_slice.update_slice(db=db,id=id,slice=update_slice)

    try:
    #0.- Validar el espacio (monitoreo) obtener id_az que viene con id_slice y luego nombre 
    ##zona disponibilidad
        db_availability_zone = db_slice.id_az
        if db_availability_zone == 1:
            db_availability_zone = 'Worker1'
        elif db_availability_zone == 2:
            db_availability_zone = 'Worker2'
        elif db_availability_zone == 3:
            db_availability_zone = 'Worker3'
        flavors = crud_flavor.get_flavors_by_id_slice(db,id_slice=id)
        print(flavors)
        print("--------------------")
        print(db_availability_zone)
        tuplas = flavors
        resultado_json = []
        for tupla in tuplas:
            diccionario = {
                "id": tupla[0],
                "cpu": tupla[1],
                "ram": tupla[2],
                "disk": tupla[3]
            }
            resultado_json.append(diccionario)
        print(resultado_json)
        zona_disponibilidad = vmplacement.elegir_zonaDisponibilidad(db_availability_zone,resultado_json)
        
        
        if zona_disponibilidad:
            print(f"La zona disponibilidad es: {zona_disponibilidad} ")

            

            try:

                #1.- Obtener token 
                project_name = db_slice.name
                project_description = "-"
                admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP,ADMIN_PASSWORD,ADMIN_USERNAME,ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_PROJECT_NAME) 
                if admin_token:
                    #2.- Crear el proyecto
                    project = openstack.crearProyecto(GATEWAY_IP, admin_token, DOMAIN_ID, project_name, project_description)
                    if project:
                        project_id = project["project"]["id"]
                        rol = openstack.asignarRol(GATEWAY_IP, admin_token, project_id, ADMIN_ID, ADMIN)
                        #3.- Token del proyecto 
                            #3.1.-Asignar rol admin al usuario admin
                            #3.2.-Crear usuario y asignar rol al usuario (rol reader) --pendiente--
                        if rol:
                            project_token = openstack.obtenerTokenProject(GATEWAY_IP, admin_token, DOMAIN_ID, project_name)
                            if project_token:
                                print(project_token)
                                #4.- Creacion de network (network_name es la id)
                                links = crud_link.get_link_by_slice(db, id_slice=id)
                                links_temp = {}

                                for link in links:

                                    network_name = str(link.id)
                                    network = openstack.crearRed(GATEWAY_IP, project_token, network_name)
                                                                
                                    network_id = network["network"]["id"]
                                    
                                    #5.- Creación de subnet (subnet name es el id)
                                    subnet_name = f"Subnet_{link.id}"
                                    subnet = openstack.crearSubred(GATEWAY_IP, project_token, network_id, subnet_name, IP_VERSION, CIDR)
                                    
                                    
                                    subnet_id = subnet["subnet"]["id"]
                                    
                                    #6.- Creación de puertos
                                    port_name0 = link.port0.name
                                    puerto0 = openstack.crearPuerto(GATEWAY_IP, project_token, port_name0, 
                                    network_id, project_id)
                                    
                                    puerto0_id = puerto0["port"]["id"]
                                    
                                    port_name1 = link.port1.name
                                    puerto1 = openstack.crearPuerto(GATEWAY_IP, project_token, port_name1, network_id, project_id)
                                    
                                    puerto1_id = puerto1["port"]["id"]

                                    links_temp[link.id] = {
                                        "network": network_id,
                                        "subnet": subnet_id,
                                        "puerto0": puerto0_id,
                                        "puerto1": puerto1_id
                                    }
                                #7.- Crear las instancias
                                    #7.1 Crear Flavors
                                
                                flavors = crud_flavor.get_flavors_by_id_slice_distinct(db, id_slice=id)
                                for flavor in flavors:
                                    name = f"Flavor_{flavor.id}"
                                    ram = flavor.ram
                                    vcpus = flavor.core
                                    disk = flavor.disk

                                    flavor_os = openstack.crearFlavor(GATEWAY_IP, project_token, name, int(ram), vcpus, int(disk), flavor.id)
                                    
                                nodes = crud_node.get_nodes_by_slice(db, slice_id=id)

                                for node in nodes:
                                    instance_name = node.name
                                    flavor_id = node.flavor.id
                                    networks = []
                                    for port in node.ports:
                                        link = crud_link.get_link_by_port0(db, id_port=port.id)
                                        if link is None:
                                            link = crud_link.get_link_by_port1(db, id_port=port.id)
                                            port = links_temp[link.id]["puerto1"]
                                        else:
                                            port = links_temp[link.id]["puerto0"]
                                            
                                        networks.append({"port": port})
                                    
                                    node0 = openstack.crearInstancia(GATEWAY_IP, project_token, instance_name, flavor_id, IMAGEN_ID, networks,zona_disponibilidad)
                                    time.sleep(10)
                                    print(node0["server"])
                                    
            except Exception as e:
                print(e)
                # Update slice status
                update_slice = schema.SliceUpdate(status="failed")
                crud_slice.update_slice(db=db,id=id,slice=update_slice)
                return {"message": "Slice deployment failed"}
            else:
                update_slice = schema.SliceUpdate(status="running")
                crud_slice.update_slice(db=db,id=id,slice=update_slice)
                return {"message": "Slice deployed successfully"}
        else:
            print('No se cuentan con los recursos suficientes para desplegar la topología.')
            update_slice = schema.SliceUpdate(status="not_deployed")
            crud_slice.update_slice(db=db,id=id,slice=update_slice)
            return {"message": "Slice deployment failed"}
            
    except Exception as e:
        print(e)
        # Update slice status
        update_slice = schema.SliceUpdate(status="not_deployed")
        crud_slice.update_slice(db=db,id=id,slice=update_slice)
        return {"message": "No se cuenta con los recursos suficientes para desplegar la topología."}
# Update slice
@router.patch("/{id}", response_model=schema.Slice)
async def update_slice(id: int, 
                 topology: Optional[str] = Form(None),
                 status: Optional[str] = Form(None),
                 id_az: Optional[str] = Form(None),
                 nodes: Optional[str] = Form(None),
                 links: Optional[str] = Form(None),
                 db=Depends(get_db)):
    db_slice = crud_slice.get_slice(db=db, slice_id=id)
    
    if not db_slice:
        raise HTTPException(status_code=404, detail="Image not found")
    
    update_slice = schema.SliceUpdate()

    if topology:
        update_slice.topology = topology
    if status:
        update_slice.status = status
    if id_az:
        update_slice.id_az = id_az
    if nodes:
        list_nodes = eval(nodes)

        for node in list_nodes:
            vm_input = schema.NodeBase(
                name=node,
                id_slice=id
            )
            response = crud_node.create_node(db=db, node=vm_input)

        db_nodes = crud_node.get_nodes_by_slice(db=db, slice_id=id)  

        if links:
            list_links = eval(links)
            # create ports and links
            ports = []
            for edge in list_links:
                for port in edge:
                    ports.append(port)
            
            for vm in db_nodes:
                for i in range(ports.count(vm.name)):
                    port_input = schema.PortBase(
                        name=f"port_{i}",
                        id_node= vm.id
                    )
                    response = crud_port.create_port(db=db, port=port_input)
            

            for edge in list_links:
                node1 = crud_node.get_node_by_name_in_slice(db=db, name=edge[0], id_slice=id)
                node2 = crud_node.get_node_by_name_in_slice(db=db, name=edge[1], id_slice=id)
                
                port0 = next((port.id for port in node1.ports if crud_link.get_link_by_port(db=db, id_port=port.id) is None), None)
                port1 = next((port.id for port in node2.ports if crud_link.get_link_by_port(db=db, id_port=port.id) is None), None)

                if port0 and port1:
                    link_input = schema.LinkBase(id_port0=port0, id_port1=port1)
                    response = crud_link.create_link(db=db, link=link_input)
    
    return crud_slice.update_slice(db=db,id=id,slice=update_slice)

@router.delete("/{id}")
async def delete_slice(id: str,db=Depends(get_db)):
    deleted = True
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    if db_slice.status == "creating":
        raise HTTPException(status_code=400, detail="Slice is being deployed")
    if db_slice.status == "running":
        print("Eliminando slice")
        # update slice status
        update_slice = schema.SliceUpdate(status="stopped")
        crud_slice.update_slice(db=db,id=id,slice=update_slice)     

        deleted = False
        project_name = db_slice.name
   
        try:
            # Auth
            admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP,ADMIN_PASSWORD,ADMIN_USERNAME,ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_PROJECT_NAME)
            project_token = openstack.obtenerTokenProject(GATEWAY_IP, admin_token, DOMAIN_ID, project_name)
            
            # Obtener id de proyecto
            project_id = openstack.obtenerIdProyecto(GATEWAY_IP, project_token, project_name)

            servers = openstack.obtenerInstancias(GATEWAY_IP, project_token)
            if servers:
                for server in servers["servers"]:
                    print(f"this is the server: {server}")
                    deleted_server = openstack.eliminarInstancia(GATEWAY_IP,project_token,server["id"])
            
            flavors = crud_flavor.get_flavors_by_id_slice_distinct(db, id_slice=id)
            if flavors:
                for flavor in flavors:
                    deleted_flavor = openstack.eliminarFlavor(GATEWAY_IP, project_token, flavor.id)

            ports = openstack.obtenerPuertos(GATEWAY_IP, project_token)
            if ports:
                for port in ports["ports"]:
                    print(f"this is the port: {port['name']}")
                    deleted_port = openstack.eliminarPuerto(GATEWAY_IP, project_token, port["id"])  

            subnets = openstack.obtenerSubredes(GATEWAY_IP, project_token)
            if subnets:
                for subnet in subnets["subnets"]:
                    print(f"this is the subnet: {subnet['name']}")
                    deleted_subnet = openstack.eliminarSubred(GATEWAY_IP, project_token, subnet["id"])

            network = openstack.obtenerRedes(GATEWAY_IP, project_token)
            if network:
                for net in network["networks"]:
                    print(f"this is the network: {net['name']}")
                    deleted_network = openstack.eliminarRed(GATEWAY_IP, project_token, net["id"])
            
            # Unassign role to admin
            permiso_admi = openstack.desasignarRol(GATEWAY_IP, admin_token, project_id, ADMIN_ID, ADMIN)
            
            # Unassign role to users
            # users = openstack.obtenerUsuarios(GATEWAY_IP, project_token)
            # for user in users["users"]:
            #     print(f"this is the user: {user['name']}")
            #     permisos = openstack.desasignarRol(GATEWAY_IP, project_token, user["id"], project_id, READER)
            
            if permiso_admi:
            
                deleted_project=openstack.eliminarProyecto(GATEWAY_IP, admin_token, project_id)
                time.sleep(5)
                if deleted_project:
                    # Delete slice
                    deleted = True
                else:
                    print("No se pudo eliminar el slice")
                    return {"message": "No se pudo eliminar el slice"}
        except Exception as e:
            print(e)
            return {"message": "No se pudo eliminar el slice"}

    if deleted:
        print("Eliminando slice de la base de datos...")
        # Delete links
        links = crud_link.get_link_by_slice(db, id_slice=id)

        for link in links:
            if link:
                crud_link.delete_link(db=db, id=link.id)
        # Delete ports
        nodes = crud_node.get_nodes_by_slice(db, slice_id=id)
        # Delete flavors
        flavor = crud_flavor.get_flavors_by_id_slice_distinct(db, id_slice=id)
        for flavor in flavor:
            if flavor:
                crud_flavor.delete_flavor(db=db, flavor_id=flavor.id)
        
        for node in nodes:
            # Delete ports
            if node:
                ports = node.ports
                if ports != []:
                    for port in ports:
                        crud_port.delete_port(db=db, id=port.id)
                    # Delete node
                crud_node.delete_node(db=db, node_id=node.id)

        users = db_slice.users
        if users != []:
            for user in users:
                # Delete slice_user
                if user:
                    slice_user = schema.SliceUserBase(
                        id_slice=db_slice.id,
                        id_user=user.id
                    )
                    crud_slice_user.delete_slice_user(db=db, slice_user=slice_user)

                    #Delete user
                    crud_user.delete_user(db=db, user_id=user.id)
        
        # Delete slice
        return crud_slice.delete_slice(db=db, slice_id=db_slice.id)

@router.post("/users/", response_model=schema.SliceUser)
async def create_slice_user(slice_user: schema.SliceUserBase, db=Depends(get_db)):
    db_slice_user = crud_slice_user.get_slice_user(db=db, slice_user=slice_user)
    if db_slice_user:
        raise HTTPException(status_code=400, detail="There user is already assigned to this slice")
    return crud_slice_user.create_slice_user(db=db, slice_user=slice_user)

@router.delete("/users/")
async def delete_slice(slice_user: schema.SliceUserBase,db=Depends(get_db)):
    db_slice_user = crud_slice_user.get_slice_user(db=db, slice_user=slice_user)
    if db_slice_user is None:
        raise HTTPException(status_code=404, detail="User not found in slice")
    return crud_slice_user.delete_slice_user(db=db, slice_user=slice_user)

@router.get("/links/{id_slice}",response_model=List[schema.Link])
async def read_links_by_slice(id_slice: int, db=Depends(get_db)):
    db_links = crud_link.get_link_by_slice(db, id_slice=id_slice)
    
    return db_links