import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# Crear datos más completos
data = {
    'Supervisor': ['Supervisor 1', 'Supervisor 2', 'Supervisor 2'],
    'Ejecutivo': ['Ejecutivo 1', 'Ejecutivo 2', 'Ejecutivo 3'],
    'Comentario': [
        'Comentario del Ejecutivo 1',
        'Comentario del Ejecutivo 2',
        'Comentario del Ejecutivo 3'
    ],
    'Actitud': [8, 7, 9],
    'Conocimiento': [9, 8, 6],
    'Argumentación': [7, 8, 8],
    'Confiabilidad': [9, 7, 8],
    'Claridad': [8, 9, 7],
    'Seguridad': [7, 6, 9]
}

df = pd.DataFrame(data)

# Definir dimensiones
dimensions = ['Actitud', 'Conocimiento', 'Argumentación', 'Confiabilidad', 'Claridad', 'Seguridad']

# Título y bienvenida
st.set_page_config(page_title="Panel de Evaluación", layout="wide")
st.title("Panel de Evaluación de Ejecutivos")

# Sidebar con filtros
st.sidebar.header("Filtros")
selected_supervisor = st.sidebar.selectbox("Seleccione un Supervisor", df['Supervisor'].unique())
filtered_executives = df[df['Supervisor'] == selected_supervisor]['Ejecutivo'].unique()
selected_executive = st.sidebar.selectbox("Seleccione un Ejecutivo", filtered_executives)

# Filtrar datos
filtered_data = df[(df['Supervisor'] == selected_supervisor) & (df['Ejecutivo'] == selected_executive)]

# Mostrar resultados
if not filtered_data.empty:
    st.subheader(f"Información para {selected_executive}")

    # Mostrar comentario general
    st.markdown("### Observaciones generales")
    st.markdown(
        f"""
        <div style="padding: 1rem; font-size: 1.4rem; background-color: #f1f8ff; 
                    border-radius: 8px; border: 1px solid #cce7ff;">
            {filtered_data['Comentario'].iloc[0]}
        </div>
        """, unsafe_allow_html=True
    )

    # Gráfico de radar
    st.markdown("### Evaluación: Gráfico de Radar")
    values = filtered_data[dimensions].iloc[0].values

    # Crear gráfico radar
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    values = np.concatenate((values, [values[0]]))  # Cerrar el gráfico
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=1)

    # Configuración de la escala
    ax.set_yticks(range(1, 11))
    ax.set_yticklabels([str(i) for i in range(1, 11)], fontsize=4)  # Reducir tamaño de números
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=6)  # Texto reducido para dimensiones

    ax.set_title(f"Gráfico de Evaluación", va='bottom', fontsize=5)  # Título reducido

    st.pyplot(fig)

    # Espacio para comentarios adicionales
    st.markdown("### Añadir comentarios adicionales")
    additional_comment = st.text_area(
        "Escribe tus observaciones sobre este ejecutivo:",
        placeholder="Añade aquí tus comentarios..."
    )

    # Guardar comentario en memoria temporal
    if st.button("Guardar comentario"):
        st.session_state['comments'] = st.session_state.get('comments', {})
        st.session_state['comments'][selected_executive] = additional_comment
        st.success("¡Comentario guardado exitosamente!")

    # Mostrar comentarios guardados
    if st.session_state.get('comments', {}).get(selected_executive):
        st.markdown("### Comentarios adicionales guardados")
        st.write(st.session_state['comments'][selected_executive])

else:
    st.warning("No hay datos disponibles para los filtros seleccionados.")
