# cargar_datos.py

import pandas as pd
from sklearn.model_selection import train_test_split

# Cargar dataset
df = pd.read_csv("data_temeperatura.csv")

# Variables de entrada
X = df[['hora', 'temperatura', 'humedad']]

# Variable objetivo
y = df['alerta']

# Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)