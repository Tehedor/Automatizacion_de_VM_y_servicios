from subprocess import call

# #########################################################################
# Control de máquinas y red
# #########################################################################

def control_add(name):
    call(["cp","files_auto/control_file","files_auto/control_file_copia"])
    copia = open("files_auto/control_file_copia","r")
    file = open("files_auto/control_file" ,"w")


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
    call(["rm","files_auto/control_file_copia"])

    
def control_rm(nombre):
    call(["mv","files_auto/control_file","files_auto/control_file_copia"])
    file = open("files_auto/control_file" ,"w")
    copia = open("files_auto/control_file_copia","r")
    
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
    call(["rm","files_auto/control_file_copia"])

def control_search(nombre):
    with open("files_auto/control_file","r") as file:
        for line in file:
            palabras = line.split()
            if nombre in palabras:
                return True
    return False

def control_state(nombre, state):
    with open("files_auto/control_file","r") as file:
        for line in file:
            palabras = line.split()            
            if line.strip() != "":
                if palabras[0] == nombre:
                    if palabras[1] == state:
                        return True
                    else:
                        return False
    return False

def control_change_state(nombre, state):
    call(["cp","cfiles_auto/ontrol_file","files_auto/control_file_copia"])

    exite = control_search(nombre)

    copia = open("files_auto/control_file_copia" ,"r")
    
    file = open("files_auto/control_file","w") 
   
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
        if c == 0: 
            file.write(line)
            
    file.close()
    copia.close()
    call(["rm","files_auto/control_file_copia"])


# #########################################################################
# #########################################################################

def monitor(maquinas):
    # Cliente
    print("##### Cliente #####")
    state = "NO EXISTE"
    if control_search("c1"):
        if control_state("c1","0"):
            state = "Parada"
        if control_state("c1","1"):
            state = "Arrancada"

    print(f"\tc1:  {state}")

    print("")
    
    # Router
    print("##### Router #####")
    state = "NO EXISTE"
    if control_search("lb"):
        if control_state("lb","0"):
            state = "Parada"
        if control_state("lb","1"):
            state = "Arrancada"

    print(f"\tlb:  {state}")

    print("")
    # Servidores
    print("##### Servidores #####")
    state = "NO EXISTE"
    for mv in maquinas:
        if mv.startswith("s"):
            if control_search(mv):
                if control_state(mv,"0"):
                    state = "Parada"
                if control_state(mv,"1"):
                    state = "Arrancada"
            print(f"\t{mv}:  {state}")
