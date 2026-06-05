la carpeta app es para ejecutar la aplicacion
la caprpeta model es para crear un modelo que sera consumedo por la app

# Documentación de Uso de OpenCV, TensorFlow Lite y TinyML en el Proyecto de Monitoreo de Temperatura

## 1. Descripción General del Proyecto

El proyecto consiste en desarrollar un sistema inteligente de monitoreo de temperatura para un almacén de productos perecederos. El sistema recopila datos de temperatura mediante un sensor conectado a un microcontrolador, analiza los datos utilizando modelos de Machine Learning ligeros y muestra información en tiempo real para apoyar la toma de decisiones.

## 2. Uso de OpenCV

### Objetivo

OpenCV se utilizará para la visualización y monitoreo en tiempo real de los datos de temperatura.

### Funciones principales

* Mostrar la temperatura actual en una ventana gráfica.
* Visualizar gráficos e indicadores de estado.
* Cambiar colores o mostrar alertas visuales cuando la temperatura supere los límites de seguridad.
* Integrar la visualización con la cámara del sistema si se requiere supervisión visual del almacén.

### Ejemplo de aplicación

* Temperatura normal: indicador verde.
* Temperatura cercana al límite: indicador amarillo.
* Temperatura crítica: indicador rojo con mensaje de alerta.

### Beneficios

* Monitoreo visual sencillo e intuitivo.
* Respuesta inmediata ante condiciones críticas.
* Interfaz amigable para supervisores.

---

## 3. Uso de TensorFlow Lite

### Objetivo

TensorFlow Lite permitirá ejecutar modelos de Machine Learning optimizados para realizar predicciones rápidas sobre el comportamiento de la temperatura.

### Funciones principales

* Cargar el modelo entrenado previamente en TensorFlow.
* Ejecutar inferencias en tiempo real.
* Predecir si la temperatura superará el límite establecido en los próximos minutos.
* Reducir el consumo de memoria y procesamiento respecto al modelo original.

### Flujo de trabajo

1. Recolección de datos históricos de temperatura.
2. Entrenamiento del modelo en TensorFlow.
3. Conversión del modelo al formato TensorFlow Lite (.tflite).
4. Implementación del modelo optimizado en el sistema de monitoreo.
5. Ejecución de predicciones en tiempo real.

### Beneficios

* Menor uso de recursos computacionales.
* Mayor velocidad de inferencia.
* Compatibilidad con dispositivos embebidos.

---

## 4. Uso de TinyML

### Objetivo

TinyML permitirá ejecutar el modelo de Machine Learning directamente en un microcontrolador de bajo consumo energético.

### Funciones principales

* Procesar datos del sensor localmente.
* Ejecutar predicciones sin necesidad de conexión a internet.
* Detectar condiciones anormales de temperatura.
* Activar alertas de forma inmediata.

### Flujo de trabajo

1. El sensor captura la temperatura.
2. El microcontrolador recibe los datos.
3. El modelo TinyML procesa la información.
4. Se genera una predicción.
5. Si existe riesgo de sobrecalentamiento, se activa una alerta.

### Beneficios

* Baja latencia.
* Menor consumo energético.
* Funcionamiento autónomo.
* Reducción del tráfico de datos hacia servidores externos.

---

## 5. Integración de las Tecnologías

| Tecnología      | Función en el Proyecto                                            |
| --------------- | ----------------------------------------------------------------- |
| OpenCV          | Visualización de datos y alertas en tiempo real.                  |
| TensorFlow Lite | Ejecución optimizada del modelo de predicción.                    |
| TinyML          | Implementación del modelo en microcontroladores de baja potencia. |

### Flujo General del Sistema

1. El sensor mide la temperatura del almacén.
2. El microcontrolador recibe la información.
3. El modelo TinyML analiza los datos.
4. TensorFlow Lite ejecuta la inferencia optimizada.
5. OpenCV muestra los resultados y alertas visuales.
6. El supervisor recibe notificaciones cuando la temperatura supera los niveles de seguridad.

## 6. Resultado Esperado

El sistema permitirá monitorear continuamente las condiciones ambientales del almacén, predecir posibles aumentos de temperatura y generar alertas tempranas para proteger los productos perecederos, garantizando una operación eficiente y de bajo consumo energético.
