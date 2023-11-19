# #########################################################################
# #########################################################################
with open('auto_p2.json', 'r') as f:
    data = json.load(f)


num_server = data['num_server']


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
            archivo.write("\tnetmask 255.255.255.0\n\n")
            # # Configuración adicional para habilitar el enrutamiento
            # archivo.write("# Configuración adicional para habilitar el enrutamiento\n")
            # archivo.write("up ip route add 10.11.1.0/24 via 10.11.1.1 dev eth0\n")
            # archivo.write("up ip route add 10.11.2.0/24 via 10.11.2.1 dev eth1\n\n")
            # archivo.write("# Habilitar el enrutamiento IP\n")
            # archivo.write("up sysctl -w net.ipv4.ip_forward=1\n")
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
      # with open ('/var/www/html/index.html','w') as archivo:
        with open ('index.html','w') as archivo:
            archivo.write("<html>\n")
            archivo.write(f"\t<h1>Servidor s{i}</h1>\n")
            archivo.write("</html>\n")
    
    if router:
        with open ('haproxy.cfg','w') as archivo:
            archivo.write("frontend lb\n")
            archivo.write("\tbind *:80\n")
            archivo.write("\tmode http\n\n")
            archivo.write("\tdefault_backendwebservers\n")
            archivo.write("backend webservers\n")
            archivo.write("\tmode http\n")
            archivo.write("\tbalance roundrobin\n")
            for i in range(num_server):
                archivo.write(f"\tserver s{i+1} 10.11.2.1.3{i+1}:80 check\n")



# ##########################################################################
# Configuración del xml
# ##########################################################################
# Editar XML
def editar_xml(self,router):
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