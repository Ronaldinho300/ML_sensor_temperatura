import numpy as np
import time

def entrada_datos():
    """
    Simula sensor ESP32 enviando datos aleatorios.
    Incluye temperaturas altas, normales y bajas.
    """
    hora = int(time.localtime().tm_hour)
    
    # Aleatoriamente elegir rango de temperatura
    tipo = np.random.choice(['frio_extremo', 'frio', 'normal', 'calor', 'calor_extremo'], 
                           p=[0.15, 0.2, 0.3, 0.2, 0.15])
    
    if tipo == 'frio_extremo':
        temperatura = np.random.uniform(0, 2.9)
    elif tipo == 'frio':
        temperatura = np.random.uniform(3, 4.9)
    elif tipo == 'normal':
        temperatura = np.random.uniform(5, 8.9)
    elif tipo == 'calor':
        temperatura = np.random.uniform(9, 10.9)
    else:  # calor_extremo
        temperatura = np.random.uniform(11, 15)
    
    # Humedad inversamente proporcional
    humedad = int(np.clip(80 - (temperatura * 3) + np.random.normal(0, 5), 30, 90))
    
    return [[hora, round(temperatura, 2), humedad]]


def obtener_datos():
    """
    Modo MANUAL - Solicita datos por consola.
    """
    hora = float(input("Hora (0-23): "))
    temperatura = float(input("Temperatura (°C): "))
    humedad = float(input("Humedad (%): "))

    return [[hora, temperatura, humedad]]