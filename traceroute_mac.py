
""" 
Python program to search for mac address in the local network.
denis.jakovina@gmail.com
"""


from netmiko import ConnectHandler
import getpass
import re
import ipaddress

def input_user_data():
    """ Input and check user data"""

    # input and check - IP address switch
    while True:
        try:
            devices_ip = input ("Enter head IP: ")
            ipaddress.ip_network(devices_ip)
            break
        except ValueError:
            print("Input not correct IP Address")


    user = input('Username: ')
    secret_pass = getpass.getpass(prompt='Enter password: ')


    # input and check - request MAC address
    while True:
        request_mac = input ("Enter request mac (H.H.H): ")
        mac_address = re.compile(r"(([\da-fA-F]{4}[.]){2}[\da-fA-F]{4})")
        mac = re.findall(mac_address, request_mac)
        if mac == []:
            print("Input not correct MAC Address, input in form H.H.H")
            continue
        else:
            break
    return devices_ip, user, secret_pass, request_mac

devices_ip, user, secret_pass, request_mac = input_user_data()




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


def main():
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

if __name__ == "__main__":
    main()
