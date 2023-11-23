from subprocess import call

# sudo virsh domstate s1
# call(["sudo","virsh","domstate","s1"])

# sudo virsh domifaddr s1
call(["sudo","virsh","domifaddr","s1"])

# sudo virsh dominfo s1