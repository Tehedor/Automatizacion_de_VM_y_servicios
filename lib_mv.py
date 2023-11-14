import logging
from subprocess import call,run
from lxml import etree
import getpass

log = logging.getLogger('auto_p2')


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
# ##########################################################################
# ##########################################################################
    
class MV:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init MV ' + self.nombre)
  def crear_mv (self, imagen, interfaces_red, router):
    log.debug("crear_mv " + self.nombre)
    user = getpass.getuser()

    # Interfaces
    interface_red = interfaces_control(self.nombre)
    ip_red = ip_control(self.nombre)

    # Creación de MV
    call(["qemu-img","create","-f","qcow2","-b",imagen,self.nombre+".qcow2"])
    # Creacion de XML
    call(["cp","plantilla-vm-pc1.xml",self.nombre + ".xml"])
    # Editar XML
    tree = etree.parse(self.nombre + ".xml")
    root = tree.getroot()
    name = root.find('name')
    name.text = self.nombre
    source = root.find('.//devices/disk/source')
    source.set('file', '/mnt/tmp/' + user + '/' + self.nombre + '.qcow2')
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
      tree.write(self.nombre + ".xml")

    tree.write(self.nombre + ".xml")

    
    # call(["HOME=/mnt/tmp", "sudo" ,"virt-manager"])
    call(["sudo","virsh","define",self.nombre + ".xml"])

    # Configuración de la máquina virtual
    crear_fiche(self.nombre,ip_red,router)
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "hostname", "/etc/"])
    call(["rm","hostname"])
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["rm","interfaces"])
    call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/hosts", "-e", f"s/127.0.1.1.*/127.0.1.1 {nombre}/"])

    
  def arrancar_mv (self):
    log.debug("arrancar_mv " + self.nombre)

    # Arrancar MV
    call(["sudo","virsh","start",self.nombre])

  def mostrar_consola_mv (self):
    log.debug("mostrar_mv " + self.nombre)
    # Mostrar consola
    call(["xterm","-e","sudo","virsh","console",self.nombre])
  def parar_mv (self):
    log.debug("parar_mv " + self.nombre)
    
    #  Detener las maquinas virutales con virsh shutdown
    call(["sudo","virsh","shutdown",self.nombre])
    

  def liberar_mv (self):
    log.debug("liberar_mv " + self.nombre)
    # Liberar MV
    call(["sudo","virsh","destroy",self.nombre])
class Red:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init Red ' + self.nombre)

  def crear_red(self):
      log.debug('crear_red ' + self.nombre)
      # Crear 
      call(["sudo","brctl","addbr",self.nombre])
      call(["sudo","ifconfig",self.nombre,"up"])

  def liberar_red(self):
      log.debug('liberar_red ' + self.nombre)
      # comand loberar redes
      call(["sudo","ifconfig",self.nombre,"down"])
      # elminar lan
      call(["sudo","brctl","delbr",self.nombre])


