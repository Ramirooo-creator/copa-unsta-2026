import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Copa UNSTA 🏆", layout="centered")
st.title("🏆 Copa UNSTA: Economía en Conexión")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Leemos con ttl=0 para forzar a Streamlit a ver los cambios del Excel YA
    df_equipos = conn.read(worksheet="Equipos", ttl=0)
    df_partidos = conn.read(worksheet="Partidos", ttl=0)

    # Convertimos nombres de columnas a minúsculas por si acaso
    df_equipos.columns = [c.lower() for c in df_equipos.columns]
    df_partidos.columns = [c.lower() for c in df_partidos.columns]

    menu = st.sidebar.selectbox("Selecciona una opción:", ["🏠 Inicio", "🚹 Torneo Masculino", "🚺 Torneo Femenino"])

    if menu == "🏠 Inicio":
        st.subheader("¡Bienvenidos a la Copa UNSTA!")
        st.write("Selecciona tu categoría en el menú lateral.")
        st.image("https://unsta.edu.ar/wp-content/uploads/2021/05/Logo-Unsta-Azul.png", width=200)
    else:
        rama_buscada = "Masculino" if "Masculino" in menu else "Femenino"
        tab_cuadro, tab_equipos = st.tabs(["📍 Cuadro", "👥 Equipos"])

        with tab_cuadro:
            partidos_rama = df_partidos[df_partidos['rama'].str.contains(rama_buscada, case=False, na=False)]
            for _, row in partidos_rama.iterrows():
                st.markdown(f"**{row['ronda']}**")
                col1, col_vs, col2 = st.columns([2, 1, 2])
                col1.button(str(row['equipo1']), key=f"e1_{row['id']}")
                col_vs.markdown("<h4 style='text-align: center;'>VS</h4>", unsafe_allow_html=True)
                col2.button(str(row['equipo2']), key=f"e2_{row['id']}")
                st.success(f"Resultado: {row['resultado']}")
                st.markdown("---")

        with tab_equipos:
            equipos_rama = df_equipos[df_equipos['rama'].str.contains(rama_buscada, case=False, na=False)]
            for _, row in equipos_rama.iterrows():
                with st.expander(f"🛡️ {row['nombre']}"):
                    if 'logo_url' in row and str(row['logo_url']) != 'nan':
                        st.image(row['logo_url'], width=100)
                    st.write(f"**Capitán:** {row['capitán']}")
                    st.write(f"**Integrantes:** {row['jugadores']}")

except Exception as e:
    st.error("⚠️ Error de conexión o formato.")
    st.info("Revisa que las pestañas del Excel se llamen 'Equipos' y 'Partidos' y que los permisos sean públicos.")
    st.write(e)
