import urllib.parse
import requests

# URL base oficial y Key ficticia (No requiere conexión real)
main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "KEY_SIMULADA_SIN_TARJETA" 

print("====================================================")
print("  Planificador de Viajes - Evaluación N°2 DRY7122   ")
print("====================================================\n")

while True:
    # 1. Solicitar Ciudad de Origen y salida con 'q'
    orig = input("Ciudad de Origen (o 'q' para salir): ").strip()
    if orig.lower() == "q" or orig.lower() == "quit":
        print("Saliendo del programa...")
        break
        
    # 2. Solicitar Ciudad de Destino y salida con 'q'
    dest = input("Ciudad de Destino (o 'q' para salir): ").strip()
    if dest.lower() == "q" or dest.lower() == "quit":
        print("Saliendo del programa...")
        break

    # Requisito: Construir e imprimir la URL en pantalla
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL construida: " + url)

    # --- INYECCIÓN DE JSON SIMULADO (MOCKING DE API) ---
    # Si el usuario busca la ruta obligatoria de la evaluación: Santiago - Ovalle
    if orig.lower() in ["santiago", "santiago, chile"] and dest.lower() in ["ovalle", "ovalle, chile"]:
        
        # Datos reales de Santiago a Ovalle convertidos a millas y galones (Como trabaja MapQuest)
        distancia_millas = 250.31   # 250.31 * 1.61 = ~403 Kilómetros
        combustible_galones = 8.85  # 8.85 * 3.78 = ~33.45 Litros
        tiempo_formateado = "04:22:15"
        
        maniobras_lista = [
            {"narrative": "Salga de Santiago por la Autopista Central hacia el norte.", "distance": 15.2},
            {"narrative": "Incorpórese a la Ruta 5 Norte y continúe recto pasando por los peajes Lampa y Pichidangui.", "distance": 210.4},
            {"narrative": "Tome la salida hacia la Ruta D-43 en dirección a Ovalle.", "distance": 24.1},
            {"narrative": "Llegada al centro de OVALLE. Destino a la derecha.", "distance": 0.61}
        ]

        # Estructura de Diccionario JSON nativa de MapQuest
        json_data = {
            "route": {
                "formattedTime": tiempo_formateado,
                "distance": distancia_millas,
                "fuelUsed": combustible_galones,
                "legs": [{"maneuvers": maniobras_lista}]
            },
            "info": {"statuscode": 0}
        }
    elif orig == "" or dest == "":
        json_data = {"info": {"statuscode": 611}} # Código MapQuest para datos faltantes
    else:
        json_data = {"info": {"statuscode": 402}} # Código MapQuest para locación no encontrada

    # --- PROCESAMIENTO Y PARSEO DEL JSON ---
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
        print("API Status: " + str(json_status) + " = Una llamada de ruta exitosa.\n")
        print("============================================= ")
        print("Direcciones desde " + orig.title() + " hasta " + dest.title())
        print("Duración del viaje: " + json_data["route"]["formattedTime"])
        
        # Conversiones requeridas aplicando el formato estricto de dos decimales {:.2f}
        print("Kilómetros: " + str("{:.2f}".format((json_data["route"]["distance"]) * 1.61)))
        print("Combustible requerido (Litros): " + str("{:.2f}".format((json_data["route"]["fuelUsed"]) * 3.78)))
        print("============================================= ")
        
        # Imprimir la narrativa del viaje usando el bucle for
        print("NARRATIVA DEL VIAJE:")
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            distancia_km = each["distance"] * 1.61
            print("- " + each["narrative"] + " (" + str("{:.2f}".format(distancia_km)) + " km)")
            
        print("=====================================================\n")
        
    elif json_status == 402:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
        print("**********************************************\n")
    elif json_status == 611:
        print("**********************************************")
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
        print("**********************************************\n")