from lxml import etree
import getpass

user = getpass.getuser()
name_mv = "s1"
lan = "LAN2"

tree = etree.parse('plantilla-vm-pc1.xml')

root = tree.getroot()

name = root.find('name')
name.text = name_mv
# source = root.find('device/interface/disk')
source = root.find('.//devices/disk/source')
source.set('file', '/mnt/tmp/' + user + '/' + name_mv + '.qcow2')
# bridge = root.find('.//interface/source')

source = root.find('.//devices/interface/source')
source.set('bridge', lan)

tree.write('plantilla-vm-pc1.xml')

print(user)