from subprocess import call
from control_file import control_search,control_state,control_change_state,control_add,control_rm
import json

with open('auto_p2.json', 'r') as f:
    data = json.load(f)


num_server = data['num_server']

def monitor():
    # Cliente
    print("###### Configuración LAN ######")
    state = "Desconectadas"
    if control_search("LAN"):
        if control_state("LAN","1"):
            state = "Conectadas"
            
    print(f"   LAN1 & LAN2:  {state}")

    print("")

    print("########    Cliente    ########")
    state = "NO EXISTE"
    if control_search("c1"):
        if control_state("c1","0"):
            state = "Parada"
        if control_state("c1","1"):
            state = "Arrancada"


    print(f"\tc1:  {state}")

    print("")
    
    # Router
    print("########     Router    ########")
    state = "NO EXISTE"
    if control_search("lb"):
        if control_state("lb","0"):
            state = "Parada"
        if control_state("lb","1"):
            state = "Arrancada"

    print(f"\tlb:  {state}")


    print("")
    # Servidores
    print("########  Servidores   ########")
    for mv in range(1, num_server+1):
        name = "s" + str(mv)
        state = "NO EXISTE"
        if control_search(name):
            if control_state(name,"0"):
                state = "Parada"
            if control_state(name,"1"):
                state = "Arrancada"
        print(f"\t{name}:  {state}")


monitor()
