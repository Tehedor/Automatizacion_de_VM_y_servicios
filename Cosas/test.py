import logging
from subprocess import call
from lxml import etree
import getpass
import sys

entrada = sys.argv[1]

imagen = "cdps-vm-base-pc1.qcow2"
user = getpass.getuser()

# nombre_mv = "lb"
nombre_mv = "c1"
# nombre_mv = "s2"

def crear_fiche(nombre,ip,router):

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
    archivo.write(nombre)


  call(["sudo","virt-copy-in", "-a", nombre + ".qcow2", "hostname", "/etc/"])
  call(["rm","hostname"])
  call(["sudo","virt-copy-in", "-a", nombre + ".qcow2", "interfaces", "/etc/network/"])
  call(["rm","interfaces"])
  call(["sudo", "virt-edit", "-a", nombre + ".qcow2", "/etc/hosts", "-e", f"s/127.0.1.1.*/127.0.1.1 {nombre}/"])
  # call(["sudo","virt-edit", "-a", nombre + ".qcow2", "/etc/hosts", "-e","pruebas"])

  # sudo bash -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
  # call(["sudo", "bash", "-a", nombre + ".qcow2", "/proc/sys/net/ipv4/ip_forward", "-e", "s/0/1"])

# Creación de red
if entrada == '1':
  # call(["mkdir","/mnt/tmp/" + user])
  # ////////////////////////////////////////////////////////////
  nombre_red = ["LAN1","LAN2"]
  # ////////////////////////////////////////////////////////////
  for lan in nombre_red:
    call(["sudo","brctl","addbr",lan])
    call(["sudo","ifconfig",lan,"up"])
elif entrada == '2':
  # Crear máquina virtual
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  # Creación de MV
  call(["qemu-img","create","-f","qcow2","-b",imagen , nombre_mv+".qcow2"])
  # Creacion de XML
  call(["cp","plantilla-vm-pc1.xml", nombre_mv + ".xml"]) 
elif entrada == '3':
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  
  num="31"
  interfaces_red = ["LAN2"]
  
  router = False
  if nombre_mv == "lb":
    router = True
    interfaces_red = ["LAN1","LAN2"]
  elif nombre_mv == "c1":
    interfaces_red = ["LAN1"]

  # ////////////////////////////////////////////////////////////
  # Editar XML
  user = getpass.getuser()
  tree = etree.parse(nombre_mv + ".xml")
  root = tree.getroot()
  name = root.find('name')
  name.text = nombre_mv
  source = root.find('.//devices/disk/source')
  # /mnt/tmp/XXX/XXX.qcow2
  source.set('file', 'mnt/tmp/' + user + '/' + nombre_mv + '.qcow2')
  devices = root.find('.//devices')
  if router == True:
    # Interfaz 1
    interface_1 = devices.find('interface')
    source_1 = interface_1.find('source')
    source_1.set('bridge', interfaces_red[0])
    model_1 = interface_1.find('model')
    # Interfaz 2
    interface_2 = etree.Element('interface')
    interface_2.set('type', 'bridge')
    source_2 = etree.SubElement(interface_2, 'source')
    source_2.set('bridge', interfaces_red[1])
    model_2 = etree.SubElement(interface_2, 'model')
    model_2.set('type', model_1.get('type'))
    index = devices.index(interface_1)
    devices.insert(index + 1, interface_2)
  else:
    source = devices.find('interface/source')
    source.set('bridge', interfaces_red[0])
    tree.write(nombre_mv + ".xml")

  tree.write(nombre_mv + ".xml")

elif entrada == '4':
  # definir maquina
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  # call(["HOME=/mnt/tmp", "sudo" ,"virt-manager"])
  call(["sudo","virsh","define",nombre_mv + ".xml"])
elif entrada == '5':
  # Configuración mv
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  
  # num="32"
  # ip = [f"10.11.2.{num}"]
  ip = ["10.11.2.32"]
  
  router = False
  if nombre_mv == "lb":
    router = True
    ip = ["10.11.1.1","10.11.2.1"]
  elif nombre_mv == "c1":
    ip = ["10.11.1.2"]

  # ////////////////////////////////////////////////////////////
  
  crear_fiche(nombre_mv,ip,router)
  
elif entrada == '6':
  # Arrancar maquina virtual
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  call(["sudo","virsh","start",nombre_mv])
elif entrada == '7':
  # Mostrar consola maquina virtual
  # ////////////////////////////////////////////////////////////
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  # call(["sudo","virsh","console",imagen,nombre_mv])
  call(["xterm","-e","sudo","virsh","console",nombre_mv])
  
elif entrada == '8':
  # Para máquina
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  call(["sudo","virsh","shutdown",nombre_mv])
elif entrada == '9':
  # nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # Eliminar máquina
  call(["sudo","virsh","destroy",nombre_mv])
  
  call(["sudo","virsh","undefine",nombre_mv])
  call(["rm",nombre_mv+".qcow2"])
  call(["rm",nombre_mv+".xml"])
  # Elimnar Red
  # LAN = ["LAN1","LAN2"]
  # for lan in LAN:
  #   call(["sudo","ifconfig",lan,"down"])
  #   # elminar lan
  #   call(["sudo","brctl","delbr",lan])







