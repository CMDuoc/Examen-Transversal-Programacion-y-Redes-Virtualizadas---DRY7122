# netconf.py
from ncclient import manager
import xmltodict
import xml.dom.minidom

# === PARÁMETROS DE CONEXIÓN ===
ROUTER_IP = "192.168.56.104"
NETCONF_PORT = 830
USER = "cmartinez"
PASSWORD = "cisco123"

# Hostname con los apellidos solicitados
NUEVO_HOSTNAME = "Martinez-Campos"

# === PAYLOAD XML (Modelo YANG Cisco-IOS-XE-native) ===
config_xml = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>{NUEVO_HOSTNAME}</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <description>Creado via NETCONF - Examen Transversal DRY7122</description>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def aplicar_netconf():
    print("=" * 60)
    print(f"CONECTANDO VÍA NETCONF A {ROUTER_IP}:{NETCONF_PORT}...")
    print("=" * 60)

    try:
        # Nota: 'hostkey_verify=False' corregido para la versión de ncclient de la VM DEVASC
        with manager.connect(
            host=ROUTER_IP,
            port=NETCONF_PORT,
            username=USER,
            password=PASSWORD,
            hostkey_verify=False,
            device_params={'name': 'iosxe'},
            timeout=30
        ) as netconf_mgr:

            print("[+] Conexión NETCONF/SSH establecida con éxito.")
            print("[+] Enviando cambios vía edit_config XML...")

            # Modificar la configuración running del CSR1000v
            rpc_reply = netconf_mgr.edit_config(
                target='running',
                config=config_xml
            )

            # Validar respuesta
            respuesta = xmltodict.parse(rpc_reply.xml)

            if 'ok' in respuesta.get('rpc-reply', {}):
                print("\n" + "=" * 60)
                print("¡CONFIGURACIÓN APLICADA EXITOSAMENTE!")
                print("=" * 60)
                print(f"✔ Hostname cambiado a: {NUEVO_HOSTNAME}")
                print("✔ Interfaz Loopback 11 configurada:")
                print("   - IP: 11.11.11.11")
                print("   - Máscara: 255.255.255.255 (/32)")
                print("=" * 60)
            else:
                print("\n[!] El router devolvió una advertencia o error:")
                print(xml.dom.minidom.parseString(rpc_reply.xml).toprettyxml())

    except Exception as e:
        print(f"\n[ERROR] Falló la conexión NETCONF: {e}")

if __name__ == "__main__":
    aplicar_netconf()
