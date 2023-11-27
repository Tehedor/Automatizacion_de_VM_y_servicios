import logging
from subprocess import call,run, Popen
from lxml import etree
import getpass
from config_files import editar_xml,crear_fiche,configurar_proxy
from os import chmod
from control_file import control_state

log = logging.getLogger('auto_p2')


# #########################################################################
# Control de redes
# #########################################################################

def ip_control(self):
    if self.nombre == "c1":
        ip = ["10.11.1.2"]
    elif self.nombre == "lb":
        ip = ["10.11.1.1","10.11.2.1"]
    elif self.nombre.startswith("s") and self.nombre[1:].isdigit():
        ip = ["10.11.2.3"+self.nombre[1:]]
    return ip

def interfaces_control(self):
    if self.nombre == "c1":
        interface = ["LAN1"]
    elif self.nombre == "lb":
        interface = ["LAN1","LAN2"]
    elif self.nombre.startswith("s") and self.nombre[1:].isdigit():
        interface = ["LAN2"]
    return interface

# ##########################################################################
# ##########################################################################

class MV:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init MV ' + self.nombre)

  def crear_mv (self, imagen, router,num_server):
    log.debug("crear_mv " + self.nombre)
    user = getpass.getuser()

    interface_red = interfaces_control(self)
    ip_red = ip_control(self)


    # # Creación de MV
    call(["qemu-img","create","-f","qcow2","-b",imagen,self.nombre+".qcow2"])
    # Creacion de XML
    call(["cp","plantilla-vm-pc1.xml",self.nombre + ".xml"])
    
    # Modificar XML
    editar_xml(self,router,interface_red)

    # call(["HOME=/mnt/tmp", "sudo" ,"virt-manager"])
    call(["sudo","virsh","define",self.nombre + ".xml"])

# ##########################################################################
# Configuración Ficheros Internos
# ##########################################################################

    crear_fiche(self,ip_red,router)
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "hostname", "/etc/"])
    call(["rm","hostname"])
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["rm","interfaces"])
    call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/hosts", "-e", f"s/127.0.1.1.*/127.0.1.1 {self.nombre}/"])

    # Servidores
    if self.nombre.startswith("s"):
      call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "index.html", "/var/www/html/"])
      call(["rm","index.html"])
      call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/rc.local", "-e",  r's/^\s*$/\/usr\/sbin\/apachectl start\n/'])

    # Router
    if router:
      call(["cp","haproxy","haproxy.cfg"])
      configurar_proxy(num_server)
      call(["sudo", "virt-copy-in", "-a", self.nombre + ".qcow2", "haproxy.cfg","/etc/haproxy/"])
      call(["rm","haproxy.cfg"])
      call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/rc.local", "-e",  r's/^\s*$/systemctl restart haproxy.service\n/'])

# ##########################################################################
# ##########################################################################

  def arrancar_mv (self):
    log.debug("arrancar_mv " + self.nombre)

    # Arrancar MV
    call(["sudo","virsh","start",self.nombre])

  def mostrar_consola_mv (self):
    log.debug("mostrar_mv " + self.nombre)
    # Mostrar la consola sin que se dentenga el programa, mostrando de esta manera todas la consolas a la vez
    Popen(["xterm","-e","sudo","virsh","console",self.nombre])
  def parar_mv (self):
    log.debug("parar_mv " + self.nombre)
    call(["sudo","virsh","shutdown",self.nombre]) #Parar la maquina de manera suave


  def liberar_mv (self):
    log.debug("liberar_mv " + self.nombre)
    if control_state(self.nombre,"1"):
      call(["sudo","virsh","destroy",self.nombre])  #Apagar la maquina de manera brusca
    call(["sudo","virsh","undefine",self.nombre]) #Eliminar la MV
    call(["rm",self.nombre + ".xml"])
    call(["rm",self.nombre + ".qcow2"])

  def monitorizar_mv (self):
    call(["watch","-n","0.25","sudo","virsh","dominfo",self.nombre])
    
class Red:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init Red ' + self.nombre)
      
  def crear_red(self):
      log.debug('crear_red ' + self.nombre)
      call(["sudo","brctl","addbr",self.nombre]) #Crear LAN
      call(["sudo","ifconfig",self.nombre,"up"])

  def liberar_red(self):
      log.debug('liberar_red ' + self.nombre)
      call(["sudo","ifconfig",self.nombre,"down"])
      call(["sudo","brctl","delbr",self.nombre]) #Eliminar LAN



