#!/usr/bin/env python
from subprocess import call, run
from lib_mv import MV,Red
import logging, sys, json

# #########################################################################

with open('auto_p2.json', 'r') as f:
    data = json.load(f)


num_server = data['num_server']
# debug = data['debug']

if len(sys.argv) < 2:
    print("Error: No se proporcionó el segundo argumento.")
    sys.exit(1)

second_arg = sys.argv[1]

next_arg = []
i=2

all_vm = ["c1","lb","s1","s2","s3"] 
if len(sys.argv) > 1:
    if sys.argv[2] == " ":
        next_arg = all_vm

    else:
        while i < len(sys.argv) and sys.argv[i] != " ":
            if sys.argv[i] != "lb" and sys.argv[i] != "c1" and (self.name.startswith("s") and self.name[1:].isdigit()):
                next_arg.append(sys.argv[i])
                i = i + 1
            else:
                print(f"maquina {sys.argv[i]} no se puede crear")

# #########################################################################
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


if second_arg == 'crear':
    imagen = "cdps-vm-base-pc1.qcow2"   
    
    if next_arg == all_vm:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.crear_red()
        if2.crear_red()
    
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        router = False
        if nombre_mv == "lb":
            router = True
        nombre.crear_mv(imagen,interface_red, router)
    
elif second_arg == 'arrancar':
    # Arrancar maquinas


    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.arrancar_mv() 
        nombre.mostrar_consola_mv()
        
    # Arrancar redes
    if next_arg == all_vm:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.arrancar_red()
        if2.arrancar_red()


elif second_arg == 'parar':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.parar_mv()
      
elif second_arg == 'liberar':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.liberar_mv()
   
    # Liberar redes
    if next_arg == all_vm:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.liberar_red()
        if2.liberar_red()

elif second_arg == 'consola':
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        run(["xterm","-e","sudo","virsh","console",nombre_mv])
elif second_arg == 'monitor':
    run(["watch", "-n", "2", "virsh", "list", "--all"])
else:
    print(f"Error: Argumento desconocido {second_arg}")
