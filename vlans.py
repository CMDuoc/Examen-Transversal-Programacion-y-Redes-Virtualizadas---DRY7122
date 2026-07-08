# vlans.py

def verificar_vlan():
    print("=== Verificador de Rango de VLANs ===")
    try:
        vlan = int(input("Ingrese el número de VLAN: "))
        
        if 1 <= vlan <= 1005:
            print(f"La VLAN {vlan} corresponde al RANGO NORMAL (1 - 1005).")
        elif 1006 <= vlan <= 4094:
            print(f"La VLAN {vlan} corresponde al RANGO EXTENDIDO (1006 - 4094).")
        elif vlan == 0 or vlan == 4095:
            print(f"La VLAN {vlan} es un valor reservado por el protocolo IEEE 802.1Q.")
        else:
            print("Número de VLAN fuera del rango válido (1 - 4094).")
            
    except ValueError:
        print("Error: Debe ingresar un número entero válido.")

if __name__ == "__main__":
    verificar_vlan()
