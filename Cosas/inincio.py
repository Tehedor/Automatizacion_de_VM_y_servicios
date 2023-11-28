from subprocess import call

call(["mkdir","maquinas"])

call(["cp","/lab/cdps/pc1/cdps-vm-base-pc1.qcow2","./maquinas"])
call(["cp","/lab/cdps/pc1/plantilla-vm-pc1.xml","./maquinas"])