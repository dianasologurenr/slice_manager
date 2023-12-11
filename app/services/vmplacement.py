import paramiko
import json
from datetime import datetime

def restar_ram_from_memory(memory_avail_GB, flavor_ram_MB):
    # Restar la RAM del flavor a la Memory Avail
    new_memory_avail_GB = memory_avail_GB - (flavor_ram_MB / 1000)
    return max(new_memory_avail_GB, 0)  # Asegurar que el resultado sea al menos 0

def obtener_worker_elegido(worker, dataTotal):
    for entry in dataTotal:
        if worker == "Worker1":
            if entry.get("VM IP") == f"10.0.0.30":
                return [entry]
            break
        if worker == "Worker2":
            if entry.get("VM IP") == f"10.0.0.40":
                return [entry]
            break
        if worker == "Worker3":
            if entry.get("VM IP") == f"10.0.0.50":
                return [entry]
            break
    return None

def ejecutar_script_remoto(worker, datosflavor):
    # Configurar la conexión SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Información de la máquina remota
    remote_host = '10.20.10.114'
    remote_port = 5800
    remote_user = 'ubuntu'
    remote_password = 'ubuntu'

    worker_resultante = worker

    try:
        # Conectar al servidor remoto
        ssh.connect(remote_host, port=remote_port, username=remote_user, password=remote_password)

        # Ejecutar el script remoto
        comando = 'python3 monitoreo.py'
        stdin, stdout, stderr = ssh.exec_command(comando)

        # Imprimir la salida del script remoto
        print("Salida del script remoto:")
        dataTotal = json.loads(stdout.read().decode('utf-8'))
        print(json.dumps(dataTotal, indent=3))

        # Obtener el json del worker elegido
        worker_data = obtener_worker_elegido(worker, dataTotal)

        if worker_data:
            # Extraer el valor de Memory Avail en GB
            first_entry = worker_data[0]
            memory_avail_GB = float(first_entry["Memory Avail"].rstrip(" GB"))

            # Restar la RAM de cada flavor
            for flavor in datosflavor:
                memory_avail_GB = restar_ram_from_memory(memory_avail_GB, flavor["ram"])
            print(f'---------------------------------------------------------------')
            print(f'Nueva memoria es {memory_avail_GB}')
            # Verificar si el Memory Avail es menor a 1
            if memory_avail_GB < 1:
                # Intentar con otros workers
                print("La Memory Avail es menor a 1. Intentando con otros workers.")

                # Lista de workers que no han sido elegidos
                otros_workers = ["Worker2", "Worker3"] if worker == "Worker1" else ["Worker1", "Worker3"] if worker == "Worker2" else ["Worker1", "Worker2"]
                
                for otro_worker in otros_workers:
                    print(f"Probando con {otro_worker}")
                    # Obtener el json del otro worker
                    worker_data_otro = obtener_worker_elegido(otro_worker, dataTotal)

                    if worker_data_otro:
                        # Extraer el valor de Memory Avail en GB
                        first_entry_otro = worker_data_otro[0]
                        memory_avail_GB_otro = float(first_entry_otro["Memory Avail"].rstrip(" GB"))

                        # Restar la RAM de cada flavor
                        for flavor in datosflavor:
                            memory_avail_GB_otro = restar_ram_from_memory(memory_avail_GB_otro, flavor["ram"])

                        print(f'---------------------------------------------------------------')
                        print(f'Nueva memoria para {otro_worker} es {memory_avail_GB_otro}')

                        # Verificar si el Memory Avail es mayor o igual a 1
                        if memory_avail_GB_otro >= 1:
                            worker_resultante = otro_worker
                            break  # Salir del bucle si encontramos un worker que cumple
                
                print(f"El worker resultante luego del bucle es {worker_resultante}")
                
                if worker_resultante == worker:
                    print("El worker resultante luego del bucle es el mismo que el original.")
                    #continuar la lógica del código
                    for otro_worker in ["Worker1", "Worker2", "Worker3"]:
                        print(f"Verificando logs de {otro_worker}")
                        logs_comando = f'cat {otro_worker}_logs.txt'
                        stdin_logs, stdout_logs, stderr_logs = ssh.exec_command(logs_comando)

                        # Analizar los registros de logs
                        logs = stdout_logs.read().decode('utf-8').splitlines()
                        for log in logs:
                            try:
                                timestamp_str, rest_of_the_line = log.split(" - ", 1)  # Solo se divide en el primer '-'
                                cpu_str, memoria_str = rest_of_the_line.split(", ")
                                timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                                cpu = float(cpu_str.split(":")[1].strip('%'))
                                memoria = float(memoria_str.split(":")[1].strip('%'))

                                # Verificar si se superan los umbrales
                                if cpu > 70 or memoria > 60:
                                    break  # Si se supera, salir del bucle
                            except ValueError:
                                # Ignorar líneas que no tienen el formato esperado
                                continue
                        else:
                            # Si el bucle no se rompe, no se superaron los umbrales
                            worker_resultante = otro_worker
                            print(f"Se seleccionó el Worker {worker_resultante} debido a los registros de logs.")
                            break
                    
            else:
                # Si el Memory Avail es mayor o igual a 1, no es necesario probar con otros workers
                worker_resultante = worker

    finally:
        # Cerrar la conexión SSH después de su uso
        ssh.close()

    return worker_resultante


def elegir_zonaDisponibilidad(worker,flavors):
    worker = ejecutar_script_remoto(worker,flavors)
    return worker