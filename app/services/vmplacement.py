import subprocess
import re
from datetime import datetime, timedelta

def obtener_valor_flavor(flavor_id, campo):
    # Ejecutar el comando openstack flavor show y obtener el valor específico del campo
    comando = f'openstack flavor show {flavor_id} | grep "| {campo}" | awk -F "|" \'{{print $3}}\' | tr -d \'[:space:]\''
    valor = subprocess.run(comando, capture_output=True, text=True, shell=True).stdout.strip()

    return int(valor) if valor.isdigit() else 0

def calcular_requisitos(instancias_flavors):
    total_ram = 0
    total_disco = 0

    for flavor_id in instancias_flavors:
        # Obtener valores específicos del flavor desde la línea de comandos
        ram = obtener_valor_flavor(flavor_id, 'ram')
        disco = obtener_valor_flavor(flavor_id, 'disk')

        # Sumar RAM y disco
        ram_gb = ram / 1024
        total_ram += ram_gb
        total_disco += disco

    return total_ram, total_disco


def obtener_info_worker(worker):
    # Ejecutar el comando openstack hypervisor show
    comando = f'openstack hypervisor show {worker}'
    salida = subprocess.run(comando, capture_output=True, text=True, shell=True)

    # Extraer información relevante usando expresiones regulares
    local_gb = int(re.search(r'\| local_gb\s*\|\s*(\d+)', salida.stdout).group(1))
    local_gb_used = int(re.search(r'\| local_gb_used\s*\|\s*(\d+)', salida.stdout).group(1))
    free_disk_gb = int(re.search(r'\| disk_available_least\s*\|\s*(-?\d+)', salida.stdout).group(1))
    memory_mb = int(re.search(r'\| memory_mb\s*\|\s*(\d+)', salida.stdout).group(1))
    memory_mb_used = int(re.search(r'\| memory_mb_used\s*\|\s*(\d+)', salida.stdout).group(1))
    free_ram_mb = int(re.search(r'\| free_ram_mb\s*\|\s*(\d+)', salida.stdout).group(1))

    # Convertir de megabytes a gigabytes
    memory_mb = round(memory_mb / 1024, 2)
    memory_mb_used = round(memory_mb_used / 1024, 2)
    free_ram_mb = round(free_ram_mb / 1024, 2)


    return {
        'local_gb': local_gb,
        'local_gb_used': local_gb_used,
        'free_disk_gb': free_disk_gb,
        'memory_mb': memory_mb,
        'memory_mb_used': memory_mb_used,
        'free_ram_mb': free_ram_mb
    }


def consulta_instancia(worker, instancias_flavors):
    lista_workers = ["Worker1", "Worker2", "Worker3"]
    # Obtener información del worker
    info_worker = obtener_info_worker(worker)
    
    # Calcular requisitos de las instancias
    total_ram, total_disco = calcular_requisitos(instancias_flavors)
    
    # Validar si el worker puede soportar las instancias
    if info_worker['free_ram_mb'] >= total_ram and info_worker['free_disk_gb'] >= total_disco:
        print(f"El worker {worker} tiene suficientes recursos para instanciar las instancias.")
        return worker
    else:
        print(f"El worker {worker} no tiene suficientes recursos para instanciar las instancias.")
        print(f"Recursos requeridos: RAM={total_ram} GB, Disco={total_disco} GB")
        print(f"Recursos disponibles: RAM={info_worker['free_ram_mb']} GB, Disco={info_worker['free_disk_gb']} GB")

        # Consultar otros workers
        for otro_worker in lista_workers:
            if otro_worker != worker:
                print(f"Intentando con el worker {otro_worker}...")
                info_otro_worker = obtener_info_worker(otro_worker)
                if info_otro_worker['free_ram_mb'] >= total_ram and info_otro_worker['free_disk_gb'] >= total_disco:
                    print(f"El worker {otro_worker} tiene suficientes recursos para instanciar las instancias.")
                    return otro_worker
                else:
                    print(f"El worker {otro_worker} tampoco tiene suficientes recursos.")
                    print(f"Recursos disponibles: RAM={info_otro_worker['free_ram_mb']} GB, Disco={info_otro_worker['free_disk_gb']} GB")

        # Si ninguno de los workers tiene suficientes recursos, realizar nueva lógica
        print("Ningún worker tiene suficientes recursos para instanciar las instancias.")
        return analizar_logs(lista_workers)

def analizar_logs(lista_workers):
    for worker in lista_workers:
        if(worker == 'Worker1'):
            log_file = f'10.0.0.30_logs.txt'
            if not file_exists(log_file):
                continue
            if analizar_log(log_file):
                return worker
        elif(worker == 'Worker2'):
            log_file = f'10.0.0.40_logs.txt'
            if not file_exists(log_file):
                continue
            if analizar_log(log_file):
                return worker
        elif(worker == 'Worker3'):
            log_file = f'10.0.0.50_logs.txt'
            if not file_exists(log_file):
                continue
            if analizar_log(log_file):
                return worker
        else:
            return None

def file_exists(file_path):
    try:
        with open(file_path):
            return True
    except FileNotFoundError:
        return False

def analizar_log(log_file):
    with open(log_file, 'r') as file:
        lines = file.readlines()

    current_time = datetime.now()
    time_threshold = timedelta(minutes=10)
    cpu_threshold = 70
    memory_threshold = 50

    for line in lines:
        timestamp_str, cpu_str, memory_str = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - CPU: (\d+\.\d+)%\, Memoria: (\d+\.\d+)%', line).groups()
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        cpu = float(cpu_str)
        memory = float(memory_str)

        if current_time - timestamp > time_threshold:
            break

        if cpu > cpu_threshold or memory > memory_threshold:
            return False

    return True

def elegir_zonaDisponibilidad(flavors,worker):
    #flavors_a_crear = ['flavor1','flavor2','flavor3','flavor4','flavor5']
    #worker_final = consulta_instancia('Worker1', flavors_a_crear)
    worker_final = consulta_instancia(worker, flavors)

    if worker_final:
        print(f"Se seleccionó el worker {worker_final} para instanciar las instancias.")
        return worker_final
    else:
        print("No hay workers disponibles con suficientes recursos.")
        return None