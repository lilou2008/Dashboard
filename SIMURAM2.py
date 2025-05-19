import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Colores y estilos
fondo = "#191C2C"
texto_color = "#E7E7EB"
color_barras = "#0FFFCF"
color_no_disp = "#FE3072"
color_mtbf = "#22B2FF"
color_mttr = "#FFD600"
color_linea1 = "#12FFF7"
color_linea2 = "#FF00EA"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: {fondo};
        color: {texto_color};
    }}
    .sidebar .sidebar-content {{
        background: #222236;
        color: {texto_color};
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image("LOGOANTAPACCAY.png", width=90)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.header("Ingresa tus datos RAM")
num_fallas = st.sidebar.number_input("Número de fallas", min_value=1, value=120)
MTBF = st.sidebar.number_input("MTBF (horas)", min_value=0.01, value=57.03, step=0.01)
MTTR = st.sidebar.number_input("MTTR (horas)", min_value=0.01, value=7.90, step=0.01)
tiempo_total = st.sidebar.number_input("Tiempo total simulado (horas)", min_value=0.01, value=7791.1, step=0.01)
tiempo_reparacion = st.sidebar.number_input("Tiempo fuera de servicio (horas)", min_value=0.01, value=947.5, step=0.01)
tiempo_operacion = st.sidebar.number_input("Tiempo en operación (horas)", min_value=0.01, value=6843.6, step=0.01)

Disponibilidad = tiempo_operacion / tiempo_total
Indisponibilidad = tiempo_reparacion / tiempo_total

fallas = np.random.normal(loc=MTBF, scale=MTBF*0.2, size=num_fallas)
fallas = np.clip(fallas, 1, None)
reparaciones = np.random.normal(loc=MTTR, scale=MTTR*0.2, size=num_fallas)
reparaciones = np.clip(reparaciones, 1, None)

plt.rcParams.update({
    "axes.facecolor": fondo,
    "axes.edgecolor": texto_color,
    "axes.labelcolor": texto_color,
    "figure.facecolor": fondo,
    "xtick.color": texto_color,
    "ytick.color": texto_color,
    "grid.color": "#393959",
    "text.color": texto_color,
    "font.size": 12,
})

st.title("🧠 Dashboard Simulación RAM - Parada de Planta Minera Antapaccay")
st.markdown("Simulación de confiabilidad y disponibilidad con entrada de datos en tiempo real.")

col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    ax.bar(['Disponible', 'No Disponible'], [Disponibilidad, Indisponibilidad],
           color=[color_barras, color_no_disp], edgecolor=texto_color, linewidth=2)
    ax.set_title('Disponibilidad del Sistema', fontsize=15, color=texto_color, weight='bold')
    ax.set_ylabel('Porcentaje')
    ax.set_ylim(0, 1)
    for i, v in enumerate([Disponibilidad, Indisponibilidad]):
        ax.text(i, v+0.03, f'{v*100:.2f}%', ha='center', fontweight='bold', color=texto_color, fontsize=13)
    st.pyplot(fig)

    # Comentario dinámico para disponibilidad
    if Disponibilidad >= 0.95:
        comentario_disp = "¡Excelente! El sistema mantiene una alta disponibilidad, lo que refleja una gestión óptima del mantenimiento y pocas paradas no planificadas."
    elif Disponibilidad >= 0.85:
        comentario_disp = "Buena disponibilidad, pero hay margen de mejora. Revisa las causas principales de indisponibilidad para optimizar aún más."
    else:
        comentario_disp = "Atención: La disponibilidad es baja. Esto puede afectar la productividad y requiere una revisión urgente del plan de mantenimiento."
    st.markdown(
        f"<div style='color:#0FFFCF;'><b>Interpretación:</b> {comentario_disp}</div>",
        unsafe_allow_html=True
    )

with col2:
    fig2, ax2 = plt.subplots()
    ax2.hist(fallas, bins=15, color=color_mtbf, edgecolor="#00ffd0", linewidth=1.2)
    ax2.set_title(f'Intervalos entre fallas (MTBF = {MTBF:.2f} h)', fontsize=13, color=texto_color, weight='bold')
    ax2.set_xlabel('Horas entre fallas')
    ax2.set_ylabel('Frecuencia')
    st.pyplot(fig2)

    # Comentario dinámico para MTBF
    if MTBF > 100:
        comentario_mtbf = "Las fallas son poco frecuentes. La confiabilidad del sistema es muy alta."
    elif MTBF > 50:
        comentario_mtbf = "El sistema presenta una frecuencia aceptable de fallas, pero se puede analizar para elevar la confiabilidad."
    else:
        comentario_mtbf = "Las fallas ocurren con frecuencia. Se recomienda investigar las causas para mejorar la confiabilidad."
    st.markdown(
        f"<div style='color:#22B2FF;'><b>Interpretación:</b> {comentario_mtbf}</div>",
        unsafe_allow_html=True
    )

col3, col4 = st.columns(2)
with col3:
    fig3, ax3 = plt.subplots()
    ax3.hist(reparaciones, bins=10, color=color_mttr, edgecolor="#ff00ea", linewidth=1.2)
    ax3.set_title(f'Tiempos de reparación (MTTR = {MTTR:.2f} h)', fontsize=13, color=texto_color, weight='bold')
    ax3.set_xlabel('Horas de reparación')
    ax3.set_ylabel('Frecuencia')
    st.pyplot(fig3)

    # Comentario dinámico para MTTR
    if MTTR < 5:
        comentario_mttr = "¡Óptimo! Las reparaciones son rápidas, lo que reduce la indisponibilidad."
    elif MTTR < 12:
        comentario_mttr = "Los tiempos de reparación son aceptables, aunque reducirlos podría mejorar la disponibilidad general."
    else:
        comentario_mttr = "Las reparaciones son lentas. Es importante revisar recursos, repuestos o capacitación para optimizar tiempos."
    st.markdown(
        f"<div style='color:#FFD600;'><b>Interpretación:</b> {comentario_mttr}</div>",
        unsafe_allow_html=True
    )

with col4:
    fig4, ax4 = plt.subplots()
    ax4.plot(np.cumsum(fallas), label='Operación acumulada', color=color_linea1, linewidth=2)
    ax4.plot(np.cumsum(reparaciones), label='Reparación acumulada', color=color_linea2, linewidth=2)
    ax4.set_title('Evolución Operación vs. Reparación', fontsize=13, color=texto_color, weight='bold')
    ax4.set_xlabel('N° de Fallas')
    ax4.set_ylabel('Horas acumuladas')
    ax4.legend(facecolor=fondo, edgecolor=texto_color)
    ax4.grid(True, alpha=0.4)
    st.pyplot(fig4)

    # Comentario dinámico para evolución
    gap = (np.cumsum(fallas)[-1] - np.cumsum(reparaciones)[-1]) if len(fallas) and len(reparaciones) else 0
    if gap > 5000:
        comentario_evol = "La brecha entre tiempo de operación y reparación es amplia: la planta opera eficientemente."
    elif gap > 1000:
        comentario_evol = "La planta mantiene un equilibrio aceptable entre tiempo productivo y tiempo en reparación."
    else:
        comentario_evol = "El tiempo de reparación se acerca peligrosamente al tiempo de operación: atención urgente para evitar pérdidas."
    st.markdown(
        f"<div style='color:#FF00EA;'><b>Interpretación:</b> {comentario_evol}</div>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown(
    f"""
    <div style='background:#212140;padding:15px 25px 15px 25px;border-radius:12px;color:{texto_color};font-size:16px;'>
    <b>Número de fallas:</b> {num_fallas}<br>
    <b>MTBF (h):</b> {MTBF:.2f}<br>
    <b>MTTR (h):</b> {MTTR:.2f}<br>
    <b>Disponibilidad total:</b> {Disponibilidad*100:.2f} %<br>
    <b>Indisponibilidad total:</b> {Indisponibilidad*100:.2f} %<br>
    <b>Tiempo total simulado:</b> {tiempo_total:.1f} h<br>
    <b>Tiempo fuera de servicio (reparaciones):</b> {tiempo_reparacion:.1f} h<br>
    <b>Tiempo en operación:</b> {tiempo_operacion:.1f} h
    </div>
    """,
    unsafe_allow_html=True
)
