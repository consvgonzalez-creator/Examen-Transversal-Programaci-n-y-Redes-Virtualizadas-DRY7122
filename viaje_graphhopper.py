API_KEY = "25a1e42e-29fa-4697-a0ff-609a0f8383c4"
GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

def obtener_coordenadas(ciudad):
    url = f"{GEOCODE_URL}q={ciudad}&key={API_KEY}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if 'hits' in datos and len(datos['hits']) > 0:
        lat = datos['hits'][0]['point']['lat']
        lng = datos['hits'][0]['point']['lng']
        return lat, lng
    return None, None

while True:
    print("\n--- Planificador de Viajes (Chile - Perú) ---")
    
    # Solicitar ciudad de origen y destino 
    # Salir con la letra 's' 
    origen = input("Ingrese la Ciudad de Origen (o 's' para salir): ")
    if origen.lower() == 's':
        print("Saliendo del programa...")
        break

    destino = input("Ingrese la Ciudad de Destino (o 's' para salir): ")
    if destino.lower() == 's':
        print("Saliendo del programa...")
        break


    print("\nMedios de transporte disponibles: car (auto), bike (bicicleta), foot (a pie)")
    vehiculo = input("Elija el tipo de medio de transporte (o 's' para salir): ")
    if vehiculo.lower() == 's':
        print("Saliendo del programa...")
        break


    lat_origen, lng_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino = obtener_coordenadas(destino)

    if lat_origen and lat_destino:
        rutas_url = f"{ROUTE_URL}point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&vehicle={vehiculo}&locale=es&key={API_KEY}"
        respuesta_ruta = requests.get(rutas_url)
        datos_ruta = respuesta_ruta.json()

        if 'paths' in datos_ruta:
            ruta = datos_ruta['paths'][0]
            
 
            distancia_m = ruta['distance']
            distancia_km = distancia_m / 1000
            distancia_mi = distancia_km * 0.621371
            

            tiempo_ms = ruta['time']
            tiempo_s = tiempo_ms / 1000
            horas = math.floor(tiempo_s / 3600)
            minutos = math.floor((tiempo_s % 3600) / 60)
            segundos = math.floor(tiempo_s % 60)


            print("\n" + "="*40)
            print("RESUMEN DEL VIAJE")
            print("="*40)
            print(f"Origen: {origen.capitalize()}")
            print(f"Destino: {destino.capitalize()}")
            print(f"Medio de transporte: {vehiculo}")
            print(f"Distancia: {distancia_km:.2f} kilómetros / {distancia_mi:.2f} millas")
            print(f"Duración: {horas} horas, {minutos} minutos, {segundos} segundos")
            
            print("\n--- Narrativa del Viaje ---")
            for instruccion in ruta['instructions']:
                texto = instrucción['text']
                dist_inst = instruccion['distance'] / 1000
                print(f"- {texto} ({dist_inst:.2f} km)")
            print("="*40 + "\n")
        else:
            print("\nError: No se encontró una ruta terrestre factible entre estas ciudades para el transporte seleccionado.")
    else:
        print("\nError: No se pudieron encontrar las coordenadas de una o ambas ciudades. Verifique los nombres.")
