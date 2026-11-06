
import streamlit as st
import pandas as pd
import re
from datetime import date, datetime
from io import BytesIO

# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Tránsito Aéreo Colombiano",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

/* GENERAL */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background-color: #F5F7FC;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* TÍTULOS */

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    color: #172B55;
}

h1 {
    font-weight: 700;
}

/* ENCABEZADO */

.hero-header {
    text-align: center;
    padding: 25px 20px;
    margin-bottom: 25px;
    border-radius: 18px;
    background: linear-gradient(115deg, #073B8C, #5141A8);
    color: white;
}

.hero-header h3 {
    color: white !important;
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 12px;
}

.hero-subtitle {
    color: white !important;
    font-size: 17px;
    margin-bottom: 5px;
}

.hero-caption {
    color: #DCE6FF !important;
    font-size: 12px;
    margin-bottom: 0;
}

/* NAVBAR */

.st-key-navbar {
    background: white;
    border: 1px solid #E7EAF3;
    border-radius: 14px;
    padding: 10px 18px;
    margin-bottom: 30px;
    box-shadow: 0 3px 12px rgba(30, 50, 100, 0.04);
}

.st-key-navbar button {
    background: transparent !important;
    color: #53617C !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    min-height: 43px;
    transition: all 0.2s ease-in-out;
}

.st-key-navbar button:hover {
    background: #F0F2FF !important;
    color: #5141A8 !important;
}

.st-key-navbar button[kind="primary"] {
    color: #5141A8 !important;
    border-bottom: 3px solid #5141A8 !important;
    font-weight: 700 !important;
}

/* BOTONES GENERALES */

.stButton button {
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton button[kind="primary"] {
    background: linear-gradient(100deg, #0753B8, #6551B8);
    border: none;
}

.stButton button[kind="primary"]:hover {
    filter: brightness(1.08);
    box-shadow: 0 4px 12px rgba(65, 70, 170, 0.2);
}

/* TARJETAS */

.info-card, .news-card {
    background: white;
    border: 1px solid #E5EAF5;
    border-radius: 16px;
    padding: 23px;
    min-height: 190px;
    transition: 0.2s ease;
    margin-bottom: 12px;
}

.info-card:hover, .news-card:hover {
    transform: translateY(-4px);
    border-color: #8C83D8;
    box-shadow: 0 8px 20px rgba(40, 50, 100, 0.08);
}

.info-card h3, .news-card h3 {
    color: #253B72 !important;
    font-size: 18px;
}

.info-card p, .news-card p {
    color: #65718A !important;
    font-size: 14px;
    line-height: 1.6;
}

.news-label {
    color: #6554B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}

/* PORTADA */

.welcome-banner {
    background: linear-gradient(115deg, #073B8C, #5141A8);
    color: white;
    padding: 48px 42px;
    border-radius: 20px;
    margin-bottom: 35px;
}

.welcome-banner h1 {
    color: white !important;
    font-size: 39px;
    font-weight: 700;
    line-height: 1.2;
}

.welcome-banner p {
    color: #E5EBFF !important;
    font-size: 16px;
    max-width: 650px;
    line-height: 1.6;
}

.welcome-tag {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #D9E4FF;
}

/* RESULTADOS */

.result-card {
    background: white;
    border: 1px solid #E5EAF5;
    border-radius: 15px;
    padding: 22px;
    margin-top: 15px;
}

.result-title {
    color: #5141A8;
    font-size: 22px;
    font-weight: 700;
}

.status-good {
    color: #16845B;
    font-weight: 700;
}

.status-bad {
    color: #C34848;
    font-weight: 700;
}

.status-warning {
    color: #B27A17;
    font-weight: 700;
}

/* PIE DE PÁGINA */

.footer-info {
    text-align: center;
    padding: 30px;
    color: #65718A;
    margin-top: 35px;
}

.footer-info h3 {
    color: #253B72;
}

.footer-info small {
    color: #8993A9;
}

/* FORMULARIOS */

div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 9px;
}

/* SEPARADORES */

hr {
    border-color: #E5EAF5;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATOS DE EJEMPLO
# =========================================================

if "registro" not in st.session_state:

    st.session_state.registro = {

        "ABC123A": {
            "propietario": "Mariana Restrepo Gómez",
            "documento": "1039456782",
            "modelo": "AeroX One",
            "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal",
            "color": "Blanco perla",
            "licencia": "Vigente",
            "vencimiento_licencia": "15/08/2027",
            "soat": "Vigente",
            "vencimiento_soat": "20/12/2026",
            "revision": "Vigente",
            "vencimiento_revision": "10/06/2027",
            "multas": [
                {
                    "descripcion": "Circulación en zona de restricción",
                    "valor": 350000,
                    "estado": "Pendiente"
                }
            ]
        },

        "XYZ456B": {
            "propietario": "Andrés Felipe Molina",
            "documento": "1023456789",
            "modelo": "Nimbus 4",
            "fabricante": "SkyMotion",
            "categoria": "Transporte ligero",
            "color": "Azul metálico",
            "licencia": "Vigente",
            "vencimiento_licencia": "12/11/2027",
            "soat": "Vigente",
            "vencimiento_soat": "18/05/2027",
            "revision": "Vigente",
            "vencimiento_revision": "05/09/2027",
            "multas": []
        },

        "TAC789C": {
            "propietario": "Daniela Vélez Arango",
            "documento": "1002345678",
            "modelo": "AeroCity Pro",
            "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal",
            "color": "Negro espacial",
            "licencia": "Vencida",
            "vencimiento_licencia": "10/10/2026",
            "soat": "Vencido",
            "vencimiento_soat": "15/09/2026",
            "revision": "Vigente",
            "vencimiento_revision": "20/03/2027",
            "multas": [
                {
                    "descripcion": "Operación sin autorización vigente",
                    "valor": 520000,
                    "estado": "Pendiente"
                },
                {
                    "descripcion": "Exceso de velocidad aérea",
                    "valor": 250000,
                    "estado": "Pagada"
                }
            ]
        },

        "DEF321D": {
            "propietario": "Sebastián Ospina López",
            "documento": "985678432",
            "modelo": "Falcon Air",
            "fabricante": "Future Mobility",
            "categoria": "Transporte ejecutivo",
            "color": "Gris titanio",
            "licencia": "Vigente",
            "vencimiento_licencia": "01/12/2027",
            "soat": "Próximo a vencer",
            "vencimiento_soat": "20/11/2026",
            "revision": "Vencida",
            "vencimiento_revision": "01/10/2026",
            "multas": []
        },

        "GHI654E": {
            "propietario": "Valentina Cárdenas Ruiz",
            "documento": "1012345678",
            "modelo": "Cloud X",
            "fabricante": "SkyMotion",
            "categoria": "Movilidad personal",
            "color": "Púrpura aurora",
            "licencia": "Vigente",
            "vencimiento_licencia": "30/07/2027",
            "soat": "Vigente",
            "vencimiento_soat": "15/04/2027",
            "revision": "Vigente",
            "vencimiento_revision": "10/02/2027",
            "multas": [
                {
                    "descripcion": "Estacionamiento en zona no autorizada",
                    "valor": 180000,
                    "estado": "Pendiente"
                }
            ]
        }
    }


if "pagina" not in st.session_state:
    st.session_state.pagina = "Inicio"

if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = None

if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = []

if "pagos" not in st.session_state:
    st.session_state.pagos = []


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def dinero(valor):
    return f"${valor:,.0f}".replace(",", ".")


def estado_color(estado):
    estado = estado.lower()

    if estado in ["vigente", "pagada"]:
        return "status-good"

    if estado in ["próximo a vencer", "pendiente"]:
        return "status-warning"

    return "status-bad"


def consultar_placa(placa):
    placa = placa.upper().strip()

    if not re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", placa):
        return None

    return st.session_state.registro.get(placa)


def total_pendiente(vehiculo):
    return sum(
        multa["valor"]
        for multa in vehiculo["multas"]
        if multa["estado"] == "Pendiente"
    )


# =========================================================
# ENCABEZADO
# =========================================================

st.markdown("""
<div class="hero-header">
    <h3>✈️ TRÁNSITO AÉREO COLOMBIANO</h3>
    <p class="hero-subtitle">Movilidad aérea para un nuevo futuro.</p>
    <p class="hero-caption">
        Portal ciudadano · Proyecto de futuros imaginados · 2026
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# NAVEGACIÓN
# =========================================================

paginas = [
    "Inicio",
    "Servicios",
    "Registro nacional",
    "Multas",
    "Regulación",
    "Noticias"
]

with st.container(key="navbar"):

    columnas = st.columns(len(paginas))

    for columna, pagina_nombre in zip(columnas, paginas):

        with columna:

            if st.button(
                pagina_nombre,
                key=f"nav_{pagina_nombre}",
                type=(
                    "primary"
                    if st.session_state.pagina == pagina_nombre
                    else "secondary"
                ),
                use_container_width=True
            ):
                st.session_state.pagina = pagina_nombre
                st.session_state.mostrar_resultado = None
                st.rerun()


pagina = st.session_state.pagina


# =========================================================
# INICIO
# =========================================================

if pagina == "Inicio":

    st.markdown("""
    <div class="welcome-banner">
        <span class="welcome-tag">PORTAL OFICIAL · 2026</span>
        <h1>El futuro de la movilidad<br>también está en el aire.</h1>
        <p>
            Consulta información, conoce las normas y realiza tus trámites
            relacionados con la movilidad aérea en Colombia.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ¿Qué puedes hacer en el portal?")

    st.write(
        "Accede a los servicios del sistema nacional de tránsito aéreo."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>✈️ Licencias aéreas</h3>
            <p>
                Consulta los requisitos y realiza la renovación
                de tu licencia de operación aérea.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>📋 Registro nacional</h3>
            <p>
                Consulta los vehículos aéreos registrados en Colombia
                mediante su placa de identificación.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>⚠️ Comparendos</h3>
            <p>
                Revisa tus infracciones, consulta los valores pendientes
                y gestiona tus pagos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Actualidad del tránsito aéreo")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="news-card">
            <span class="news-label">REGULACIÓN</span>
            <h3>Conoce el CRTEC</h3>
            <p>
                Consulta el Código de Regulación de Tecnología y conoce
                las disposiciones para operar vehículos aéreos en Colombia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="news-card">
            <span class="news-label">MOVILIDAD</span>
            <h3>Consulta el pico y placa aéreo</h3>
            <p>
                Infórmate sobre las restricciones de circulación aérea
                y las fechas establecidas para cada categoría de vehículo.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class="footer-info">
        <h3>Tránsito Aéreo Colombiano</h3>
        <p>
            Construyendo una movilidad aérea segura,
            organizada y sostenible.
        </p>
        <small>
            Portal ciudadano · Proyecto de futuros imaginados · 2026
        </small>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SERVICIOS
# =========================================================

elif pagina == "Servicios":

    st.title("Servicios ciudadanos")
    st.write(
        "Realiza tus trámites relacionados con la movilidad aérea."
    )

    st.markdown("### Renovación de licencia aérea")

    st.info(
        "Solicita la renovación de la licencia que autoriza "
        "la operación de tu vehículo aéreo."
    )

    with st.form("form_renovacion"):

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input(
                "Nombre completo",
                placeholder="Ej. Mariana Restrepo Gómez"
            )

            documento = st.text_input(
                "Número de documento"
            )

        with col2:
            placa = st.text_input(
                "Placa del vehículo",
                placeholder="ABC123A",
                max_chars=7
            )

            correo = st.text_input(
                "Correo electrónico"
            )

        motivo = st.selectbox(
            "Motivo de la solicitud",
            [
                "Renovación por vencimiento",
                "Actualización de datos",
                "Reposición de licencia",
                "Otro"
            ]
        )

        fecha = st.date_input(
            "Fecha de solicitud",
            value=date.today()
        )

        aceptar = st.checkbox(
            "Declaro que la información suministrada es correcta."
        )

        enviar = st.form_submit_button(
            "Enviar solicitud",
            use_container_width=True
        )

        if enviar:

            if not nombre or not documento or not placa or not correo:
                st.error("Completa todos los campos para continuar.")

            elif not re.fullmatch(
                r"[A-Z]{3}[0-9]{3}[A-Z]",
                placa.upper().strip()
            ):
                st.error("La placa debe tener el formato ABC123A.")

            elif not aceptar:
                st.warning("Debes aceptar la declaración para continuar.")

            else:

                solicitud = {
                    "nombre": nombre,
                    "documento": documento,
                    "placa": placa.upper().strip(),
                    "correo": correo,
                    "motivo": motivo,
                    "fecha": str(fecha),
                    "radicado": f"TAC-{len(st.session_state.solicitudes) + 1001}"
                }

                st.session_state.solicitudes.append(solicitud)

                st.success("¡Solicitud registrada correctamente!")

                st.write(
                    f"**Número de radicado:** {solicitud['radicado']}"
                )

    st.markdown("---")
    st.markdown("### Otros trámites disponibles")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>📄 Certificado de registro</h3>
            <p>
                Consulta la información de registro de un vehículo aéreo
                y sus documentos asociados.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🔄 Actualización de propietario</h3>
            <p>
                Consulta el procedimiento para actualizar la información
                del titular de un vehículo aéreo.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# REGISTRO NACIONAL
# =========================================================

elif pagina == "Registro nacional":

    st.title("Registro Nacional de Vehículos Aéreos")

    st.write(
        "Consulta la información de los vehículos aéreos "
        "registrados en el territorio colombiano."
    )

    st.markdown("### Consulta por placa")

    placa_busqueda = st.text_input(
        "Ingresa la placa del vehículo",
        placeholder="Ej. ABC123A",
        max_chars=7,
        key="buscador_registro"
    ).upper().strip()

    if st.button(
        "Consultar vehículo",
        type="primary",
        use_container_width=True
    ):

        if not re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", placa_busqueda):

            st.session_state.mostrar_resultado = None
            st.error("La placa debe tener el formato ABC123A.")

        elif placa_busqueda in st.session_state.registro:

            st.session_state.mostrar_resultado = placa_busqueda

        else:

            st.session_state.mostrar_resultado = None
            st.error("No se encontró ningún vehículo con esa placa.")

    placa_resultado = st.session_state.mostrar_resultado

    if placa_resultado:

        vehiculo = st.session_state.registro[placa_resultado]

        st.markdown("---")

        st.markdown(
            f'<div class="result-title">✈️ Vehículo {placa_resultado}</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Información del vehículo")

            st.write(f"**Modelo:** {vehiculo['modelo']}")
            st.write(f"**Fabricante:** {vehiculo['fabricante']}")
            st.write(f"**Categoría:** {vehiculo['categoria']}")
            st.write(f"**Color:** {vehiculo['color']}")

        with col2:

            st.markdown("### Propietario")

            st.write(f"**Nombre:** {vehiculo['propietario']}")
            st.write(f"**Documento:** {vehiculo['documento']}")

        st.markdown("---")
        st.markdown("### Estado de documentación")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Licencia", vehiculo["licencia"])
            st.caption(
                f"Vencimiento: {vehiculo['vencimiento_licencia']}"
            )

        with col2:
            st.metric("SOAT", vehiculo["soat"])
            st.caption(
                f"Vencimiento: {vehiculo['vencimiento_soat']}"
            )

        with col3:
            st.metric("Revisión técnica", vehiculo["revision"])
            st.caption(
                f"Vencimiento: {vehiculo['vencimiento_revision']}"
            )

        st.markdown("---")
        st.markdown("### Historial de comparendos")

        if vehiculo["multas"]:

            for indice, multa in enumerate(vehiculo["multas"]):

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(multa["descripcion"])

                with col2:
                    st.write(dinero(multa["valor"]))

                with col3:
                    st.write(multa["estado"])

        else:

            st.success("Este vehículo no registra comparendos.")

        st.markdown("---")

        pendiente = total_pendiente(vehiculo)

        st.metric(
            "Total de comparendos pendientes",
            dinero(pendiente)
        )

    st.markdown("---")
    st.markdown("### Vehículos registrados en el sistema")

    busqueda_tabla = st.text_input(
        "Filtrar por placa o propietario",
        placeholder="Escribe para filtrar..."
    ).lower()

    filas = []

    for placa, vehiculo in st.session_state.registro.items():

        if (
            busqueda_tabla in placa.lower()
            or busqueda_tabla in vehiculo["propietario"].lower()
        ):

            filas.append({
                "Placa": placa,
                "Propietario": vehiculo["propietario"],
                "Modelo": vehiculo["modelo"],
                "Categoría": vehiculo["categoria"],
                "Licencia": vehiculo["licencia"]
            })

    if filas:
        st.dataframe(
            pd.DataFrame(filas),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No se encontraron vehículos.")


# =========================================================
# MULTAS
# =========================================================

elif pagina == "Multas":

    st.title("Comparendos y sanciones")

    st.write(
        "Consulta las infracciones asociadas a un vehículo aéreo "
        "y revisa los valores pendientes de pago."
    )

    placa_multa = st.text_input(
        "Ingresa la placa del vehículo",
        placeholder="Ej. ABC123A",
        max_chars=7,
        key="buscador_multas"
    ).upper().strip()

    if st.button(
        "Consultar comparendos",
        type="primary",
        use_container_width=True
    ):

        vehiculo = consultar_placa(placa_multa)

        if vehiculo is None:

            st.session_state.mostrar_resultado = None
            st.error("Placa inválida o vehículo no registrado.")

        else:

            st.session_state.mostrar_resultado = placa_multa

    placa_resultado = st.session_state.mostrar_resultado

    if placa_resultado and placa_resultado in st.session_state.registro:

        vehiculo = st.session_state.registro[placa_resultado]

        st.markdown("---")

        st.markdown(f"## Comparendos de {placa_resultado}")

        st.write(
            f"**Propietario:** {vehiculo['propietario']}"
        )

        if vehiculo["multas"]:

            for indice, multa in enumerate(vehiculo["multas"]):

                with st.container(border=True):

                    col1, col2 = st.columns([3, 1])

                    with col1:

                        st.markdown(
                            f"**{multa['descripcion']}**"
                        )

                        st.write(
                            f"Estado: {multa['estado']}"
                        )

                    with col2:

                        st.markdown(
                            f"### {dinero(multa['valor'])}"
                        )

                    if multa["estado"] == "Pendiente":

                        if st.button(
                            "Pagar comparendo",
                            key=f"pagar_{placa_resultado}_{indice}",
                            type="primary"
                        ):

                            multa["estado"] = "Pagada"

                            st.session_state.pagos.append({
                                "placa": placa_resultado,
                                "descripcion": multa["descripcion"],
                                "valor": multa["valor"],
                                "fecha": str(date.today())
                            })

                            st.success(
                                "Pago simulado realizado correctamente."
                            )

                            st.rerun()

                    else:

                        st.success("Comparendo pagado")

            st.markdown("---")

            st.metric(
                "Total pendiente",
                dinero(total_pendiente(vehiculo))
            )

        else:

            st.success(
                "Este vehículo no tiene comparendos registrados."
            )

    st.markdown("---")
    st.markdown("### Historial de pagos simulados")

    if st.session_state.pagos:

        st.dataframe(
            pd.DataFrame(st.session_state.pagos),
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Todavía no hay pagos registrados en esta sesión.")


# =========================================================
# REGULACIÓN
# =========================================================

elif pagina == "Regulación":

    st.title("Regulación del tránsito aéreo")

    st.write(
        "Consulta las disposiciones que organizan la movilidad "
        "de vehículos aéreos en Colombia."
    )

    st.markdown("## Código de Regulación de Tecnología")
    st.markdown("### CRTEC")

    st.info(
        "Documento de referencia del proyecto de futuros imaginados. "
        "Su contenido es una propuesta ficticia."
    )

    st.markdown("""
    ### Capítulo I. Disposiciones generales

    El Código de Regulación de Tecnología y Tránsito Aéreo (CRTEC)
    establece los lineamientos para la circulación, operación,
    identificación y control de vehículos aéreos en el territorio
    colombiano.

    ### Capítulo II. Registro e identificación

    - Todo vehículo aéreo deberá contar con una placa única.
    - La placa estará compuesta por tres letras, tres números y una letra.
    - Todo vehículo deberá estar asociado a un propietario registrado.
    - Los vehículos deberán mantener su documentación vigente.

    ### Capítulo III. Seguridad y operación

    - Los vehículos deberán respetar las alturas de operación establecidas.
    - Se deberá mantener una distancia mínima de seguridad.
    - Las operaciones deberán realizarse en corredores autorizados.
    - Los conductores deberán contar con licencia vigente.

    ### Capítulo IV. Zonas de circulación

    La circulación aérea estará organizada en zonas autorizadas,
    restringidas y prohibidas.

    ### Capítulo V. Infracciones

    El incumplimiento de las disposiciones podrá generar comparendos,
    sanciones económicas y suspensión de la licencia.
    """)

    documento_crtec = """
CÓDIGO DE REGULACIÓN DE TECNOLOGÍA Y TRÁNSITO AÉREO
CRTEC - COLOMBIA 2026

CAPÍTULO I. DISPOSICIONES GENERALES

El CRTEC establece los lineamientos para la circulación,
operación, identificación y control de vehículos aéreos
en el territorio colombiano.

CAPÍTULO II. REGISTRO E IDENTIFICACIÓN

Todo vehículo aéreo deberá contar con una placa única.
La placa estará compuesta por tres letras, tres números
y una letra.

Todo vehículo deberá estar asociado a un propietario
registrado y mantener su documentación vigente.

CAPÍTULO III. SEGURIDAD Y OPERACIÓN

Los vehículos deberán respetar las alturas de operación,
las distancias mínimas de seguridad y los corredores
autorizados.

Los conductores deberán contar con licencia vigente.

CAPÍTULO IV. ZONAS DE CIRCULACIÓN

La circulación aérea estará organizada en zonas
autorizadas, restringidas y prohibidas.

CAPÍTULO V. INFRACCIONES

El incumplimiento de las disposiciones podrá generar
comparendos, sanciones económicas y suspensión
de la licencia.

Documento ficticio para proyecto académico de futuros imaginados.
"""

    st.download_button(
        "⬇️ Descargar documento CRTEC",
        data=documento_crtec,
        file_name="CRTEC_Colombia_2026.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("## Zonas de circulación aérea")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h3>🟢 Zona autorizada</h3>
            <p>
                Espacios habilitados para la circulación de vehículos
                aéreos bajo las condiciones establecidas.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h3>🟡 Zona restringida</h3>
            <p>
                Espacios donde la circulación requiere permisos
                o condiciones especiales.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h3>🔴 Zona prohibida</h3>
            <p>
                Espacios en los que no se permite la circulación
                de vehículos aéreos.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Pico y placa aéreo")

    datos_pico_placa = {
        "Día": [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ],
        "Último dígito": [
            "1 - 2",
            "3 - 4",
            "5 - 6",
            "7 - 8",
            "9 - 0",
            "Sin restricción",
            "Sin restricción"
        ],
        "Horario": [
            "6:00 a.m. - 8:00 p.m.",
            "6:00 a.m. - 8:00 p.m.",
            "6:00 a.m. - 8:00 p.m.",
            "6:00 a.m. - 8:00 p.m.",
            "6:00 a.m. - 8:00 p.m.",
            "Todo el día",
            "Todo el día"
        ]
    }

    st.dataframe(
        pd.DataFrame(datos_pico_placa),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Calendario ficticio de ejemplo para el proyecto académico."
    )


# =========================================================
# NOTICIAS
# =========================================================

elif pagina == "Noticias":

    st.title("Noticias y actualidad")

    st.write(
        "Conoce las novedades, anuncios y actualizaciones "
        "del sistema de tránsito aéreo colombiano."
    )

    noticias = [
        {
            "categoria": "REGULACIÓN",
            "titulo": "Nuevo código de circulación aérea",
            "fecha": "06 de noviembre de 2026",
            "descripcion": (
                "El sistema presenta el CRTEC, un documento que reúne "
                "las disposiciones para organizar la movilidad aérea."
            )
        },
        {
            "categoria": "MOVILIDAD",
            "titulo": "Actualización del pico y placa aéreo",
            "fecha": "03 de noviembre de 2026",
            "descripcion": (
                "Conoce la distribución semanal de circulación "
                "según el último dígito de la placa."
            )
        },
        {
            "categoria": "SERVICIOS",
            "titulo": "Renovación digital de licencias",
            "fecha": "28 de octubre de 2026",
            "descripcion": (
                "Los ciudadanos podrán gestionar solicitudes "
                "de renovación de licencia desde el portal."
            )
        },
        {
            "categoria": "SEGURIDAD",
            "titulo": "Recomendaciones para la movilidad aérea",
            "fecha": "20 de octubre de 2026",
            "descripcion": (
                "Consulta las recomendaciones para operar vehículos "
                "aéreos de manera responsable."
            )
        }
    ]

    for noticia in noticias:

        with st.container(border=True):

            st.markdown(
                f'<span class="news-label">{noticia["categoria"]}</span>',
                unsafe_allow_html=True
            )

            st.markdown(f"### {noticia['titulo']}")

            st.caption(noticia["fecha"])

            st.write(noticia["descripcion"])

            st.button(
                "Leer noticia",
                key=f"noticia_{noticia['titulo']}"
            )


# =========================================================
# PIE DE PÁGINA GENERAL
# =========================================================

st.markdown("---")

st.markdown("""
<div class="footer-info">
    <h3>✈️ Tránsito Aéreo Colombiano</h3>
    <p>Movilidad aérea para un nuevo futuro.</p>
    <small>
        Proyecto de futuros imaginados · 2026
        <br>
        Plataforma de demostración académica.
    </small>
</div>
""", unsafe_allow_html=True)
