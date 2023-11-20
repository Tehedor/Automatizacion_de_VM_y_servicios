import logging
from subprocess import call,run
from lxml import etree
import getpass
import logging, sys, json


# #########################################################################
# Control de máquinas y red
# #########################################################################

def control_add(name):
    call(["cp","control_file","control_file_copia"])
    copia = open("control_file_copia","r")
    file = open("control_file" ,"w")


    # print(red)
    rellenar = False
    # copia_lines = copia.readlines()
    hecho = 0
    for i,line in enumerate(copia):
        if hecho == 0:
            if name == "LAN":
                    if i == 1:
                        rellenar = True
            else:
                if i > 2 and line.strip() == "":
                    rellenar = True

            if rellenar == True:
                if name == "LAN":
                    line = "\tLAN\t1\n"
                else:
                    file.write("\t"+ name + "\t0\n")
                hecho = 1
                misma_linea = False
                rellenar = False
            
        file.write(line)

    file.close()
    copia.close()
    call(["rm","control_file_copia"])

    
def control_rm(nombre):
    # etc/apache2/sites-available/argumento.conf
    call(["mv","control_file","control_file_copia"])
    file = open("control_file" ,"w")
    copia = open("control_file_copia","r")
    
    if nombre == "LAN":
        for i,line in enumerate(copia):
            if i == 1:
               file.write("\tLAN\t0\n")
            else:
                file.write(line)
    else:
        for line in copia:
            if nombre not in line:
                file.write(line)

    file.close()
    copia.close()
    call(["rm","control_file_copia"])

def control_search(nombre):
    with open("control_file","r") as file:
        for line in file:
            palabras = line.split()
            if nombre in palabras:
                return True
    return False

def control_state(nombre, state):
    with open("control_file","r") as file:
        for line in file:
            palabras = line.split()            
            if line.strip() != "":
                if palabras[0] == nombre:
                    if palabras[1] == state:
                        return True
                    else:
                        return False
    return False

# def control_state_mac(nombre, state):
def control_change_state(nombre, state):
    call(["cp","control_file","control_file_copia"])

    exite = control_search(nombre)

    copia = open("control_file_copia" ,"r")
    
    file = open("control_file","w") 

   
    # cambios = False    
    for line in copia:
        c = 0
        if exite == True:
            if nombre in line:
                palabras = line.split()
                if palabras[1] != state:
                    palabras[1] = "\t" + state
                    line = "\t" + palabras[0] + palabras[1] + "\n"
                    file.write(line)
                    c = 1
                    # cambios = True
        if c == 0: 
            file.write(line)
                # return True
            
    file.close()
    copia.close()
    call(["rm","control_file_copia"])
    # return True
    # return cambios


# #########################################################################
# #########################################################################
