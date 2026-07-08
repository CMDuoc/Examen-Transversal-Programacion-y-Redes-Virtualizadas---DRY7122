import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://192.168.56.102/restconf/data/Cisco-IOS-XE-native:native/interface"
headers = {
    "Content-Type": "application/yang-data+json",
    "Accept": "application/yang-data+json"
}
auth = ("Martinez", "cisco123")

payload = {
    "Cisco-IOS-XE-native:Loopback": {
        "name": "1",
        "ip": {
            "address": {
                "primary": {
                    "address": "1.1.1.1",
                    "mask": "255.255.255.255"
                }
            }
        },
        "shutdown": [None]
    }
}

response = requests.post(url, headers=headers, auth=auth, json=payload, verify=False)
print(f"Status Code: {response.status_code}")
