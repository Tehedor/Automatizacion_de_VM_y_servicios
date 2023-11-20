import logging
from subprocess import call,run
from lxml import etree
import getpass
from config_files import editar_xml,crear_fiche

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

# def interfaces_control(self):
#     if self.nombre == "c1"
#         interface = ["if1"]
#     elif self.nombre == "lb"
#         interface = ["if1","if2"]
#     elif self.nombre.startswith("s") and self.nombre[1:].isdigit():
#         interface = ["if2"]
#     return interface
# ##########################################################################
# ##########################################################################

# ##########################################################################
# ##########################################################################

class MV:
  def __init__(self, nombre):
    self.nombre = nombre
    log.debug('init MV ' + self.nombre)
  # def crear_mv (self, imagen, interfaces_red, router):
  def crear_mv (self, imagen, router):
    log.debug("crear_mv " + self.nombre)
    user = getpass.getuser()

    # print(self.nombre)

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

    # Configuración de la máquina virtual
    crear_fiche(self,ip_red,router)
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "hostname", "/etc/"])
    call(["rm","hostname"])
    call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "interfaces", "/etc/network/"])
    call(["rm","interfaces"])
    call(["sudo", "virt-edit", "-a", self.nombre + ".qcow2", "/etc/hosts", "-e", f"s/127.0.1.1.*/127.0.1.1 {self.nombre}/"])

    if self.nombre.startswith("s"):
      call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "index.html", "/var/www/html/"])
      call(["rm","index.html"])
    
    # Ruter
    # if router:
    #   call(["sudo","virt-copy-in", "-a", self.nombre + ".qcow2", "haproxy.cfg", "/etc/haproxy/"])
    #   call(["rm","haproxy.cfg"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv6.conf.all.forwarding=1/net.ipv6.conf.all.forwarding=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.conf.all.forwarding=1/net.ipv4.conf.all.forwarding=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.conf.default.forwarding=1/net.ipv4.conf.default.forwarding=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv6.conf.default.forwarding=1/net.ipv6.conf.default.forwarding=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv6.conf.all.forwarding=1/net.ipv6.conf.all.forwarding=1/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.conf.all.accept_redirects = 0/net.ipv4.conf.all.accept_redirects = 0/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.conf.default.accept_redirects = 0/net.ipv4.conf.default.accept_redirects = 0/"])
      # call(["sudo","virt-edit", "-a", self.nombre + ".qcow2", "/etc/sysctl.conf", "-e", "s/#net.ipv4.conf.all.send_redirects = 0/net.ipv

  def arrancar_mv (self):
    log.debug("arrancar_mv " + self.nombre)

    # Arrancar MV
    call(["sudo","virsh","start",self.nombre])

    # Balaceador de carga
    # ##########################################################
    # if self.nombre == "lb":
    #   call(["service","apache2","stop"])


    # ##########################################################
  def mostrar_consola_mv (self):
    log.debug("mostrar_mv " + self.nombre)
    # Mostrar consola
    # call(["xterm","-e","sudo","virsh","console",self.nombre])
    # Mostrar la consola sin que se dentenga el prgrama, mostrando de esta manera todas la consolas a la vez
    run(["xterm","-e","sudo","virsh","console",self.nombre])
  def parar_mv (self):
    log.debug("parar_mv " + self.nombre)

    #  Detener las maquinas virutales con virsh shutdown
    call(["sudo","virsh","shutdown",self.nombre]) #Apagar la consola de manera suave


  def liberar_mv (self):
    log.debug("liberar_mv " + self.nombre)
    # Liberar MV
    call(["sudo","virsh","destroy",self.nombre])  #Apagar la consola de manera brusca
    call(["sudo","virsh","undefine",self.nombre]) #Eliminar la MV
    call(["rm",self.nombre + ".xml"])
    call(["rm",self.nombre + ".qcow2"])

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


