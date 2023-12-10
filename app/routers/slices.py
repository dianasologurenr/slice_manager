import json
from dependencies import get_db
from fastapi import APIRouter, Body, Depends, Form, HTTPException
from crud import slice as crud_slice
from crud import user as crud_user
from crud import slice_user as crud_slice_user
from crud import node as crud_node
from crud import port as crud_port
from crud import link as crud_link
from services import funciones as openstack
from config import GATEWAY_IP, ADMIN_PASSWORD, ADMIN_PROJECT_NAME, ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_USERNAME,ADMIN_ID,ADMIN,READER,MEMBER,IP_VERSION, CIDR



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
    print("desplegado")

#0.- Validar el espacio (monitoreo) obtener id_az que viene con id_slice y luego nombre 
#1.- Obtener token 
    project_name = db_slice.name
    project_description = "-"
    admin_token = openstack.obtenerTokenAdmin(GATEWAY_IP,ADMIN_PASSWORD,ADMIN_USERNAME,ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_PROJECT_NAME) 
    if admin_token:
        #2.- Crear el proyecto

        project = openstack.crearProyecto(GATEWAY_IP, admin_token, DOMAIN_ID, project_name, project_description)
        project_id = project["project"]["id"]
        openstack.asignarRol(GATEWAY_IP, admin_token, project_id, ADMIN_ID, ADMIN)
        #3.- Token del proyecto 
            #3.1.-Asignar rol admin al usuario admin
            #3.2.-Crear usuario y asignar rol al usuario (rol reader) --pendiente--
        project_token = openstack.obtenerTokenProject(GATEWAY_IP, admin_token, DOMAIN_ID, project_name)
        print(project_token)
        #4.- Creacion de network (network_name es la id)
        links = crud_link.get_link_by_slice(db, id_slice=id)
        links_temp = {}

        for link in links:

            network_name = link.id
            network = openstack.crearRed(GATEWAY_IP, project_token, network_name)
            network_id = network["network"]["id"]
            #5.- Creación de subnet (subnet name es el id)
            subnet_name = f"Subnet_{link}"
            subnet = openstack.crearSubred(GATEWAY_IP, project_token, network_id, subnet_name, IP_VERSION, CIDR)
            subnet_id = subnet["subnet"]["id"]
            #6.- Creación de puertos
            port_name0 = link.port0.name
            puerto0 = openstack.crearPuerto(GATEWAY_IP, project_token, port_name0, network_id, project_id)
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

        nodes = crud_node.get_nodes_by_slice(db, slice_id=id)
        nodes_temp = {}

        for node in nodes:

            


        

        return {}
    else:
        print('No se pudo obtener el token.')
    return{}


#8.- En otra funcion: Eliminar Slices




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
    db_slice = crud_slice.get_slice(db, slice_id=id)
    if db_slice is None:
        raise HTTPException(status_code=404, detail="Slice not found")
    return crud_slice.delete_slice(db=db, slice_id=id)

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
