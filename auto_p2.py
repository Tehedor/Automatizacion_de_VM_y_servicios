#!/usr/bin/env python

from lib_mv import MV,Red
import logging, sys, json



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
# #########################################################################


with open('auto_p2.json', 'r') as f:
    data = json.load(f)

num_server = data['num_server']
# debug = data['debug']


if len(sys.argv) < 2:
    print("Error: No se proporcionó el segundo argumento.")
    sys.exit(1)

second_arg = sys.argv[1]

# mv = MV()
# red = Red()

if second_arg == 'crear':
    imagen = "cdps-vm-base-pc1.qcow2"   
    if1 = Red("LAN1")
    if2 = Red("LAN2")
    if1.crear_red()
    if2.crear_red()
    
    # def crear_mv (self, imagen, interfaces_red, router):
    # Creacion de rotuer
    lb = MV("LB")
    lb.arrancar_mv( imagen,['if1', 'if2'], True)
    # Creacion de clinete
    c1 = MV("c1")
    mv.arrancar_mv(imagen, 'if1', False)
    # Creación de Servidores
    for num_server in range(1,num_server+1):
        name = "s" + num_server
        mv.arrancar_mv(imagen, 'if1' , False)
    
elif second_arg == 'arrancar':
    mv.crear_mv()

elif second_arg == 'parar':
    mv.parar_mv()
elif second_arg == 'liberar':
    mv.lib_mb()
else:
    print(f"Error: Argumento desconocido {second_arg}")

