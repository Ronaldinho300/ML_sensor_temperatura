import streamlit as st
import numpy as np
import csv
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "modelo"))

from cargar_modelo import cargar_modelo
from entrada_datos import entrada_datos

# =========================
# CONFIGURACIÓN PÁGINA
# =========================
st.set_page_config(
    page_title="IoT Almacén",
    page_icon=":material/warehouse:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    .stApp {
        background-color: #0f0f0f !important;
    }
    
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label {
        color: #e2e8f0;
    }
    
    .main-header { 
        font-size: 2.2rem; 
        font-weight: 700; 
        text-align: center; 
        color: #f8fafc; 
        letter-spacing: -0.5px;
    }
    .sub-header { 
        text-align: center; 
        color: #94a3b8; 
        font-size: 1rem; 
        margin-bottom: 2rem; 
        font-weight: 400;
    }
    
    .card-base {
        background: rgba(30, 30, 30, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        transition: all 0.2s ease;
    }
    .card-base:hover {
        background: rgba(40, 40, 40, 0.8);
        border-color: rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        transform: translateY(-1px);
    }
    
    .metric-card { 
        background: rgba(25, 25, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; 
        padding: 24px; 
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    .metric-card i { 
        font-size: 1.8rem; 
        margin-bottom: 12px; 
        display: block;
        color: #94a3b8;
    }
    .metric-card .label {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
    }
    .metric-card .sub-value {
        font-size: 0.85rem;
        color: #475569;
        margin-top: 4px;
    }
    
    .alert-calor { 
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.25);
        color: #fca5a5; 
        padding: 24px; 
        border-radius: 16px; 
        text-align: center; 
        font-size: 1.2rem; 
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(239, 68, 68, 0.1);
    }
    .alert-calor i {
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
        color: #ef4444;
    }
    
    .alert-frio { 
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.25);
        color: #93c5fd; 
        padding: 24px; 
        border-radius: 16px; 
        text-align: center; 
        font-size: 1.2rem; 
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
    }
    .alert-frio i {
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
        color: #3b82f6;
    }
    
    .alert-safe { 
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #6ee7b7; 
        padding: 24px; 
        border-radius: 16px; 
        text-align: center; 
        font-size: 1.2rem; 
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(16, 185, 129, 0.1);
    }
    .alert-safe i {
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
        color: #10b981;
    }
    
    .status-dot { 
        display: inline-block; 
        width: 10px; 
        height: 10px; 
        border-radius: 50%; 
        margin-right: 8px; 
        animation: pulse 2s infinite; 
    }
    @keyframes pulse { 
        0% { opacity: 1; transform: scale(1); } 
        50% { opacity: 0.5; transform: scale(0.9); } 
        100% { opacity: 1; transform: scale(1); } 
    }
    
    .sidebar-title { 
        font-size: 1.1rem; 
        font-weight: 600; 
        color: #e2e8f0; 
    }
    .info-box { 
        background: rgba(25, 25, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 3px solid #3b82f6; 
        padding: 16px; 
        border-radius: 12px;
        backdrop-filter: blur(8px);
    }
    
    .chart-container { 
        background: rgba(25, 25, 25, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px; 
        padding: 24px;
        backdrop-filter: blur(8px);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    
    .manual-input { 
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.15); 
        border-radius: 16px; 
        padding: 24px;
        backdrop-filter: blur(8px);
    }
    
    .mode-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .mode-auto {
        background: rgba(59, 130, 246, 0.12);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .mode-manual {
        background: rgba(245, 158, 11, 0.12);
        color: #fcd34d;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .stDataFrame {
        background: rgba(25, 25, 25, 0.6) !important;
        border-radius: 12px !important;
    }
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.08), transparent);
        margin: 1.5rem 0;
    }
    
    .stNumberInput input, .stSlider, .stRadio > div {
        background: rgba(30, 30, 30, 0.8) !important;
        color: #e2e8f0 !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stToast {
        background: rgba(30, 30, 30, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SONIDO DE ALARMA (JavaScript)
# =========================
def reproducir_alarma(tipo_alerta):
    """
    Reproduce sonido de alarma usando Web Audio API.
    tipo_alerta: 'calor_extremo' o 'frio_extremo'
    """
    if tipo_alerta == "calor_extremo":
        # Sonido agudo para calor (dos tonos altos)
        js_code = """
        <script>
        (function() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;
            
            // Oscilador 1 - tono principal
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'square';
            osc1.frequency.setValueAtTime(800, now);
            osc1.frequency.exponentialRampToValueAtTime(1200, now + 0.3);
            gain1.gain.setValueAtTime(0.3, now);
            gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.5);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.5);
            
            // Oscilador 2 - tono secundario
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'square';
            osc2.frequency.setValueAtTime(600, now + 0.2);
            osc2.frequency.exponentialRampToValueAtTime(1000, now + 0.5);
            gain2.gain.setValueAtTime(0.2, now + 0.2);
            gain2.gain.exponentialRampToValueAtTime(0.01, now + 0.7);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.2);
            osc2.stop(now + 0.7);
        })();
        </script>
        """
    elif tipo_alerta == "frio_extremo":
        # Sonido grave para frío (tonos bajos)
        js_code = """
        <script>
        (function() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const now = ctx.currentTime;
            
            // Oscilador 1 - tono grave
            const osc1 = ctx.createOscillator();
            const gain1 = ctx.createGain();
            osc1.type = 'sine';
            osc1.frequency.setValueAtTime(200, now);
            osc1.frequency.exponentialRampToValueAtTime(150, now + 0.4);
            gain1.gain.setValueAtTime(0.4, now);
            gain1.gain.exponentialRampToValueAtTime(0.01, now + 0.6);
            osc1.connect(gain1);
            gain1.connect(ctx.destination);
            osc1.start(now);
            osc1.stop(now + 0.6);
            
            // Oscilador 2 - tono más grave
            const osc2 = ctx.createOscillator();
            const gain2 = ctx.createGain();
            osc2.type = 'sine';
            osc2.frequency.setValueAtTime(150, now + 0.3);
            osc2.frequency.exponentialRampToValueAtTime(100, now + 0.7);
            gain2.gain.setValueAtTime(0.3, now + 0.3);
            gain2.gain.exponentialRampToValueAtTime(0.01, now + 1.0);
            osc2.connect(gain2);
            gain2.connect(ctx.destination);
            osc2.start(now + 0.3);
            osc2.stop(now + 1.0);
        })();
        </script>
        """
    else:
        return
    
    st.components.v1.html(js_code, height=0)

# =========================
# CARGAR MODELO (caché)
# =========================
@st.cache_resource
def load_model():
    return cargar_modelo()

interpreter, input_details, output_details = load_model()

# =========================
# CSV HISTORIAL
# =========================
os.makedirs("data", exist_ok=True)
csv_file = "data/historial.csv"
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["fecha", "hora", "temperatura", "humedad", "prediccion", "tipo_alerta", "modo"])

# =========================
# FUNCIÓN: Determinar tipo de alerta
# =========================
def determinar_tipo_alerta(temperatura, prediccion):
    if prediccion < 0.5:
        return "seguro"
    elif temperatura < 3:
        return "frio_extremo"
    elif temperatura > 9:
        return "calor_extremo"
    else:
        return "seguro"

# =========================
# FUNCIÓN PREDICCIÓN
# =========================
def predecir(hora, temperatura, humedad):
    entrada = np.array([[hora, temperatura, humedad]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], entrada)
    interpreter.invoke()
    salida = interpreter.get_tensor(output_details[0]['index'])
    return float(salida[0][0])

# =========================
# FUNCIÓN GUARDAR LECTURA
# =========================
def guardar_lectura(hora, temperatura, humedad, pred, tipo_alerta, modo):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([fecha, hora, temperatura, humedad, pred, tipo_alerta, modo])
    
    st.session_state.historial.append({
        "fecha": fecha,
        "hora": hora,
        "temperatura": temperatura,
        "humedad": humedad,
        "prediccion": pred,
        "tipo_alerta": tipo_alerta,
        "modo": modo
    })
    
    if len(st.session_state.historial) > 100:
        st.session_state.historial.pop(0)

# =========================
# ESTADO DE SESIÓN
# =========================
if "historial" not in st.session_state:
    st.session_state.historial = []
if "modo" not in st.session_state:
    st.session_state.modo = "manual"
if "auto_lectura" not in st.session_state:
    st.session_state.auto_lectura = False
if "ultima_alerta_sonido" not in st.session_state:
    st.session_state.ultima_alerta_sonido = None

# =========================
# SIDEBAR - CONTROLES
# =========================
with st.sidebar:
    st.markdown('<p class="sidebar-title"><i class="fas fa-cogs"></i> Panel de Control</p>', unsafe_allow_html=True)
    
    st.session_state.modo = st.radio(
        "Modo de Operación",
        ["manual", "automatico"],
        format_func=lambda x: "Manual" if x == "manual" else "Automático (Sensor ESP32)",
        index=0 if st.session_state.modo == "manual" else 1
    )
    
    if st.session_state.modo == "automatico":
        st.session_state.auto_lectura = st.toggle(
            "Lectura Automática Activa", 
            value=st.session_state.auto_lectura,
            help="Envía datos del sensor ESP32 constantemente"
        )
        intervalo = st.slider("Intervalo (segundos)", 1, 10, 2)
    
    st.divider()
    
    if st.button("Limpiar Historial", use_container_width=True, type="secondary"):
        st.session_state.historial = []
        st.rerun()
    
    st.divider()
    
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    if st.session_state.modo == "automatico":
        st.markdown('<i class="fas fa-wifi" style="color: #60a5fa; margin-right: 8px;"></i> <b>Sensor ESP32 Simulado</b>', unsafe_allow_html=True)
    else:
        st.markdown('<i class="fas fa-hand-pointer" style="color: #fbbf24; margin-right: 8px;"></i> <b>Ingreso Manual</b>', unsafe_allow_html=True)
    st.markdown(f'<br><i class="fas fa-database" style="color: #34d399; margin-right: 8px;"></i> Total lecturas: <b>{len(st.session_state.historial)}</b>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# HEADER PRINCIPAL
# =========================
st.markdown('<p class="main-header"><i class="fas fa-warehouse"></i> Monitoreo IoT Almacén</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Sistema de alertas de temperatura en tiempo real</p>', unsafe_allow_html=True)

# =========================
# ACTUALIZACIÓN AUTOMÁTICA
# =========================
if st.session_state.modo == "automatico" and st.session_state.auto_lectura:
    st_autorefresh(interval=intervalo * 1000, key="auto_refresh")
    
    datos = entrada_datos()
    hora = int(datos[0][0])
    temperatura = float(datos[0][1])
    humedad = float(datos[0][2])
    
    pred = predecir(hora, temperatura, humedad)
    tipo_alerta = determinar_tipo_alerta(temperatura, pred)
    
    guardar_lectura(hora, temperatura, humedad, pred, tipo_alerta, "automatico")
    
    # Reproducir sonido si hay alerta y es diferente a la última
    if tipo_alerta != "seguro" and tipo_alerta != st.session_state.ultima_alerta_sonido:
        reproducir_alarma(tipo_alerta)
        st.session_state.ultima_alerta_sonido = tipo_alerta
    elif tipo_alerta == "seguro":
        st.session_state.ultima_alerta_sonido = None
    
    if tipo_alerta == "calor_extremo":
        st.toast(f"ALERTA CALOR EXTREMO: {temperatura}°C", icon=":material/warning:")
    elif tipo_alerta == "frio_extremo":
        st.toast(f"ALERTA FRÍO EXTREMO: {temperatura}°C", icon=":material/ac_unit:")
    else:
        st.toast(f"Temperatura segura: {temperatura}°C", icon=":material/check_circle:")

# =========================
# MODO MANUAL
# =========================
if st.session_state.modo == "manual":
    st.markdown('<div class="manual-input">', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top: 0; color: #fbbf24; font-size: 1.1rem;"><i class="fas fa-hand-pointer" style="margin-right: 8px;"></i> Ingreso Manual de Datos</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        hora_manual = st.number_input("Hora (0-23)", min_value=0, max_value=23, value=12, step=1)
    with col2:
        temp_manual = st.number_input("Temperatura (°C)", min_value=-10.0, max_value=70.0, value=8.0, step=0.1)
    with col3:
        hum_manual = st.number_input("Humedad (%)", min_value=0, max_value=100, value=60, step=1)
    
    if st.button("Enviar Datos al Modelo", type="primary", use_container_width=True, icon=":material/send:"):
        pred = predecir(hora_manual, temp_manual, hum_manual)
        tipo_alerta = determinar_tipo_alerta(temp_manual, pred)
        
        guardar_lectura(hora_manual, temp_manual, hum_manual, pred, tipo_alerta, "manual")
        
        # Reproducir sonido si hay alerta
        if tipo_alerta != "seguro":
            reproducir_alarma(tipo_alerta)
        
        if tipo_alerta == "calor_extremo":
            st.toast(f"ALERTA CALOR EXTREMO: {temp_manual}°C", icon=":material/warning:")
        elif tipo_alerta == "frio_extremo":
            st.toast(f"ALERTA FRÍO EXTREMO: {temp_manual}°C", icon=":material/ac_unit:")
        else:
            st.toast(f"Temperatura segura: {temp_manual}°C", icon=":material/check_circle:")
        st.success("Datos procesados correctamente")
    
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MOSTRAR DATOS ACTUALES
# =========================
if st.session_state.historial:
    ultimo = st.session_state.historial[-1]
    
    hora_actual = datetime.now().strftime("%H:%M:%S")
    hora_registro = ultimo["fecha"].split(" ")[1] if " " in ultimo["fecha"] else hora_actual
    
    modo_badge = "AUTOMÁTICO" if ultimo["modo"] == "automatico" else "MANUAL"
    modo_class = "mode-auto" if ultimo["modo"] == "automatico" else "mode-manual"
    modo_icon = "fa-wifi" if ultimo["modo"] == "automatico" else "fa-hand-pointer"
    
    st.markdown(f'<div style="text-align:center; margin-bottom: 16px;">'
                f'<span class="mode-badge {modo_class}">'
                f'<i class="fas {modo_icon}" style="margin-right: 6px;"></i>{modo_badge}</span></div>', unsafe_allow_html=True)
    
    # ===== ALERTA VISUAL =====
    tipo = ultimo.get("tipo_alerta", "seguro")
    
    if tipo == "calor_extremo":
        st.markdown(
            f'<div class="alert-calor">'
            f'<i class="fas fa-fire"></i>'
            f'ALERTA: CALOR EXTREMO<br>'
            f'<span style="font-size: 0.95rem; font-weight: 400; opacity: 0.7;">'
            f'Temperatura: {ultimo["temperatura"]}°C | Probabilidad: {ultimo["prediccion"]:.2f}</span>'
            f'</div>', 
            unsafe_allow_html=True
        )
    elif tipo == "frio_extremo":
        st.markdown(
            f'<div class="alert-frio">'
            f'<i class="fas fa-snowflake"></i>'
            f'ALERTA: FRÍO EXTREMO<br>'
            f'<span style="font-size: 0.95rem; font-weight: 400; opacity: 0.7;">'
            f'Temperatura: {ultimo["temperatura"]}°C | Probabilidad: {ultimo["prediccion"]:.2f}</span>'
            f'</div>', 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="alert-safe">'
            f'<i class="fas fa-shield-alt"></i>'
            f'TEMPERATURA SEGURA<br>'
            f'<span style="font-size: 0.95rem; font-weight: 400; opacity: 0.7;">'
            f'Probabilidad de alerta: {ultimo["prediccion"]:.2f}</span>'
            f'</div>', 
            unsafe_allow_html=True
        )
    
    # ===== MÉTRICAS =====
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f'<div class="metric-card">'
            f'<i class="fas fa-thermometer-half" style="color: #fb923c;"></i>'
            f'<div class="label">Temperatura</div>'
            f'<div class="value">{ultimo["temperatura"]}°C</div>'
            f'</div>', 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="metric-card">'
            f'<i class="fas fa-tint" style="color: #38bdf8;"></i>'
            f'<div class="label">Humedad</div>'
            f'<div class="value">{ultimo["humedad"]}%</div>'
            f'</div>', 
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            f'<div class="metric-card">'
            f'<i class="fas fa-clock" style="color: #a78bfa;"></i>'
            f'<div class="label">Hora Registro</div>'
            f'<div class="value">{hora_registro}</div>'
            f'<div class="sub-value">Hora actual: {hora_actual}</div>'
            f'</div>', 
            unsafe_allow_html=True
        )
    with col4:
        prob = ultimo['prediccion'] * 100
        if tipo == "calor_extremo":
            icono = "fa-fire"
            color_icon = "#ef4444"
            color_val = "#fca5a5"
        elif tipo == "frio_extremo":
            icono = "fa-snowflake"
            color_icon = "#3b82f6"
            color_val = "#93c5fd"
        else:
            icono = "fa-shield-alt"
            color_icon = "#10b981"
            color_val = "#6ee7b7"
        
        st.markdown(
            f'<div class="metric-card">'
            f'<i class="fas {icono}" style="color: {color_icon};"></i>'
            f'<div class="label">Prob. Alerta</div>'
            f'<div class="value" style="color: {color_val};">{prob:.1f}%</div>'
            f'</div>', 
            unsafe_allow_html=True
        )

# =========================
# GRÁFICOS
# =========================
if len(st.session_state.historial) > 1:
    tab1, tab2 = st.tabs(["Gráficos en Tiempo Real", "Tabla de Datos"])
    
    with tab1:
        temps = []
        preds = []
        for h in st.session_state.historial:
            t = h.get("temperatura")
            p = h.get("prediccion")
            if t is not None and p is not None:
                try:
                    t_float = float(t)
                    p_float = float(p) * 100
                    if np.isfinite(t_float) and np.isfinite(p_float):
                        temps.append(t_float)
                        preds.append(p_float)
                except (ValueError, TypeError):
                    continue
        
        if len(temps) >= 2:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-top: 0; color: #cbd5e1; font-size: 1rem;"><i class="fas fa-chart-line" style="margin-right: 8px; color: #fb923c;"></i> Temperatura vs Tiempo</h3>', unsafe_allow_html=True)
                st.line_chart({"Temperatura (°C)": temps}, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with col_chart2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 style="margin-top: 0; color: #cbd5e1; font-size: 1rem;"><i class="fas fa-bell" style="margin-right: 8px; color: #ef4444;"></i> Probabilidad de Alerta</h3>', unsafe_allow_html=True)
                st.area_chart({"Prob. Alerta (%)": preds}, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Datos insuficientes para generar gráficos.")
    
    with tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="margin-top: 0; color: #cbd5e1; font-size: 1rem;"><i class="fas fa-table" style="margin-right: 8px; color: #60a5fa;"></i> Historial Completo</h3>', unsafe_allow_html=True)
        df = st.session_state.historial[::-1]
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if os.path.exists(csv_file):
            with open(csv_file, "rb") as f:
                csv_data = f.read()
            st.download_button(
                label="Descargar CSV",
                data=csv_data,
                file_name="historial_sensor.csv",
                mime="text/csv",
                use_container_width=True,
                icon=":material/download:"
            )
else:
    st.info("Selecciona un modo de operación y comienza el monitoreo")