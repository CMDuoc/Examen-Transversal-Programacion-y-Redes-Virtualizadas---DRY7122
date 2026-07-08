# item2_distancia.py
import requests

def obtener_coordenadas(ciudad, pais):
    """Obtiene latitud y longitud desde OpenStreetMap Nominatim"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': f"{ciudad}, {pais}",
        'format': 'json',
        'limit': 1
    }
    headers = {
        'User-Agent': 'ExamenTransversal_DRY7122_DevNet'
    }
    
    try:
        r = requests.get(url, params=params, headers=headers)
        if r.status_code == 200:
            datos = r.json()
            if datos:
                return float(datos[0]['lat']), float(datos[0]['lon']), datos[0]['display_name']
    except Exception as e:
        print(f"Error al buscar coordenadas: {e}")
    return None, None, None

def calcular_viaje():
    print("=" * 60)
    print("      CÁLCULO DE DISTANCIA Y RUTA (CHILE - ARGENTINA)")
    print("=" * 60)

    while True:
        # 1. Solicitar Ciudad de Origen y Destino en español
        origen = input("\nIngrese Ciudad de Origen (Chile) [o 's' para salir]: ").strip()
        if origen.lower() == 's':
            print("\nSaliendo del programa...")
            break

        destino = input("Ingrese Ciudad de Destino (Argentina) [o 's' para salir]: ").strip()
        if destino.lower() == 's':
            print("\nSaliendo del programa...")
            break

        # 2. Selección del Medio de Transporte
        print("\nSeleccione el medio de transporte:")
        print("1. Auto")
        print("2. Bicicleta")
        print("3. Caminando")
        
        opcion = input("Elija una opción (1-3): ").strip()

        modos = {
            '1': 'car',
            '2': 'bike',
            '3': 'foot'
        }
        modo_transporte = modos.get(opcion, 'car')

        print("\nObteniendo geolocalización de las ciudades...")
        lat_ori, lon_ori, nombre_ori = obtener_coordenadas(origen, "Chile")
        lat_des, lon_des, nombre_des = obtener_coordenadas(destino, "Argentina")

        if not lat_ori or not lat_des:
            print("\n[ERROR] No se pudo encontrar una o ambas ciudades. Verifique el nombre e intente de nuevo.")
            continue

        # 3. Consulta a la API de Ruteo OSRM
        url_osrm = f"http://router.project-osrm.org/route/v1/{modo_transporte}/{lon_ori},{lat_ori};{lon_des},{lat_des}?overview=false&steps=true"
        
        try:
            r = requests.get(url_osrm)
            data = r.json()

            if data.get("code") == "Ok":
                route = data["routes"][0]
                
                # Conversión de metros a km/millas y segundos a formato legible
                distancia_m = route["distance"]
                distancia_km = distancia_m / 1000.0
                distancia_mi = distancia_km * 0.621371
                
                duracion_seg = route["duration"]
                horas = int(duracion_seg // 3600)
                minutos = int((duracion_seg % 3600) // 60)
                segundos = int(duracion_seg % 60)
                duracion_fmt = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

                print("\n" + "=" * 60)
                print(f"RESUMEN DEL VIAJE:")
                print(f"Origen:  {nombre_ori}")
                print(f"Destino: {nombre_des}")
                print("=" * 60)
                print(f"Distancia en Millas:    {distancia_mi:.2f} mi")
                print(f"Distancia en Kilómetros:{distancia_km:.2f} km")
                print(f"Duración estimada:      {duracion_fmt} (HH:MM:SS)")
                print("-" * 60)

                # 4. Narrativa del Viaje
                print("NARRATIVA DEL VIAJE:")
                pasos = route["legs"][0]["steps"]
                for i, paso in enumerate(pasos, 1):
                    nombre_calle = paso.get("name", "Vía de tránsito")
                    if not nombre_calle:
                        nombre_calle = "Siga por el camino principal"
                    dist_paso_km = paso.get("distance", 0) / 1000.0
                    print(f" {i}. Avance por '{nombre_calle}' durante {dist_paso_km:.1f} km")
                print("=" * 60)

            else:
                print("\n[ERROR] No se pudo calcular la ruta entre ambos puntos.")

        except Exception as e:
            print(f"\n[ERROR] Fallo en la conexión con la API de rutas: {e}")

if __name__ == "__main__":
    calcular_viaje()
