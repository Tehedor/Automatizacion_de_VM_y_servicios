#!/usr/bin/env python
from subprocess import call
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
# #########################################################################
# #########################################################################

def crear_fiche(self,ip,router):

    with open ('interfaces','w') as archivo:
    if router == True:
      archivo.write("auto lo\n")
      archivo.write("iface lo inet loopback\n\n")
      archivo.write("auto eth0\n")
      archivo.write("iface eth0 inet static\n")
      archivo.write(f"\taddress {ip[0]}\n")
      archivo.write("\tnetmask 255.255.255.0\n")
      archivo.write("auto eth1\n")
      archivo.write("iface eth1 inet static\n")
      archivo.write(f"\taddress {ip[1]}\n")
      archivo.write("\tnetmask 255.255.255.0\n")
    else:
      if nombre.startswith("s"):
        archivo.write("auto lo\n")
        archivo.write("iface lo inet loopback\n\n")
        archivo.write("auto eth0\n")
        archivo.write("iface eth0 inet static\n")
        archivo.write(f"\taddress {ip[0]}\n")
        archivo.write("\tnetmask 255.255.255.0\n")
        archivo.write("\tgateway 10.11.2.1\n")
      else:
        archivo.write("auto lo\n")
        archivo.write("iface lo inet loopback\n\n")
        archivo.write("auto eth0\n")
        archivo.write("iface eth0 inet static\n")
        archivo.write(f"\taddress {ip[0]}\n")
        archivo.write("\tnetmask 255.255.255.0\n")
        archivo.write("\tgateway 10.11.1.1\n")
  
    with open ('hostname','w') as archivo:
        archivo.write(self.nombre)


    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "hostname", "/etc/"])
    call(["rm","hostname"])
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["rm","interfaces"])
    call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/hosts", "-e", f"s/127.0.1.1.*/127.0.1.1 {nombre}/"])

# #########################################################################

def ip_control(self):
    if self.name == "c1"
        ip = ["10.11.1.2"]
    elif self.name == "lb"
        ip = ["10.11.1.1","10.11.2.1"]
    elif self.name.startswith("s") and self.name[1:].isdigit():
        ip = ["10.11.2.3"+self.name[1:]]
    return ip

def interfaces_control(self):
    if self.name == "c1"
        interface = ["LAN1"]
    elif self.name == "lb"
        interface = ["LAN1","LAN2"]
    elif self.name.startswith("s") and self.name[1:].isdigit():
        interface = ["LAN2"]
    return interface

# def interfaces_control(self):
#     if self.name == "c1"
#         interface = ["if1"]
#     elif self.name == "lb"
#         interface = ["if1","if2"]
#     elif self.name.startswith("s") and self.name[1:].isdigit():
#         interface = ["if2"]
#     return interface



if second_arg == 'crear':
    imagen = "cdps-vm-base-pc1.qcow2"   
    
    if next_arg == all_vm:
        if1 = Red("LAN1")
        if2 = Red("LAN2")
        if1.crear_red()
        if2.crear_red()
    
    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        interface_red = interfaces_control(nombre)
        ip_red = ip_control(nombre)
        router = False
        if nombre_mv == "lb":
            router = True
        nombre.crear_mv(imagen,interface_red, router)
        crear_fiche(nombre,ip_red,router)
    
elif second_arg == 'arrancar':
    # Arrancar maquinas


    for nombre_mv in next_arg:
        nombre = MV(nombre_mv)
        nombre.arrancar_mv() 
    
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
else:
    print(f"Error: Argumento desconocido {second_arg}")
