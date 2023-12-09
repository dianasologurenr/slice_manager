from openstack_sdk import password_authentication_with_scoped_authorization
from openstack_sdk import token_authentication_with_scoped_authorization
from openstack_sdk import create_network
import json

def obtenerTokenAdmin(gateway_ip, admin_password, admin_username, admin_domain_name, domain_id, admin_project_name):
    keystone_endpoint = f'http://{gateway_ip}:5000/v3'

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
        resp1 = token_authentication_with_scoped_authorization(
            keystone_endpoint,
            admin_token, 
            domain_id,
            admin_project_name)
        if resp1.status_code == 201:
            token_for_project = resp1.headers['X-Subject-Token']
            print(f'Token del proyecto: {token_for_project}')
            return token_for_project
        else:
            print('FAILED AUTHENTICATION FOR PROJECT ')
            return None
    else:
        print('La autenticación del administrador ha fallado')
        return None
    
def crearRed(gateway_ip, token_for_project, network_name):
    neutron_endpoint = f'http://{gateway_ip}:9696/v2.0'  # Se ha corregido el endpoint
    resp3 = create_network(neutron_endpoint, token_for_project, network_name)
    if resp3.status_code == 201:
        print('NETWORK CREATED SUCCESSFULLY')
        network_created = resp3.json()
        print(json.dumps(network_created))
    else:
        print('FAILED NETWORK CREATION')
        return None
    


def main():
    # Input para los datos necesarios
    gateway_ip = '10.20.10.114'
    admin_password = 'f2d47da4670dc4fb30e1e6e1eed8bb7e'
    admin_username = 'admin'
    admin_domain_name = 'Default'
    domain_id = 'default'
    admin_project_name = 'admin'
    network_name = 'Enlace 1'

    # Obtener el token del administrador
    project_token = obtenerTokenAdmin(
        gateway_ip,
        admin_password,
        admin_username,
        admin_domain_name,
        domain_id,
        admin_project_name
    ) 
    if project_token:
        # Crear la red con el token del proyecto
        crearRed(gateway_ip, project_token, network_name)
        # Puedes realizar operaciones adicionales aquí utilizando el token de administrador
        print('Operaciones adicionales realizadas exitosamente.')
    else:
        print('La autenticación del administrador ha fallado. No se pudo obtener el token.')

if __name__ == "__main__":
    main()
