import paramiko
#from prettytable import PrettyTable

def get_ssh_connection(hostname, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    return client

def get_remote_data(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode('utf-8')

def get_memory_info(ssh_client):
    meminfo = get_remote_data(ssh_client, "cat /proc/meminfo")
    # Buscar la línea que contiene "MemAvailable"
    mem_available_line = next(line for line in meminfo.split('\n') if "MemAvailable" in line)
    _, value_kB, _ = mem_available_line.split()
    # Convertir el valor a gigabytes
    value_GB = round(int(value_kB) / (1024 * 1024), 2)
    return f"{value_GB} GB"

def get_memory_total(ssh_client):
    meminfo = get_remote_data(ssh_client, "cat /proc/meminfo")
    # Obtener la información sobre la memoria total
    mem_total_line = next(line for line in meminfo.split('\n') if "MemTotal" in line)
    _, total_kB, _ = mem_total_line.split()
    # Convertir el valor a gigabytes
    total_GB = round(int(total_kB) / (1024 * 1024), 2)
    return f"{total_GB} GB"

def get_memory_usage(ssh_client):
    meminfo = get_remote_data(ssh_client, "cat /proc/meminfo")
    # Obtener la información sobre la memoria total
    mem_total_line = next(line for line in meminfo.split('\n') if "MemTotal" in line)
    _, total_kB, _ = mem_total_line.split()
    # Convertir el valor a gigabytes
    total_GB = round(int(total_kB) / (1024 * 1024), 2)

    meminfo = get_remote_data(ssh_client, "cat /proc/meminfo")
    # Buscar la línea que contiene "MemAvailable"
    mem_available_line = next(line for line in meminfo.split('\n') if "MemAvailable" in line)
    _, value_kB, _ = mem_available_line.split()
    # Convertir el valor a gigabytes
    value_GB = round(int(value_kB) / (1024 * 1024), 2)

    used =total_GB-value_GB
    usage_percentage = (used / total_GB) * 100
    return f"{usage_percentage:.2f}%"


def get_cpu_info(ssh_client):
    cpuinfo = get_remote_data(ssh_client, "nproc")
    return cpuinfo

def main():
    # Configuración de las máquinas virtuales
    vms = [
        {"ip": "10.0.0.30", "username": "ubuntu", "password": "ubuntu"},
        {"ip": "10.0.0.40", "username": "ubuntu", "password": "ubuntu"},
        {"ip": "10.0.0.50", "username": "ubuntu", "password": "ubuntu"},
    ]

    # Lista para almacenar los resultados
    results = []

    # Conexión y obtención de datos de cada máquina virtual
    for vm in vms:
        try:
            ssh_client = get_ssh_connection(vm["ip"], vm["username"], vm["password"])

            memory_avail = get_memory_info(ssh_client)
            memory_total = get_memory_total(ssh_client)
            memory_usage = get_memory_usage(ssh_client)
            cpu_info = get_cpu_info(ssh_client)

            # Almacenar resultados en la lista
            result = {
                "worker": vm["ip"],
                "memory_avail": memory_avail,
                "memory_total": memory_total,
                "memory_usage": memory_usage,
                "cpu_info": cpu_info
            }

            results.append(result)

        except Exception as e:
            print(f"Error connecting to {vm['ip']}: {str(e)}")

        finally:
            ssh_client.close()

    return results

if __name__ == "__main__":
    results = main()