from ncclient import manager

router = {
    "host": "192.168.56.102",
    "port": 830,
    "username": "Martinez",
    "password": "cisco123",
    "hostkey_verify": False
}

loopback_xml = """
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
            <Loopback>
                <name>2</name>
                <ip>
                    <address>
                        <primary>
                            <address>2.2.2.2</address>
                            <mask>255.255.255.255</mask>
                        </primary>
                    </address>
                </ip>
            </Loopback>
        </interface>
    </native>
</config>
"""

with manager.connect(**router) as m:
    response = m.edit_config(target='running', config=loopback_xml)
    print(response)
