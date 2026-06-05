# predecir.py

import numpy as np

from entrada_datos import entrada_datos
from cargar_modelo import cargar_modelo

# cargar modelo
interpreter, input_details, output_details = cargar_modelo()

# obtener datos
datos = entrada_datos()

# convertir a float32
entrada = np.array(datos, dtype=np.float32)

# ingresar datos
interpreter.set_tensor(
    input_details[0]['index'],
    entrada
)

# ejecutar inferencia
interpreter.invoke()

# obtener resultado
salida = interpreter.get_tensor(
    output_details[0]['index']
)

prediccion = salida[0][0]

print("\nProbabilidad de alerta:", prediccion)

if prediccion >= 0.5:
    print("⚠ ALERTA: Temperatura peligrosa")
else:
    print("✓ Temperatura segura")