import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuración visual
st.set_page_config(page_title="Copa UNSTA 🏆", layout="centered")

st.title("🏆 Copa UNSTA: Economía en Conexión")
st.markdown("---")

# Conexión a tu Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos
df_equipos = conn.read(worksheet="Equipos")
df_partidos = conn.read(worksheet="Partidos")

# Menú lateral para navegar
menu = st.sidebar.selectbox("Selecciona una opción:", ["🏠 Inicio", "🚹 Torneo Masculino", "🚺 Torneo Femenino"])

if menu == "🏠 Inicio":
    st.subheader("¡Bienvenidos a la Copa UNSTA!")
    st.write("Selecciona tu categoría en el menú lateral para ver los cruces y equipos.")
    st.image("https://unsta.edu.ar/wp-content/uploads/2021/05/Logo-Unsta-Azul.png", width=200)

else:
    rama_buscada = "Masculino" if "Masculino" in menu else "Femenino"
    
    # --- PESTAÑAS INTERNAS ---
    tab_cuadro, tab_equipos = st.tabs(["📍 Cuadro del Torneo", "👥 Equipos Inscritos"])

    with tab_cuadro:
        st.header(f"Fase de Eliminatorias - {rama_buscada}")
        partidos_rama = df_partidos[df_partidos['Rama'] == rama_buscada]
        
        for index, row in partidos_rama.iterrows():
            with st.container():
                st.markdown(f"**{row['Ronda']}**")
                col1, col_vs, col2 = st.columns([2, 1, 2])
                with col1:
                    st.button(f"{row['Equipo1']}", key=f"e1_{row['ID']}", use_container_width=True)
                with col_vs:
                    st.markdown("<h4 style='text-align: center;'>VS</h4>", unsafe_allow_html=True)
                with col2:
                    st.button(f"{row['Equipo2']}", key=f"e2_{row['ID']}", use_container_width=True)
                
                # Mostrar el resultado debajo
                st.success(f"Resultado: {row['Resultado']}")
                st.markdown("---")

    with tab_equipos:
        st.header(f"Lista de Equipos - {rama_buscada}")
        equipos_rama = df_equipos[df_equipos['Rama'] == rama_buscada]
        
        for index, row in equipos_rama.iterrows():
            with st.expander(f"🛡️ {row['Nombre']}"):
                st.image(row['Logo_URL'], width=100)
                st.write(f"**Capitán:** {row['Capitán']}")
                st.write(f"**Integrantes:** {row['Jugadores']}")
