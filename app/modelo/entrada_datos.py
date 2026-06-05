# entrada_datos.py

def obtener_datos():
    hora = float(input("Hora (0-23): "))
    temperatura = float(input("Temperatura (°C): "))
    humedad = float(input("Humedad (%): "))

    return [[hora, temperatura, humedad]]