# cargar_modelo.py

import tensorflow as tf

def cargar_modelo():

    interpreter = tf.lite.Interpreter(
        model_path="modelo_temperatura.tflite"
    )

    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    return interpreter, input_details, output_details