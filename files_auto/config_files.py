from lxml import etree
import getpass
from subprocess import call, run

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
            archivo.write("\tnetmask 255.255.255.0\n\n")
            # Configuración adicional para habilitar el enrutamiento
            archivo.write("# Habilitar el enrutamiento IP\n")
            archivo.write("up echo 1 > /proc/sys/net/ipv4/ip_forward\n")
        else:
            if self.nombre.startswith("s"):
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

  # Index servidores
    if self.nombre.startswith("s"):
        i = self.nombre[1:]
        with open ('index.html','w') as archivo:
            archivo.write("<html>\n")
            archivo.write(f"\t<h1>Servidor s{i}</h1>\n")
            archivo.write("</html>\n")

    # if self.nombre.startswith("s"):
    #     i = self.nombre[1:]
    #     color = "#FFFF00 "
    #     if i == "1":
    #         color="#FF0000"
    #     elif i == "2":
    #         color = "#008000"
            

    #     with open ('index.html','w') as archivo:
    #         archivo.write("<html>\n")
    #         archivo.write("<head>\n")
    #         archivo.write("\t<style>\n")
    #         archivo.write(f"\t\tbody {{background-color: {color};}}\n")  # Cambia el color según tus necesidades
    #         archivo.write("\t</style>\n")
    #         archivo.write("</head>\n")
    #         archivo.write("<body>\n")
    #         archivo.write(f"\t<h1>Servidor s{i}</h1>\n")
    #         archivo.write("</body>\n")
    #         archivo.write("</html>\n")
            
def configurar_proxy(num_server):
    with open ('haproxy.cfg','a') as archivo:
            archivo.write("\nfrontend lb\n")
            archivo.write("\tbind *:80\n")
            archivo.write("\tmode http\n\n")
            archivo.write("\tdefault_backend webservers\n")
            archivo.write("backend webservers\n")
            archivo.write("\tmode http\n")
            
            archivo.write("\tbalance roundrobin\n")
            for i in range(num_server):
               archivo.write(f"\tserver s{i+1} 10.11.2.3{i+1}:80 check\n")


# ##########################################################################
# Configuración del XML
# ##########################################################################
# Editar XML
def editar_xml(self,router,interface_red):
    user = getpass.getuser()
    tree = etree.parse(self.nombre + ".xml")
    root = tree.getroot()
    name = root.find('name')
    name.text = self.nombre
    source = root.find('.//devices/disk/source')
    source.set('file', '/mnt/tmp/' + user + '/maquinas/' + self.nombre + '.qcow2')
    devices = root.find('.//devices')
    if router == True:
        # Interfaz 1
        interface_1 = devices.find('interface')
        source_1 = interface_1.find('source')
        source_1.set('bridge', interface_red[0])
        model_1 = interface_1.find('model')
        # Interfaz 2
        interface_2 = etree.Element('interface')
        interface_2.set('type', 'bridge')
        source_2 = etree.SubElement(interface_2, 'source')
        source_2.set('bridge', interface_red[1])
        model_2 = etree.SubElement(interface_2, 'model')
        model_2.set('type', model_1.get('type'))
        index = devices.index(interface_1)
        devices.insert(index + 1, interface_2)
    else:
        source = devices.find('interface/source')
        source.set('bridge', interface_red[0])
        tree.write(self.nombre + ".xml")

    tree.write(self.nombre + ".xml")
