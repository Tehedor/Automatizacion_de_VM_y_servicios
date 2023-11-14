import logging
from subprocess import call
from lxml import etree
import getpass
import sys

entrada = sys.argv[1]


# Creación de red
if entrada == '1':
  # ////////////////////////////////////////////////////////////
  nombre_red = "LAN1"
  # nombre_red = "LAN2"
  # ////////////////////////////////////////////////////////////
  call(["sudo","brctl","addbr",nombre_red])
  call(["sudo","ifconfig",nombre_red,"up"])
elif entrada == '2':
  # Crear máquina virtual
  # ////////////////////////////////////////////////////////////
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  user = getpass.getuser()
  # Creación de MV
  call(["qemu-img","create","-f","qcow2","-b",imagen,nombre_mv+".qcow2"])
  # Creacion de XML
  call(["cp","plantilla-vm-pc1.xml",imagen,nombre_mv + ".xml"])
elif entrada == '3':
  # ////////////////////////////////////////////////////////////
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  # Editar XML
  tree = etree.parse(imagen,nombre_mv + ".xml")
  root = tree.getroot()
  name = root.find('name')
  name.text = imagen,nombre_mv
  source = root.find('.//devices/disk/source')
  source.set('file', '/mnt/tmp/' + user + '/' + imagen,nombre_mv + '.qcow2')
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
    tree.write(imagen,nombre_mv + ".xml")

  tree.write(imagen,nombre_mv + ".xml")

elif entrada == '4':
  # ////////////////////////////////////////////////////////////
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  call(["HOME=/mnt/tmp", "sudo" ,"virt-manager"])
  call(["sudo","virsh","define",imagen,nombre_mv + ".xml"])
elif entrada == '5':
  # Configuración mv
  # ////////////////////////////////////////////////////////////
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  
  num="31"
  ip = [f"10.11.2.{num}"]
  
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
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  call(["sudo","virsh","start",imagen,nombre_mv])
elif entrada == '7':
  # Mostrar consola maquina virtual
  # ////////////////////////////////////////////////////////////
  nombre_mv = "lb"
  # nombre_mv = "c1"
  # nombre_mv = "s1"
  # ////////////////////////////////////////////////////////////
  # call(["sudo","virsh","console",imagen,nombre_mv])
  call(["xterm","-e","sudo","virsh","console",self.nombre])






def crear_fiche(nombre,ip,router):
    with open ('interfaces','w') as archivo:
        
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
        archivo.write("\tgateway 10.11.2.1\n")
      else:
        archivo.write("auto lo\n")
        archivo.write("iface lo inet loopback\n\n")
        archivo.write("auto eth0\n")
        archivo.write("iface eth0 inet static\n")
        archivo.write(f"\taddress {ip[0]}\n")
        archivo.write("\tnetmask 255.255.255.0\n")
        archivo.write("\tgateway 10.11.1.1\n")
                

    call(["sudo","virth-copy-in", "-a", nombre + ".qcow2", "hostname", "/etc/"])
    call(["sudo","virth-copy-in", "-a", nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["sudo","virth-edit", "-a", nombre + ".qcow2", "/etc/hosts", "-e","/'127.0.1.1.*/127.0.1.1" + " " + nombre + "'/"])