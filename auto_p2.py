#!/usr/bin/env python
from subprocess import call, run
from lib_mv import MV,Red
import logging, sys, json
from os import path

# #########################################################################
# Control file 
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

with open('auto_p2.json', 'r') as f:
    data = json.load(f)


num_server = data['num_server']
# debug = data['debug']

if len(sys.argv) < 2:
    print("Error: No se proporcionó el segundo argumento.")
    sys.exit(1)


def init_log():
    # Creacion y configuracion del logger
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('auto_p2')
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.propagate = False

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

# Main
init_log()
print('CDPS - mensaje info1')

# #########################################################################
# Control de máquinas y red
# #########################################################################

def control_add(name):
    call(["cp","control_file","control_file_copia"])
    copia = open("control_file_copia","r")
    file = open("control_file" ,"w")


    # print(red)
    rellenar = False
    # copia_lines = copia.readlines()
    hecho = 0
    for i,line in enumerate(copia):
        if hecho == 0:
            if name == "LAN":
                    if i == 1:
                        rellenar = True
            else:
                if i > 2 and line.strip() == "":
                    rellenar = True

            if rellenar == True:
                if name == "LAN":
                    line = "\tLAN\t1\n"
                else:
                    file.write("\t"+ name + "\t0\n")
                hecho = 1
                misma_linea = False
                rellenar = False
            
        file.write(line)

    file.close()
    copia.close()
    call(["rm","control_file_copia"])

    
def control_rm(nombre):
    # etc/apache2/sites-available/argumento.conf
    call(["mv","control_file","control_file_copia"])
    file = open("control_file" ,"w")
    copia = open("control_file_copia","r")
    
    if nombre == "LAN":
        for i,line in enumerate(copia):
            if i == 1:
               file.write("\tLAN\t0\n")
            else:
                file.write(line)
    else:
        for line in copia:
            if nombre not in line:
                file.write(line)

    file.close()
    copia.close()
    call(["rm","control_file_copia"])

def control_search(nombre):
    with open("control_file","r") as file:
        for line in file:
            palabras = line.split()
            if nombre in palabras:
                return True
    return False

def control_state(nombre, state):
    with open("control_file","r") as file:
        for line in file:
            palabras = line.split()            
            if line.strip() != "":
                if palabras[0] == nombre:
                    if palabras[1] == state:
                        return True
                    else:
                        return False
    return False

# def control_state_mac(nombre, state):
def control_change_state(nombre, state):
    call(["cp","control_file","control_file_copia"])

    exite = control_search(nombre)

    copia = open("control_file_copia" ,"r")
    
    file = open("control_file","w") 

   
    # cambios = False    
    for line in copia:
        c = 0
        if exite == True:
            if nombre in line:
                palabras = line.split()
                if palabras[1] != state:
                    palabras[1] = "\t" + state
                    line = "\t" + palabras[0] + palabras[1] + "\n"
                    file.write(line)
                    c = 1
                    # cambios = True
        if c == 0: 
            file.write(line)
                # return True
            
    file.close()
    copia.close()
    call(["rm","control_file_copia"])
    # return True
    # return cambios


# #########################################################################
# #########################################################################


# #########################################################################
# Argumentos
# #########################################################################
second_arg = sys.argv[1]

next_arg = []

all_vm = ["c1","lb"]
for i in range(num_server):
    all_vm.append("s" + str(i+1)) 


if len(sys.argv) > 1:
    if sys.argv[2] == " ":
        next_arg = all_vm
    else:
        while i < len(sys.argv) and sys.argv[i] != " ":
            if sys.argv[i] != "lb" and sys.argv[i] != "c1" and (self.name.startswith("s") and self.name[1:].isdigit()):
                print(f"maquina {sys.argv[i]} no permitida")                
            else:
                next_arg.append(sys.argv[i])
            i = i + 1

# #########################################################################
# #########################################################################
# Ejecucion
# #########################################################################
# #########################################################################


if second_arg == 'crear':
    imagen = "cdps-vm-base-pc1.qcow2"   
    
    if not control_state("LAN","1"):
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.crear_red()
        if2.crear_red()
        control_add("LAN")
    
    for nombre_mv in next_arg:
        if not control_search(nombre_mv):
            nombre = MV(nombre_mv)
            router = False
            if nombre_mv == "lb":
                router = True
            nombre.crear_mv(imagen,interface_red, router)
            control_add(nombre_mv)
        else:
            print(f"Error: La maquina {nombre_mv} ya existe")
    
elif second_arg == 'arrancar':

    # Arrancar maquinas
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"0"):    
                nombre = MV(nombre_mv)
                nombre.arrancar_mv() 
                nombre.mostrar_consola_mv()
                control_change_state(nombre_mv,"1")
            else:
                print(f"Error: La maquina {nombre_mv} ya esta arrancada")
        else:
            print(f"Error: La maquina {nombre_mv} no existe")


elif second_arg == 'parar':
    for nombre_mv in next_arg:
        if control_search(nombre_mv):
            if control_state(nombre_mv,"1"):
                nombre = MV(nombre_mv)
                nombre.parar_mv()
                control_change_state(nombre_mv,"0")
            else:
                print(f"Error: La maquina {nombre_mv} ya esta parada")
        else:
            print(f"Error: La maquina {nombre_mv} no existe")
      
elif second_arg == 'liberar':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.liberar_mv()
        control_rm(nombre_mv)
   
    # Liberar redes
    with open ('control_file','r') as archivo:
        n_lines = len(archivo.readlines())

    if n_lines < 5:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.liberar_red()
        if2.liberar_red()
        control_state_mac("LAN","0")

elif second_arg == 'consola':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        run(["xterm","-e","sudo","virsh","console",nombre_mv])
elif second_arg == 'monitor':
    run(["watch", "-n", "2", "virsh", "list", "--all"])
else:
    print(f"Error: Argumento desconocido {second_arg}")
