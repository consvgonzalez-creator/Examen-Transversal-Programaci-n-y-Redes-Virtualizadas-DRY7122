import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ROUTER_HOST = "192.168.56.103"
ROUTER_PORT = 443
ROUTER_USER = "cisco"
ROUTER_PASSWORD = "cisco123!"

BASE_URL = f"https://{ROUTER_HOST}:{ROUTER_PORT}/restconf/data"

headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}

auth = (ROUTER_USER, ROUTER_PASSWORD)

def borrar_loopback_111():
    print("\nBORRANDO INTERFAZ LOOPBACK 111")
    print("-" * 60)
    
    url = f"{BASE_URL}/ietf-interfaces:interfaces/interface=Loopback111"
    
    try:
        response = requests.delete(url, headers=headers, auth=auth, verify=False, timeout=10)
        print(f"Estado HTTP: {response.status_code}")
        if response.status_code == 204:
            print("Interfaz Loopback 111 eliminada exitosamente")
            return True
        elif response.status_code == 404:
            print("Interfaz Loopback 111 no encontrada")
            return True
        else:
            print(response.text)
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def crear_loopback_33():
    print("\nCREANDO INTERFAZ LOOPBACK 33 (DESHABILITADA)")
    print("-" * 60)
    
    url = f"{BASE_URL}/ietf-interfaces:interfaces"
    
    payload = {
        "ietf-interfaces:interface": {
            "name": "Loopback33",
            "description": "Loopback Examen Item 5",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "33.33.33.33",
                        "netmask": "255.255.255.255"
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, auth=auth, json=payload, verify=False, timeout=10)
        print(f"Estado HTTP: {response.status_code}")
        if response.status_code in [201, 200]:
            print("Interfaz Loopback 33 creada exitosamente")
            return True
        else:
            print(response.text)
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def listar_interfaces():
    print("\nLISTANDO TODAS LAS INTERFACES")
    print("-" * 60)
    
    url = f"{BASE_URL}/ietf-interfaces:interfaces"
    
    try:
        response = requests.get(url, headers=headers, auth=auth, verify=False, timeout=10)
        print(f"Estado HTTP: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\nInterfaces en formato JSON:")
            print(json.dumps(data, indent=2))
            
            with open("interfaces_backup.json", "w") as f:
                json.dump(data, f, indent=2)
            print("\nBackup guardado en: interfaces_backup.json")
            return True
        else:
            print(response.text)
            return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

print("="*60)
print("CONFIGURACION REST API - ROUTER CSR1000v")
print("Examen DRY7122 - Item 5")
print("="*60)

borrar_loopback_111()
crear_loopback_33()
listar_interfaces()

print("\n" + "="*60)
print("PROCESO COMPLETADO")
print("="*60)
