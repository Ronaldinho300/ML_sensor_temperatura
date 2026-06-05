import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Generar 1000 registros con temperaturas variadas
np.random.seed(42)

n = 1000
hora = np.random.randint(0, 24, n)

# Generar temperaturas: algunas bajas, normales y altas
temperatura = np.concatenate([
    np.random.uniform(0, 3, 200),    # Frío extremo (alerta)
    np.random.uniform(3, 5, 200),      # Frío moderado
    np.random.uniform(5, 8, 200),      # Normal
    np.random.uniform(8, 10, 200),     # Calor moderado
    np.random.uniform(10, 15, 200)     # Calor extremo (alerta)
])
np.random.shuffle(temperatura)

# Humedad inversamente proporcional a temperatura (tendencia natural)
humedad = np.clip(80 - (temperatura * 3) + np.random.normal(0, 5, n), 30, 90)

# Alerta: 1 si temperatura < 3 (frío) o temperatura > 9 (calor)
alerta = np.where((temperatura < 3) | (temperatura > 9), 1, 0)

# Crear DataFrame
df = pd.DataFrame({
    'hora': hora,
    'temperatura': np.round(temperatura, 2),
    'humedad': np.round(humedad, 0).astype(int),
    'alerta': alerta
})

# Guardar CSV
df.to_csv("data_temeperatura.csv", index=False)
print(f"Dataset generado: {len(df)} registros")
print(f"Alertas (1): {alerta.sum()} | Seguro (0): {len(df) - alerta.sum()}")

# Variables de entrada
X = df[['hora', 'temperatura', 'humedad']]
y = df['alerta']

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)