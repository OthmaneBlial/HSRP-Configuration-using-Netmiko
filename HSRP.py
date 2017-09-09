from netmiko import ConnectHandler

SW1 = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.1.1',
    'username': 'user',
    'password': 'pass',
}

SW2 = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.1.2',
    'username': 'user',
    'password': 'pass',
}

def ifNotNone(cmd, condition):
	if condition == "None":
		return "None"
	else:
		return cmd

def config_interface(interface, address):
	return ["int "+ interface +"", "no switchport" , "no sh", "ip add "+ address +" 255.255.255.0"]


def config_eigrp(id, network):
	return ["router eigrp "+ id +"", "no auto", "network "+ network]


def config_standby(interface, id, virtual_address, priority= "None", preempt= "None", authentication_key= "None"):
	commands = ["int " + interface , "standby "+ id +" ip  "+ virtual_address +" ",
	ifNotNone("standby "+ id +" priority "+ priority +" ", priority), 
	ifNotNone("standby "+ id +" preempt ", preempt), 
	ifNotNone("standby "+ id +" authentication "+authentication_key+"", authentication_key)]
	return [cmd for cmd in commands if cmd != "None"]

SWITCHES = [SW1, SW2]



def configure_hsrp(SWITCHES):
	print("Applying HSRP configuration to SWITCHES")
	idx = 0
	for SWITCH in SWITCHES:
		idx += 1
		net_connect = ConnectHandler(**SWITCH)
		config_commands = config_interface('g0/0', '10.10.10.'+ str(idx)) + config_interface('g0/1', '10.10.20.'+ str(idx))
		config_commands += config_interface('g0/2', '10.10.30.'+ str(idx))
		config_commands += config_standby('g0/0', '10', '10.10.10.10') + config_standby('g0/1', '20', '10.10.20.20')
		config_commands += config_eigrp('1', '0.0.0.0')
		output = net_connect.send_config_set(config_commands)
		#print(output)
	print("HSRP configuration has finished!")


def show_hsrp(SWITCHES):
	print("Fetching HSRP statuts from SWITCHES")
	for SWITCH in SWITCHES:
		net_connect = ConnectHandler(**SWITCH)
		output = net_connect.send_command_expect('show standby')
		print(output)


configure_hsrp(SWITCHES)

show_hsrp(SWITCHES)






