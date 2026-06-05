import os
import tensorflow as tf

def cargar_modelo():
    # Obtener la ruta absoluta de este archivo (cargar_modelo.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir la ruta absoluta al modelo .tflite
    model_path = os.path.join(base_dir, "modelo_temperatura.tflite")

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details