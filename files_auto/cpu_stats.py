from subprocess import call
from control_file import control_search,control_state,control_change_state,control_add,control_rm
import json

with open('auto_p2.json', 'r') as f:
    data = json.load(f)


num_server = data['num_server']

def cpu_stats():
    # print("########    Cliente    ########")
    print("## c1 ##")
    state = "NO EXISTE"
    run = False
    if control_search("c1"):
        if control_state("c1","0"):
            state = "Parada"
        if control_state("c1","1"):
            call(["sudo","virsh","cpu-stats","c1"])
            run = True
    if run == False
        print(f"\t{state}")
    print("")
    
    # Router
    # print("########     Router    ########")
    print("## lb ##")
    state = "NO EXISTE"
    run = False
    if control_search("lb"):
        if control_state("lb","0"):
            state = "Parada"
        if control_state("lb","1"):
            call(["sudo","virsh","cpu-stats","c1"])
            run = True
    if run == False    
        print(f"\t{state}")

    print("")
    # Servidores
    for mv in range(1, num_server+1):
        name = "s" + str(mv)
        print( "## "+ name +" ##" )
        state = "NO EXISTE"
        if control_search(name):
            if control_state(name,"0"):
                state = "Parada"
            if control_state(name,"1"):
                call(["sudo","virsh","cpu-stats","c1"])
                run = True
        if run == False
            print(f"\t{state}")

cpu_stats()
