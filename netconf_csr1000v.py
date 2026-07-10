from ncclient import manager
import time

ROUTER_HOST = "192.168.56.103"
ROUTER_PORT = 830
ROUTER_USER = "cisco"
ROUTER_PASSWORD = input("Contraseña: ")
NUEVO_NOMBRE = input("Nombre del router: ")

def conectar():
    mgr = manager.connect(
        host=ROUTER_HOST,
        port=ROUTER_PORT,
        username=ROUTER_USER,
        password=ROUTER_PASSWORD,
        hostkey_verify=False,
        device_params={'name': 'csr'},
        look_for_keys=False,
        allow_agent=False
    )
    return mgr

def cambiar_hostname(mgr, nombre):
    config = "<config xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\"><native xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\"><hostname>" + nombre + "</hostname></native></config>"
    mgr.edit_config(target='running', config=config)

def crear_loopback(mgr):
    config = "<config xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\"><native xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\"><interface><Loopback><name>111</name><description>Loopback Examen</description><ip><address><primary><address>111.111.111.111</address><mask>255.255.255.255</mask></primary></address></ip></Loopback></interface></native></config>"
    mgr.edit_config(target='running', config=config)

mgr = conectar()
cambiar_hostname(mgr, NUEVO_NOMBRE)
time.sleep(1)
crear_loopback(mgr)
mgr.close_session()
print("Configuracion completada")
