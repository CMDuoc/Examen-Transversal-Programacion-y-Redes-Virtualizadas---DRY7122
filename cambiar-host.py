from ncclient import manager

router = {
    "host": "192.168.56.102",
    "port": 830,
    "username": "Martinez",
    "password": "cisco123",
    "hostkey_verify": False
}

config_xml = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>Martinez-Campos</hostname>
    </native>
</config>
"""

with manager.connect(**router) as m:
    response = m.edit_config(target='running', config=config_xml)
    print("Respuesta del servidor:")
    print(response)
