import cv2
import numpy as np
import time
import csv
import os
from datetime import datetime

from modelo.cargar_modelo import cargar_modelo

# =========================
# MODELO TFLITE
# =========================
interpreter, input_details, output_details = cargar_modelo()

# =========================
# ARCHIVO CSV
# =========================
os.makedirs("data", exist_ok=True)
csv_file = "data/historial.csv"

if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "hora", "temperatura", "humedad", "prediccion"])

# =========================
# HISTORIAL PARA GRAFICO
# =========================
hist_temp = []
hist_pred = []

# =========================
# FUNCION PREDICCION
# =========================
def predecir(hora, temperatura, humedad):
    entrada = np.array([[hora, temperatura, humedad]], dtype=np.float32)

    interpreter.set_tensor(input_details[0]['index'], entrada)
    interpreter.invoke()

    salida = interpreter.get_tensor(output_details[0]['index'])
    return float(salida[0][0])

# =========================
# LOOP PRINCIPAL
# =========================
while True:

    # 🔧 SIMULACION TIPO ESP32
    hora = int(time.localtime().tm_hour)
    temperatura = np.random.uniform(5, 12)
    humedad = np.random.randint(40, 80)

    pred = predecir(hora, temperatura, humedad)

    # =========================
    # GUARDAR CSV (HISTORIAL)
    # =========================
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([fecha, hora, temperatura, humedad, pred])

    # =========================
    # HISTORIAL GRAFICO
    # =========================
    hist_temp.append(temperatura)
    hist_pred.append(pred)

    if len(hist_temp) > 50:
        hist_temp.pop(0)
        hist_pred.pop(0)

    # =========================
    # ALERTA
    # =========================
    if pred > 0.5:
        color = (0, 0, 255)
        estado = "PELIGRO"
    else:
        color = (0, 255, 0)
        estado = "SEGURO"

    # =========================
    # DASHBOARD
    # =========================
    frame = np.zeros((600, 900, 3), dtype=np.uint8)

    # TITULO
    cv2.putText(frame, "DASHBOARD ALMACEN - IoT + TinyML",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    # DATOS
    cv2.putText(frame, f"Temperatura: {temperatura:.2f} C",
                (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(frame, f"Humedad: {humedad}%",
                (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(frame, f"Prediccion: {pred:.2f}",
                (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(frame, f"Estado: {estado}",
                (50, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    # =========================
    # GRAFICO SIMPLE
    # =========================
    for i in range(1, len(hist_temp)):
        cv2.line(frame,
                 (50 + (i-1)*15, 500 - int(hist_temp[i-1]*10)),
                 (50 + i*15, 500 - int(hist_temp[i]*10)),
                 (255, 255, 0), 2)

    cv2.putText(frame, "Grafico Temperatura",
                (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    # =========================
    # ALERTA VISUAL
    # =========================
    if pred > 0.5:
        cv2.rectangle(frame, (650, 100), (850, 300), (0,0,255), -1)
        cv2.putText(frame, "ALERTA!",
                    (670, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)

    cv2.imshow("Sistema Industrial - Almacen", frame)

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()