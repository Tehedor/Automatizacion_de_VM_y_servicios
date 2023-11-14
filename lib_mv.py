import logging
from subprocess import call
from lxml import etree
import getpass

log = logging.getLogger('auto_p2')
    
class MV:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init MV ' + self.nombre)
  def crear_mv (self, imagen, interfaces_red, router):
    log.debug("crear_mv " + self.nombre)
    user = getpass.getuser()
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


