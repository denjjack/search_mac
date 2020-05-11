""" Python program to search for mac address in the local network."""



from netmiko import ConnectHandler
import getpass
import re

# input user data
devices_ip = input ("Enter head IP: ")
user = input('Username: ')
secret_pass = getpass.getpass(prompt='Enter password: ')
request_mac = input ("Enter request mac (H.H.H): ")


def connect():
    """connect to device"""
    device = {
        'device_type': 'cisco_ios',
        'host': devices_ip,
        'username': user,
        'password': secret_pass,
        }
    net_connect = ConnectHandler(**device)
    return net_connect

print('Connection to device {}'.format(devices_ip))


def get_so_mac():
    """getting local/source mac"""
    data = connect().send_command("sh ip arp " + devices_ip)
    data = str(data)
    mac_address = re.compile(r"((?:[\da-fA-F]{4}[.]){2}[\da-fA-F]{4}|(?:[\da-fA-F]{2}[:\-]){5}[\da-fA-F]{2})")
    mac = re.findall(mac_address, data)
    return mac

so_mac = get_so_mac()
so_mac = so_mac[0]
so_mac = str(so_mac)


def get_vlans():
    """getting all vlans on device"""
    data = connect().send_command("show vlan brief")
    data = str(data)
    vlanpt = re.compile(r"\s+(?P<vlanid>\d+)")
    vlans = re.findall(vlanpt, data)
    return vlans

vlans = get_vlans()


def tracer_mac():
    """search mac in network"""
    for vlan in vlans:
        command = ("traceroute mac" + " " + so_mac + " " + request_mac + " " + "Vlan" + " " + vlan)
        data = connect().send_command(command)
        data = str(data)
        dest = re.compile(r"not found")
        tracer = re.findall(dest, data)
        if tracer == ["not found"]:
            continue
        else:
            print(data)
            break

tracer_mac()



