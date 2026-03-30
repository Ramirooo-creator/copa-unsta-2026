import streamlit as st
import pandas as pd

st.set_page_config(page_title="Copa UNSTA 🏆", layout="centered")
st.title("🏆 Copa UNSTA: Economía en Conexión")

# ID de tu Google Sheet (sacado de tu URL)
sheet_id = "194B-UU530jc-SheTk7DX0b7Bg8dJ7GI63aDbviPuHBw"

# URLs para descargar las pestañas como CSV directamente
url_equipos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Equipos"
url_partidos = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Partidos"

try:
    # Leemos los datos directamente
    df_equipos = pd.read_csv(url_equipos)
    df_partidos = pd.read_csv(url_partidos)

    # Limpieza de columnas (pasamos todo a minúsculas)
    df_equipos.columns = [c.lower() for c in df_equipos.columns]
    df_partidos.columns = [c.lower() for c in df_partidos.columns]

    menu = st.sidebar.selectbox("Selecciona una opción:", ["🏠 Inicio", "🚹 Torneo Masculino", "🚺 Torneo Femenino"])

    if menu == "🏠 Inicio":
        st.subheader("¡Bienvenidos a la Copa UNSTA!")
        st.image("https://unsta.edu.ar/wp-content/uploads/2021/05/Logo-Unsta-Azul.png", width=200)
    else:
        rama = "Masculino" if "Masculino" in menu else "Femenino"
        t1, t2 = st.tabs(["📍 Cuadro", "👥 Equipos"])

        with t1:
            # Filtramos partidos por rama
            partidos_filt = df_partidos[df_partidos['rama'].str.contains(rama, case=False, na=False)]
            for _, row in partidos_filt.iterrows():
                st.write(f"**{row['ronda']}**")
                c1, cv, c2 = st.columns([2, 1, 2])
                c1.info(row['equipo1'])
                cv.markdown("<h3 style='text-align:center;'>VS</h3>", unsafe_allow_html=True)
                c2.info(row['equipo2'])
                st.success(f"Resultado: {row['resultado']}")
                st.divider()

        with t2:
            # Filtramos equipos por rama
            equipos_filt = df_equipos[df_equipos['rama'].str.contains(rama, case=False, na=False)]
            for _, row in equipos_filt.iterrows():
                with st.expander(f"🛡️ {row['nombre']}"):
                    if 'logo_url' in row and pd.notnull(row['logo_url']):
                        st.image(row['logo_url'], width=100)
                    st.write(f"**Capitán:** {row['capitán']}")
                    st.write(f"**Integrantes:** {row['jugadores']}")

except Exception as e:
    st.error("Error al cargar los datos.")
    st.write("Asegúrate de que el Excel sea público (Cualquier persona con el enlace -> Lector)")
    st.write(e)
