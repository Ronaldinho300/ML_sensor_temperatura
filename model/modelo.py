import tensorflow as tf
from entrena_model import model

# Convertir modelo entrenado a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar archivo .tflite
with open("modelo_temperatura.tflite", "wb") as f:
    f.write(tflite_model)

print("Modelo guardado como modelo_temperatura.tflite")