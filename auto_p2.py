#!/usr/bin/env python3
from subprocess import call
from files_auto.lib_mv import MV,Red
import logging, sys, json
from os import path
from files_auto.control_file import control_search,control_state,control_change_state,control_add,control_rm
import time

# #########################################################################
# Verificar si existen los archivos necesarios
# #########################################################################
work = True
if not path.exists("maquinas") or not path.exists("maquinas/cdps-vm-base-pc1.qcow2") or not path.exists("maquinas/plantilla-vm-pc1.xml"):
    work = False
# #########################################################################
# #########################################################################

# #########################################################################
# Creación control_file
# #########################################################################
reset_file = False
if path.exists("files_auto/control_file") == False:
    reset_file = True
else:
    with open ('files_auto/control_file','r') as archivo:
        n_lines = len(archivo.readlines())
    if n_lines < 5:
        reset_file = True
          

if reset_file == True:
    with open ('files_auto/control_file','w') as archivo:
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
if len(sys.argv) < 2 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
    print("""
    Uso_1: auto_p2.py [opcion1] mv1 mv2 ... mvx
    Uso_2: auto_p2.py [Opcion2]
    
    opcion1:
        crear: Crea una nueva máquina virtual o red.
        arrancar: Inicia una máquina virtual o red existente.
        parar: Detiene una máquina virtual o red existente.
        liberar: Libera una máquina virtual o red existente.
        consola: Muestra la consola de una máquina virtual existente.
        info: Muestr info de cada máquina virtual
        forceReiniciar: Reinicia una máquina virtual existente. Liberandola, creandola y arrancandola.
        
        Argumento 2...N:
            mv1 mv2 ... mvx: Nombre de la máquina virtual o red a crear, arrancar, parar, liberar o mostrar la consola.
            Si no pones nada hará el proceso de operación con todas las máquinas virtuales especificadas en el fichero auto_p2.json
    
    opcion2:
        iniciar: Crea el directorio maquinas y copia los archivos necesarios, si estos no estan disponibles.
        monitor: Inicia el monitor de todas las máquinas virtuales.
        cpu_stats: Muestra el estado de las cpu de todas las máquinas.
        gestion: Abre la interfaz de gestión de HAProxy.

    
    """)
    sys.exit(0)


second_arg = sys.argv[1]
if not second_arg == 'monitor' and not second_arg == 'cpu_stats' and not second_arg == 'gestion' and not second_arg == 'iniciar': 
    next_arg = []

    all_vm = ["c1","lb"]
    for i in range(num_server):
        all_vm.append("s" + str(i+1)) 

    i=2
    if num_server <= 5:
        if len(sys.argv) > 2:
            while i < len(sys.argv) and sys.argv[i] != " ":
                if sys.argv[i] != "lb" and sys.argv[i] != "c1" and not(sys.argv[i].startswith("s") and sys.argv[i][1:].isdigit() and int(sys.argv[i][1:]) <= num_server):
                    print("")
                    logging.warning(f" Maquina {sys.argv[i]} no permitida\n")                
                else:
                    next_arg.append(sys.argv[i])
                i = i + 1
        else:
            next_arg = all_vm
        
        long_ini = len(next_arg)
        next_arg = list(set(next_arg)) # Convierte en un conjunto para eliminar duplicados y luego lo vuelve a convertir en lista
    
        if len(next_arg) != long_ini:
            logging.info("Se han eliminado argumentos duplicados\n")

    else:
        print("")
        logging.error("No se puede crear mas de 5 servidores")
        print("")
else:
    if len(sys.argv) > 2:
        print("")
        logging.warning(f"No se pueden poner argumento para " + second_arg)
        print("")
        sys.exit(1)
# #########################################################################
# Aplicacion
# #########################################################################
if second_arg == 'iniciar':
    if work:
        logging.info(" Directorio maquinas y files plantilla-vm-pc1.xml & cdps-vm-base-pc1.qcow2 ya estan disponibles\n")
    
    if path.exists("maquinas") == False:
        call(["mkdir","maquinas"])
        logging.info(" Directorio maquinas creado\n")
    if path.exists("maquinas/cdps-vm-base-pc1.qcow2") == False:
        call(["cp","/lab/cdps/pc1/cdps-vm-base-pc1.qcow2","./maquinas"])
        logging.info(" Imagen cdps-vm-base-pc1 copiada\n")
    if path.exists("maquinas/plantilla-vm-pc1.xml") == False:
        call(["cp","/lab/cdps/pc1/plantilla-vm-pc1.xml","./maquinas"])
        logging.info(" Plantilla plantilla-vm-pc1.xml copiada\n")
    sys.exit(0)

if not work:
    if not path.exists("maquinas"):
        logging.warning(" Directorio maquinas no existe\n")
    if not path.exists("maquinas/cdps-vm-base-pc1.qcow2"):
        logging.warning(" Imagen cdps-vm-base-pc1 no existe\n")
    if not path.exists("maquinas/plantilla-vm-pc1.xml"):
        logging.warning(" Plantilla plantilla-vm-pc1.xml no existe\n")
    sys.exit(1)


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
        logging.info(" La red LAN ha sido creada y host añadido a la LAN1\n")

    for nombre_mv in next_arg:
        if not control_search(nombre_mv):
            nombre = MV(nombre_mv)
            router = False
            if nombre_mv == "lb":
                router = True
            nombre.crear_mv(imagen, router,num_server)
            control_add(nombre_mv)
            logging.info(f" La maquina {nombre_mv} ha sido creada\n")
        else:
            logging.warning(f" La maquina {nombre_mv} ya existe\n")
    
elif second_arg == 'arrancar':
    
    # Arrancar maquinas
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"0"):    
                nombre = MV(nombre_mv)
                nombre.arrancar_mv(num_server) 
                control_change_state(nombre_mv,"1")
                logging.info(f" La maquina {nombre_mv} ha sido arrancada\n")
            else:
               logging.warning(f" La maquina {nombre_mv} ya esta arrancada\n")
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")


elif second_arg == 'parar':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"1"):
                nombre = MV(nombre_mv)
                nombre.parar_mv()
                control_change_state(nombre_mv,"0")
                logging.info(f" La maquina {nombre_mv} ha sido parada\n")
            else:
                logging.warning(f" La maquina {nombre_mv} ya esta parada\n")
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")
    
    time.sleep(6*len(next_arg)/6+4) 
    
elif second_arg == 'forceReiniciar':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
                nombre = MV(nombre_mv)
                call(["python3","auto_p2.py","liberar",nombre_mv])
                call(["python3","auto_p2.py","crear",nombre_mv])
                call(["python3","auto_p2.py","arrancar",nombre_mv])
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")
    
  
elif second_arg == 'liberar':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):    
            nombre = MV(nombre_mv)
            nombre.liberar_mv()
            control_rm(nombre_mv)
            logging.info(f" La maquina {nombre_mv} ha sido liberada\n")
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")
   
    # Liberar redes
    with open ('files_auto/control_file','r') as archivo:
        n_lines = len(archivo.readlines())

    if n_lines < 6:
        if control_state("LAN","1"):
            if1 = Red("LAN1")
            if2 = Red("LAN2")
            if1.liberar_red()
            if2.liberar_red()
            control_rm("LAN")
            logging.info(" La red LAN ha sido liberada\n")

elif second_arg == 'consola':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):  
            if control_state(nombre_mv,"1"):
                nombre = MV(nombre_mv)
                nombre.mostrar_consola_mv()
                logging.info(f" Abriendo consola de la máquina {nombre_mv}\n")
            else:
                logging.warning(f" La maquina {nombre_mv} no está arrancada\n")   
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")       
        
elif second_arg == 'monitor':
    call(["watch", "-n", "0.25", "python3", "files_auto/monitor.py"])

elif second_arg == 'cpu_stats':
    call(["watch", "-n", "0.25", "python3", "files_auto/cpu_stats.py"])    

elif second_arg == 'gestion':
    if control_search("lb"):
        if control_state("lb","1"):
            call(["firefox", "http://10.11.1.1:8080/stats"])
        else:
            logging.warning(f" Proxy (lb) no arrancado\n")
    else:
        logging.warning(f" Proxy (lb) no existe\n")
elif second_arg == 'info':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv, "1"):
                nombre = MV(nombre_mv)
                nombre.monitorizar_mv()
            else:
                logging.warning(f" La maquina {nombre_mv} no esta arrancada\n")
        else:
            logging.warning(f" La maquina {nombre_mv} no existe\n")
else:
    logging.warning(f" Argumento desconocido {second_arg}")
