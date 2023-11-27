#!/usr/bin/env python3
from subprocess import call, run
from lib_mv import MV,Red
import logging, sys, json
from os import path
from control_file import control_search,control_state,control_change_state,control_add,control_rm,monitor
import time

# #########################################################################
# Creación control_file
# #########################################################################
reset_file = False
if path.exists("control_file") == False:
    reset_file = True
else:
    with open ('control_file','r') as archivo:
        n_lines = len(archivo.readlines())
    if n_lines < 5:
        reset_file = True
          

if reset_file == True:
    with open ('control_file','w') as archivo:
        archivo.write("#### RED #### 0 -> no lan; 1 -> hay LAN\n")
        archivo.write("\tLAN\t0\n")
        archivo.write("\n#### MAQUINAS VIRTUALES #### 0 -> parada; 1 -> arrancada\n\n")  
    n_lines = 4
# #########################################################################
# #########################################################################



#########################################################################
#########################################################################
# Main
#########################################################################
#########################################################################

# Cargar JSON
with open('auto_p2.json', 'r') as f:
    data = json.load(f)

num_server = data['num_server']
debug = data['debug']

if len(sys.argv) < 2:
    logging.warning("No se proporcionó el segundo argumento.")
    sys.exit(1)

# Creacion y configuracion del logger
def init_log():
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

init_log()


# #########################################################################
# Argumentos
# #########################################################################
if len(sys.argv) < 2 or sys.argv[1] == '--help':
    print("""
    Uso: auto_p2.py [opcion] mv1 mv2 ... mvx

    Opcion:
        crear: Crea una nueva máquina virtual o red.
        arrancar: Inicia una máquina virtual o red existente.
        parar: Detiene una máquina virtual o red existente.
        liberar: Libera una máquina virtual o red existente.
        consola: Muestra la consola de una máquina virtual existente.
        monitor: Inicia el monitor de todas las máquinas virtuales.
        monitor_mv: Inicia el monitor de cada máquina virtual

    Argumento 2...N:
        mv1 mv2 ... mvx: Nombre de la máquina virtual o red a crear, arrancar, parar, liberar o mostrar la consola.
        Si no pones nada hará el proceso de operación con todas las máquinas virtuales especificadas en el fichero auto_p2.json
    
    """)
    sys.exit(0)


second_arg = sys.argv[1]

next_arg = []

all_vm = ["c1","lb"]
for i in range(num_server):
    all_vm.append("s" + str(i+1)) 

i=2
if num_server <= 5:
    if len(sys.argv) > 2:
        while i < len(sys.argv) and sys.argv[i] != " ":
            # logging.warning(sys.argv[i][1:].isdigit())
            if sys.argv[i] != "lb" and sys.argv[i] != "c1" and not(sys.argv[i].startswith("s") and sys.argv[i][1:].isdigit() and int(sys.argv[i][1:]) <= num_server):
                logging.warning(f"maquina {sys.argv[i]} no permitida")                
            else:
                next_arg.append(sys.argv[i])
            i = i + 1
    else:
        next_arg = all_vm
else:
    print("")
    logging.error("No se puede crear mas de 5 servidores")
    print("")
# #########################################################################
# Aplicacion
# #########################################################################

if second_arg == 'crear':
    imagen = "cdps-vm-base-pc1.qcow2"   
    
    if not control_state("LAN","1"):
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.crear_red()
        if2.crear_red()
        control_add("LAN")
        call(["sudo","ifconfig","LAN1","10.11.1.3/24"])
        call(["sudo","ip","route","add","10.11.0.0/16","via","10.11.1.1"])


    for nombre_mv in next_arg:
        if not control_search(nombre_mv):
            nombre = MV(nombre_mv)
            router = False
            if nombre_mv == "lb":
                router = True
            nombre.crear_mv(imagen, router,num_server)
            control_add(nombre_mv)
        else:
            logging.warning(f"La maquina {nombre_mv} ya existe\n")
    
elif second_arg == 'arrancar':

    # Arrancar maquinas
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"0"):    
                nombre = MV(nombre_mv)
                nombre.arrancar_mv() 
                control_change_state(nombre_mv,"1")
            else:
               logging.warning(f"La maquina {nombre_mv} ya esta arrancada\n")
        else:
            logging.warning(f"La maquina {nombre_mv} no existe\n")


elif second_arg == 'parar':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"1"):
                nombre = MV(nombre_mv)
                nombre.parar_mv()
                control_change_state(nombre_mv,"0")
            else:
                logging.warning(f"La maquina {nombre_mv} ya esta parada\n")
        else:
            logging.warning(f"La maquina {nombre_mv} no existe\n")
    
    time.sleep(5)
    

elif second_arg == 'liberar':
    
    for nombre_mv in next_arg:
        if control_search(nombre_mv):    
            nombre = MV(nombre_mv)
            nombre.liberar_mv()
            control_rm(nombre_mv)
        else:
            logging.warning(f"La maquina {nombre_mv} no existe\n")
   
    # Liberar redes
    with open ('control_file','r') as archivo:
        n_lines = len(archivo.readlines())

    if n_lines < 6:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.liberar_red()
        if2.liberar_red()
        control_rm("LAN")

elif second_arg == 'consola':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.mostrar_consola_mv()
elif second_arg == 'monitor':
    run(["watch", "-n", "0.25", "python3", "monitor.py"])
elif second_arg == 'monitor_mv':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.monitorizar_mv()
else:
    logging.warning(f"Argumento desconocido {second_arg}")
