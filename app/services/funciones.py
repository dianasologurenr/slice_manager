from services.openstack_sdk import *


from config import GATEWAY_IP, ADMIN_PASSWORD, ADMIN_PROJECT_NAME, ADMIN_DOMAIN_NAME,DOMAIN_ID,ADMIN_USERNAME
import json

def obtenerTokenAdmin(gateway_ip, admin_password, admin_username, admin_domain_name, domain_id, admin_project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    try:
        resp = password_authentication_with_scoped_authorization(
            keystone_endpoint,
            admin_domain_name,
            admin_username,
            admin_password,
            domain_id,
            admin_project_name
        )

        if resp.status_code == 201:
            admin_token = resp.headers['X-Subject-Token']
            print(f'Token de administrador: {admin_token}')
            return admin_token
        else:
            print('La autenticación del administrador ha fallado')
            return None
    except:
        return None
    
def obtenerTokenProject(gateway_ip, admin_token, domain_id, project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'

    try: 
        resp1 = token_authentication_with_scoped_authorization(
                keystone_endpoint,
                admin_token, 
                domain_id,
                project_name
        )
        if resp1.status_code == 201:
            token_for_project = resp1.headers['X-Subject-Token']
            print(f'Token del proyecto: {token_for_project}')
            return token_for_project
        else:
            print('FAILED AUTHENTICATION FOR PROJECT ')
            return None
    except:
        return None
    
def crearRed(gateway_ip, token_for_project, network_name):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0' 
    try:
        resp3 = create_network(neutron_endpoint, token_for_project, network_name)
        if resp3.status_code == 201:
            print('NETWORK CREATED SUCCESSFULLY')
            network_created = resp3.json()
            print(json.dumps(network_created))
            return network_created
        else:
            print('FAILED NETWORK CREATION')
            return None
    except:
        return None
    
def crearSubred(gateway_ip, token_for_project, network_id, subnet_name, ip_version, cidr):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0' 
    try:
        resp = create_subnet(neutron_endpoint, token_for_project, network_id, subnet_name, ip_version, cidr)
        if resp.status_code == 201:
            print('SUBNET CREATED SUCCESSFULLY')
            subnet_created = resp.json()
            print(json.dumps(subnet_created))
            return subnet_created
        else:
            print('FAILED SUBNET CREATION')
            return None
    except:
        return None

def crearPuerto(gateway_ip, token_for_project, port_name, network_id, project_id):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0' 
    try:
        resp = create_port(neutron_endpoint, token_for_project, port_name, network_id, project_id)
        if resp.status_code == 201:
            print('PORT CREATED SUCCESSFULLY')
            port_created = resp.json()
            print(json.dumps(port_created))
            return port_created
        else:
            print('FAILED PORT CREATION')
            return None
    except:
        return None
    
def crearInstancia(gateway_ip, token_for_project, instance_name, flavor_id, image_id, networks,zona_disponibilidad):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1' 
    #availability_zone = 'nova:Worker1'
    availability_zone = 'nova:'+''+zona_disponibilidad
    resp = create_instance(nova_endpoint, token_for_project, instance_name, flavor_id, image_id, networks,availability_zone)
    print(resp.status_code)
    if resp.status_code == 202:
        print('INSTANCE CREATED SUCCESSFULLY')
        instance_created = resp.json()
        print(json.dumps(instance_created))
        return instance_created
    else:
        print('FAILED INSTANCE CREATION')
        return None

def obtenerInstancias(gateway_ip, token_for_project):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1' 
    try:
        resp = get_instances(nova_endpoint, token_for_project)
        print(resp.status_code)
        if resp.status_code == 200:
            print('INSTANCES OBTAINED SUCCESSFULLY')
            instances = resp.json()
            print(json.dumps(instances))
            return instances
        else:
            print('FAILED INSTANCES OBTAINMENT')
            return None
    except:
        return None

def eliminarInstancia(gateway_ip, token_for_project, instance_id):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1' 
    try:
        resp = delete_instance(nova_endpoint, token_for_project, instance_id)
        print(resp.status_code)
        if resp.status_code == 204:
            print('INSTANCE DELETED SUCCESSFULLY')
            return True
        else:
            print('FAILED INSTANCE DELETION')
            return None
    except:
        return None

def crearProyecto(gateway_ip, token_for_project, domain_id, project_name, project_description):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    try:
        resp = create_project(keystone_endpoint, token_for_project, domain_id, project_name, project_description)
        print(resp.status_code)
        if resp.status_code == 201:
            print('PROJECT CREATED SUCCESSFULLY')
            project_created = resp.json()
            print(json.dumps(project_created))
            return project_created
        else:
            print('FAILED PROJECT CREATION')
            return None
    except:
        return None

def obtenerProyecto(gateway_ip, token_for_project, project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    try:
        resp = get_projects(keystone_endpoint, token_for_project)
        print(resp.status_code)
        if resp.status_code == 200:
            print('PROJECTS OBTAINED SUCCESSFULLY')
            projects = resp.json()
            print(json.dumps(projects))
            for project in projects:
                if project['name'] == project_name:
                    print("ID del Proyecto:", project['id'])
                    return project['id']
            print('PROJECT NOT FOUND')
            return None
        else:
            print('FAILED PROJECTS OBTAINMENT')
            return None
    except:
        return None

def asignarRol(gateway_ip, admin_token, project_id, user_id, role_id):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'
    try:
        resp = assign_role_to_user(keystone_endpoint, admin_token, project_id, user_id, role_id)
        print(resp.status_code)
        if resp.status_code == 204:
            print('ROL ASIGNADO SUCCESSFULLY')
            return True
        else:
            print('ROL NO ASIGNADO')
            return None
    except:
        return None
    
def crearFlavor(gateway_ip, token_for_project, name, ram, vcpus, disk, flavor_id):
    nova_endpoint = f'http://{gateway_ip}:8774/v2.1' 
    try:
        resp = create_flavor(nova_endpoint, token_for_project, name, ram, vcpus, disk, flavor_id)
        print(resp.status_code)
        if resp.status_code == 200:
            print('INSTANCE CREATED SUCCESSFULLY')
            flavor_created = resp.json()
            print(json.dumps(flavor_created))
            return flavor_created
        else:
            print('FAILED INSTANCE CREATION')
            return None
    except:
        return None
    


def main():
    #Datos que no se cambian
    gateway_ip = GATEWAY_IP
    admin_password = ADMIN_PASSWORD
    admin_domain_name = ADMIN_DOMAIN_NAME
    domain_id = DOMAIN_ID
    admin_project_name = ADMIN_PROJECT_NAME
    admin_username = ADMIN_USERNAME

    #Datos que deben cambiarse de acuerdo a lo que ingresa el usuario 
    network_name = 'Enlace 1'
    subnet_name = 'Subred del Enlace 1'
    ip_version = '4' 
    cidr = '10.0.39.96/28'
    network_id = '4af63c6b-a719-401d-b8ee-429f320ba1b0'
    port_name = 'Enlace 1'
    project_id = 'c0ee6cd0d5f94c808eb8b5a8813963aa'
    instance_1_name = 'instance 1'
    instance_1_flavor_id = '5c199260-3938-4b8a-94e8-9282e915b508'
    instance_1_image_id = '48d109e3-e4ab-422b-99fa-04a0b70cea7e'
    instance_1_networks = [{"port": "dfe4c979-297c-4f74-a069-d72201a0db04"}]

    instance_2_name = 'instance 2'
    instance_2_flavor_id = '5c199260-3938-4b8a-94e8-9282e915b508'
    instance_2_image_id = '48d109e3-e4ab-422b-99fa-04a0b70cea7e'
    instance_2_networks = [{"port": "dfe4c979-297c-4f74-a069-d72201a0db04"}]


    # Obtener el token del administrador
    project_token = obtenerTokenAdmin(gateway_ip,admin_password,admin_username,admin_domain_name,domain_id,admin_project_name) 
    if project_token:
        # Crear la red con el token del proyecto
        crearRed(gateway_ip, project_token, network_name)
        crearSubred(gateway_ip, project_token, network_id, subnet_name, ip_version, cidr)
        crearPuerto(gateway_ip, project_token, port_name, network_id, project_id)
        crearInstancia(gateway_ip, project_token, instance_1_name, instance_1_flavor_id, instance_1_image_id, instance_1_networks)
        crearInstancia(gateway_ip, project_token, instance_2_name, instance_2_flavor_id, instance_2_image_id, instance_2_networks)


        # Puedes realizar operaciones adicionales aquí utilizando el token de administrador
        print('Operaciones adicionales realizadas exitosamente.')
    else:
        print('La autenticación del administrador ha fallado. No se pudo obtener el token.')

# if __name__ == "__main__":
#     main()
