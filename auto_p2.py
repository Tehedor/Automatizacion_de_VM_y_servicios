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




if second_arg == 'crear':
    imagen = "./cdps-vm-base-pc1.qcow2"   
    if1 = Red("LAN1")
    if2 = Red("LAN2")
    if1.crear_red()
    if2.crear_red()
    
    # def crear_mv (self, imagen, interfaces_red, router):
    # Creacion de rotuer
    lb = MV("LB")
    lb.crear_mv( imagen,['if1', 'if2'], True)
    ip_lb = ["192.1.1.1.1","192.0.0.0"]
    crear_fiche(lb,ip_lb,True)
    # Creacion de clinete
    c1 = MV("c1")
    c1.crear_mv(imagen, ['if1'], False)
    ip_c1 = ["1234.134.132.41"]
    crear_fiche(c1,ip_c1,False)
    # Creación de Servidores
    num = "31"
    for num_server in range(1,num_server+1):
        name = "s" + num_server
        mv.crear_mv(imagen, ['if1'] , False)
        ip_mv = [f"10.11.2.{num}"]
        crear_fiche(mv,ip_mv,False)
        num = num + 1
elif second_arg == 'arrancar':
    # Arrancar maquinas
    lb.arrancar_mv()
    c1.arrancar_mv()
    for num_server in range(1,num_server+1):
        name = "s" + num_server
        name.arrancar_mv()  
    # Arrancar redes
    if1.arrancar_red()
    if2.arrancar_red()



elif second_arg == 'parar':
    lb.parar_mv()
    c1.parar_mv()
    for num_server in range(1,num_server+1):
        name = "s" + num_server
        name.parar_mv()  
elif second_arg == 'liberar':
    lb.liberar_red()
    c1.liberar_red()   
    for num_server in range(1,num_server+1):
        name = "s" + num_server
        name.liberar_red()  
    # Liberar redes
    if1.liberar_red()
    if2.liberar_red()
else:
    print(f"Error: Argumento desconocido {second_arg}")

def crear_fiche(self,ip,router):
    with open ('hostname','w') as archivo:
        
        if router == True:
            archivo.write("auto lo\n")
            archivo.write("iface lo inet loopback\n\n")
            archivo.write("auto eth0\n")
            archivo.write("iface eth0 inet static\n")
            archivo.write(f"\taddress {ip[0]}\n")
            archivo.write("\tnetmask 255.255.255.0\n")
            archivo.write("\tgateway 10.11.2.33\n")
            archivo.write("auto eth1\n")
            archivo.write("iface eth1 inet static\n")
            archivo.write(f"\taddress {ip[1]}\n")
            archivo.write("\tnetmask 255.255.255.0\n")
            archivo.write("\tgateway 10.11.2.33\n")
        else:
            if nombre.startswith("s"):
                archivo.write("auto lo\n")
                archivo.write("iface lo inet loopback\n\n")
                archivo.write("auto eth1\n")
                archivo.write("iface eth1 inet static\n")
                archivo.write(f"\taddress {ip[0]}\n")
                archivo.write("\tnetmask 255.255.255.0\n")
                archivo.write("\tgateway 10.11.1.1\n")
            else:
                archivo.write("auto lo\n")
                archivo.write("iface lo inet loopback\n\n")
                archivo.write("auto eth0\n")
                archivo.write("iface eth0 inet static\n")
                archivo.write(f"\taddress {ip[0]}\n")
                archivo.write("\tnetmask 255.255.255.0\n")
                archivo.write("\tgateway 10.11.2.1\n")
                

    call(["sudo","virth-copy-in", "-a", self.nombre + ".qcow2", "hostname", "/etc/"])
    call(["sudo","virth-copy-in", "-a", self.nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["sudo","virth-edit", "-a", self.nombre + ".qcow2", "/etc/hosts", "-e","/'127.0.1.1.*/127.0.1.1 " + self.nombre + "'/"])
    