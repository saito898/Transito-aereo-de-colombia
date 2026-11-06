import streamlit as st
import pandas as pd
import re
from datetime import date

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Tránsito Aéreo Colombiano",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# BASE DE DATOS DEMOSTRATIVA
# =====================================================

if "registro" not in st.session_state:

    st.session_state.registro = {

        "ABC123A": {
            "propietario": "Mariana Restrepo Gómez",
            "documento": "1.032.456.789",
            "modelo": "AeroX One",
            "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal",
            "color": "Blanco perla",
            "licencia": "Vigente",
            "soat": "Vigente",
            "soat_fecha": "15/08/2027",
            "revision": "Vigente",
            "revision_fecha": "20/04/2027",
            "multas": [
                {
                    "codigo": "TAC-00124",
                    "motivo": "Exceso de velocidad aérea",
                    "fecha": "12/09/2026",
                    "valor": 180000,
                    "estado": "Pendiente"
                }
            ]
        },

        "XYZ456B": {
            "propietario": "Andrés Felipe Molina",
            "documento": "1.020.345.678",
            "modelo": "Nimbus 4",
            "fabricante": "SkyMotion",
            "categoria": "Transporte liviano",
            "color": "Azul metálico",
            "licencia": "Vigente",
            "soat": "Vigente",
            "soat_fecha": "11/11/2027",
            "revision": "Vigente",
            "revision_fecha": "05/06/2027",
            "multas": []
        },

        "TAC789C": {
            "propietario": "Daniela Vélez Arango",
            "documento": "1.045.678.912",
            "modelo": "AeroCity Pro",
            "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal",
            "color": "Negro espacial",
            "licencia": "Vencida",
            "soat": "Vencido",
            "soat_fecha": "10/07/2026",
            "revision": "Vigente",
            "revision_fecha": "18/12/2026",
            "multas": [
                {
                    "codigo": "TAC-00251",
                    "motivo": "Vuelo en zona restringida",
                    "fecha": "20/10/2026",
                    "valor": 450000,
                    "estado": "Pendiente"
                },
                {
                    "codigo": "TAC-00190",
                    "motivo": "Incumplimiento de pico y placa",
                    "fecha": "03/08/2026",
                    "valor": 120000,
                    "estado": "Pagada"
                }
            ]
        },

        "DEF321D": {
            "propietario": "Sebastián Ospina López",
            "documento": "1.098.765.432",
            "modelo": "Falcon Air",
            "fabricante": "Future Mobility",
            "categoria": "Transporte ejecutivo",
            "color": "Gris titanio",
            "licencia": "Vigente",
            "soat": "Por vencer",
            "soat_fecha": "18/11/2026",
            "revision": "Vencida",
            "revision_fecha": "02/09/2026",
            "multas": []
        },

        "GHI654E": {
            "propietario": "Valentina Cárdenas Ruiz",
            "documento": "1.012.345.678",
            "modelo": "Cloud X",
            "fabricante": "SkyMotion",
            "categoria": "Movilidad personal",
            "color": "Morado aurora",
            "licencia": "Vigente",
            "soat": "Vigente",
            "soat_fecha": "01/02/2027",
            "revision": "Vigente",
            "revision_fecha": "10/01/2027",
            "multas": [
                {
                    "codigo": "TAC-00321",
                    "motivo": "Estacionamiento en corredor aéreo",
                    "fecha": "15/10/2026",
                    "valor": 90000,
                    "estado": "Pendiente"
                }
            ]
        }
    }


# =====================================================
# DATOS COMPLEMENTARIOS
# =====================================================

if "solicitudes" not in st.session_state:
    st.session_state.solicitudes = []

if "pagos" not in st.session_state:
    st.session_state.pagos = []


# =====================================================
# IDENTIDAD VISUAL
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --azul: #155EEF;
    --azul-oscuro: #102B62;
    --morado: #8057E8;
    --celeste: #DCEBFF;
    --fondo: #F5F7FC;
    --texto: #172B4D;
}

.stApp {
    background: #F5F7FC;
    color: var(--texto);
    font-family: 'DM Sans', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* NAVBAR */

.navbar-brand {
    font-family: 'Space Grotesk';
    font-weight: 700;
    font-size: 23px;
    color: #123A83;
    padding: 12px 0;
}

.navbar-sub {
    font-size: 10px;
    letter-spacing: 2px;
    color: #7585A3;
    font-weight: 700;
}

/* TEXTOS */

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #152D59 !important;
}

p {
    color: #62718D;
}

/* HERO */

.hero {
    background: linear-gradient(
        115deg,
        #124CC7 0%,
        #346FF0 50%,
        #7955D9 100%
    );
    padding: 42px;
    border-radius: 25px;
    color: white;
    margin: 18px 0 28px 0;
    position: relative;
    overflow: hidden;
}

.hero h1 {
    color: white !important;
    font-size: 42px;
    line-height: 1.12;
    margin: 10px 0;
}

.hero p {
    color: #E2EBFF;
    font-size: 16px;
    max-width: 650px;
}

.hero-label {
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 800;
    color: #C5D9FF;
}

/* TARJETAS */

.card {
    background: white;
    border: 1px solid #E8EDF6;
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 5px 20px rgba(28,55,100,.045);
    margin-bottom: 15px;
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    color: #17356D;
    margin-bottom: 7px;
}

.card-description {
    color: #7B89A3;
    font-size: 13px;
    line-height: 1.5;
}

.service-icon {
    background: linear-gradient(135deg,#E5EEFF,#F0E9FF);
    width: 52px;
    height: 52px;
    border-radius: 15px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 25px;
    margin-bottom: 15px;
}

.section-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #6D7F9F;
}

.search-card {
    background: white;
    border: 1px solid #E0E8F5;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 8px 28px rgba(28,55,100,.07);
    margin: 20px 0;
}

/* ESTADOS */

.status {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
}

.ok {
    color: #16865B;
    background: #E0F7EB;
}

.bad {
    color: #D13D55;
    background: #FFE6EA;
}

.warning {
    color: #A76A00;
    background: #FFF3D5;
}

/* PLACA */

.plate {
    background: #FFFFFF;
    border: 3px solid #253B61;
    border-radius: 12px;
    padding: 14px 25px;
    display: inline-block;
    color: #162D53;
    font-family: 'Space Grotesk';
    font-weight: 700;
    font-size: 29px;
    letter-spacing: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,.08);
}

/* MÉTRICAS */

.metric-card {
    background: white;
    border: 1px solid #E8EDF6;
    border-radius: 18px;
    padding: 20px;
    min-height: 105px;
}

.metric-card small {
    color: #8290A9;
    font-size: 12px;
}

.metric-card strong {
    display: block;
    color: #17356D;
    font-family: 'Space Grotesk';
    font-size: 27px;
    margin-top: 7px;
}

/* NOTICIAS */

.news-card {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #E8EDF6;
    margin-bottom: 12px;
}

.news-date {
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 800;
    color: #8057E8;
}

/* INPUTS */

.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stDateInput input,
.stTextArea textarea {
    background: white !important;
    color: #172B4D !important;
    border-radius: 10px !important;
    border-color: #DCE4F1 !important;
}

.stTextInput label,
.stSelectbox label,
.stDateInput label {
    color: #435575 !important;
    font-weight: 600 !important;
}

/* BOTONES */

.stButton > button,
.stDownloadButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(90deg,#155EEF,#8057E8);
    color: white;
    border: none;
    border-radius: 11px;
    min-height: 43px;
    font-weight: 700;
}

.stButton > button:hover {
    color: white;
    border: 1px solid #155EEF;
    background: #174DC4;
}

/* NAVBAR HORIZONTAL */

div[role="radiogroup"] {
    gap: 7px;
}

div[role="radiogroup"] label {
    background: white;
    border: 1px solid #E5EAF4;
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 700;
}

div[role="radiogroup"] label:has(input:checked) {
    background: #E8EEFF;
    border-color: #A9BFFF;
}

div[role="radiogroup"] label p {
    color: #29436E !important;
}

/* TABLAS */

div[data-testid="stDataFrame"] {
    border: 1px solid #E4EAF3;
    border-radius: 12px;
}

/* PIE */

.footer {
    background: #102B62;
    border-radius: 18px;
    color: white;
    padding: 25px;
    margin-top: 35px;
    text-align: center;
}

.footer p {
    color: #C5D4F1;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# FUNCIONES
# =====================================================

def hero(titulo, descripcion, etiqueta="PORTAL CIUDADANO"):

    st.markdown(f"""
    <div class="hero">
        <div class="hero-label">{etiqueta}</div>
        <h1>{titulo}</h1>
        <p>{descripcion}</p>
    </div>
    """, unsafe_allow_html=True)


def tarjeta(icono, titulo, descripcion):

    st.markdown(f"""
    <div class="card">
        <div class="service-icon">{icono}</div>
        <div class="card-title">{titulo}</div>
        <div class="card-description">{descripcion}</div>
    </div>
    """, unsafe_allow_html=True)


def indicador(titulo, valor):

    st.markdown(f"""
    <div class="metric-card">
        <small>{titulo}</small>
        <strong>{valor}</strong>
    </div>
    """, unsafe_allow_html=True)


def estado(valor):

    if valor == "Vigente" or valor == "Pagada":
        clase = "ok"
    elif valor == "Por vencer":
        clase = "warning"
    else:
        clase = "bad"

    return f'<span class="status {clase}">{valor}</span>'


def buscar_placa(placa):

    placa = placa.strip().upper()

    if not re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", placa):
        st.error(
            "Formato inválido. La placa debe tener "
            "tres letras, tres números y una letra. Ejemplo: ABC123A."
        )
        return

    if placa not in st.session_state.registro:
        st.warning(
            "No encontramos esta placa en el Registro Nacional "
            "de Vehículos Aéreos de demostración."
        )
        return

    st.session_state.placa_consultada = placa
    st.session_state.mostrar_resultado = True


def ficha_vehiculo(placa):

    datos = st.session_state.registro[placa]

    multas = datos["multas"]

    pendientes = [
        m for m in multas
        if m["estado"] == "Pendiente"
    ]

    st.markdown("---")

    st.markdown(
        f'<div class="section-label">REGISTRO NACIONAL DE VEHÍCULOS AÉREOS</div>',
        unsafe_allow_html=True
    )

    a, b = st.columns([1, 2])

    with a:

        st.markdown(
            f'<div class="plate">{placa}</div>',
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            f'<span class="tag">REGISTRO ACTIVO</span>',
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"### {datos['modelo']}"
        )

        st.caption(
            f"{datos['fabricante']} · {datos['categoria']}"
        )

    st.markdown("---")

    st.subheader("Información del propietario")

    a, b = st.columns(2)

    with a:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-description">PROPIETARIO REGISTRADO</div>
                <div class="card-title">{datos['propietario']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-description">DOCUMENTO DE IDENTIDAD</div>
                <div class="card-title">{datos['documento']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Estado de documentación")

    a, b, c = st.columns(3)

    with a:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Licencia aérea</div>
                {estado(datos['licencia'])}
            </div>
            """,
            unsafe_allow_html=True
        )

    with b:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">SOAT aéreo</div>
                {estado(datos['soat'])}
                <p class="card-description">
                    Vence: {datos['soat_fecha']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c:

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Revisión técnica</div>
                {estado(datos['revision'])}
                <p class="card-description">
                    Vence: {datos['revision_fecha']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("Historial de infracciones")

    if multas:

        for multa in multas:

            st.markdown(f"""
            <div class="card">
                <div class="card-title">
                    {multa['motivo']}
                </div>
                <div class="card-description">
                    Comparendo: {multa['codigo']} |
                    Fecha: {multa['fecha']}
                </div>
                <h3>${multa['valor']:,.0f} COP</h3>
                {estado(multa['estado'])}
            </div>
            """, unsafe_allow_html=True)

    else:

        st.success(
            "Este vehículo no registra infracciones."
        )

    total = sum(
        m["valor"] for m in pendientes
    )

    if pendientes:

        st.warning(
            f"Este vehículo tiene {len(pendientes)} "
            f"multas pendientes por ${total:,.0f} COP."
        )

    else:

        st.success(
            "El vehículo no tiene multas pendientes."
        )


# =====================================================
# NAVBAR SUPERIOR
# =====================================================

logo, espacio, acceso = st.columns([2, 2, 1])

with logo:

    st.markdown("""
    <div class="navbar-brand">
        ✈️ TAC
    </div>
    <div class="navbar-sub">
        TRÁNSITO AÉREO COLOMBIANO
    </div>
    """, unsafe_allow_html=True)

with acceso:

    st.markdown(
        "<div style='padding-top:17px;text-align:right;color:#60728F;font-size:12px'>"
        "PORTAL NACIONAL · 2026"
        "</div>",
        unsafe_allow_html=True
    )

st.write("")

pagina = st.radio(
    "Navegación",
    [
        "Inicio",
        "Servicios",
        "Registro nacional",
        "Multas",
        "Regulación",
        "Noticias"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")


# =====================================================
# INICIO
# =====================================================

if pagina == "Inicio":

    hero(
        "El cielo colombiano, conectado.",
        "Bienvenido al portal oficial de servicios de movilidad aérea. "
        "Consulta vehículos, gestiona tus trámites y conoce las reglas "
        "para circular por el espacio aéreo nacional."
    )

    # BUSCADOR PRINCIPAL

    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True
    )

    st.markdown("### 🔎 Consulta un vehículo aéreo")

    st.caption(
        "Busca cualquier vehículo registrado en Colombia "
        "mediante su placa de identificación."
    )

    with st.form("buscador_inicio"):

        col1, col2 = st.columns([4, 1])

        with col1:

            placa = st.text_input(
                "Número de placa",
                placeholder="ABC123A"
            )

        with col2:

            st.write("")
            st.write("")

            consultar = st.form_submit_button(
                "Consultar"
            )

        if consultar:
            buscar_placa(placa)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("mostrar_resultado", False):

        ficha_vehiculo(
            st.session_state.placa_consultada
        )

    st.write("")

    st.subheader("¿Qué necesitas hacer?")

    st.caption(
        "Encuentra rápidamente el servicio que estás buscando."
    )

    servicios = [
        ("📄", "Licencia aérea", "Consulta o solicita la renovación de tu licencia."),
        ("🚁", "Registro nacional", "Busca vehículos aéreos inscritos en Colombia."),
        ("🛡️", "SOAT aéreo", "Consulta la vigencia del seguro obligatorio."),
        ("💳", "Multas", "Consulta comparendos y obligaciones pendientes."),
        ("🗺️", "Zonas de vuelo", "Identifica los espacios permitidos y restringidos."),
        ("📅", "Pico y placa", "Consulta las restricciones de circulación.")
    ]

    columnas = st.columns(3)

    for i, (icono, titulo, descripcion) in enumerate(servicios):

        with columnas[i % 3]:

            tarjeta(icono, titulo, descripcion)

    st.markdown("---")

    st.subheader("Últimas noticias")

    noticias = [
        (
            "06 NOV 2026",
            "Actualización del Código CRTEC",
            "Nuevos lineamientos de identificación digital."
        ),
        (
            "02 NOV 2026",
            "Nuevos corredores de movilidad aérea",
            "Actualización de rutas habilitadas para vehículos personales."
        )
    ]

    for fecha, titulo, descripcion in noticias:

        st.markdown(f"""
        <div class="news-card">
            <div class="news-date">{fecha}</div>
            <h3>{titulo}</h3>
            <p>{descripcion}</p>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# SERVICIOS
# =====================================================

elif pagina == "Servicios":

    hero(
        "Servicios ciudadanos",
        "Todo lo que necesitas para circular por el aire.",
        "TRÁMITES Y SERVICIOS"
    )

    st.subheader("Documentación y trámites")

    with st.expander("📄 Licencia aérea", expanded=True):

        st.write(
            "Consulta la vigencia de tu licencia y realiza "
            "una solicitud de renovación."
        )

        with st.form("renovacion"):

            nombre = st.text_input("Nombre completo")
            documento = st.text_input("Documento de identidad")

            tipo = st.selectbox(
                "Tipo de solicitud",
                [
                    "Renovación de licencia",
                    "Duplicado de licencia",
                    "Actualización de datos"
                ]
            )

            enviar = st.form_submit_button(
                "Enviar solicitud"
            )

            if enviar:

                if nombre and documento:

                    st.session_state.solicitudes.append({
                        "nombre": nombre,
                        "documento": documento,
                        "tipo": tipo
                    })

                    st.success(
                        "Solicitud recibida. Radicado simulado: TAC-2026-001."
                    )

                else:

                    st.error(
                        "Completa los datos solicitados."
                    )

    with st.expander("🛡️ SOAT aéreo"):

        st.write(
            "El seguro obligatorio protege a terceros "
            "ante incidentes relacionados con la movilidad aérea."
        )

        st.info(
            "Consulta el estado del SOAT de cualquier vehículo "
            "desde el Registro Nacional."
        )

    with st.expander("🔧 Revisión técnica"):

        st.write(
            "Consulta la vigencia de las revisiones técnicas "
            "y los requisitos de seguridad de los vehículos."
        )

    with st.expander("📅 Pico y placa"):

        st.write(
            "Consulta los días y horarios de restricción "
            "según la terminación de la placa."
        )

        calendario = pd.DataFrame([
            ["Lunes", "1 y 2"],
            ["Martes", "3 y 4"],
            ["Miércoles", "5 y 6"],
            ["Jueves", "7 y 8"],
            ["Viernes", "9 y 0"],
            ["Fin de semana", "Sin restricción general"]
        ], columns=["Día", "Placas restringidas"])

        st.dataframe(
            calendario,
            use_container_width=True,
            hide_index=True
        )


# =====================================================
# REGISTRO NACIONAL
# =====================================================

elif pagina == "Registro nacional":

    hero(
        "Registro Nacional de Vehículos Aéreos",
        "Cada vehículo tiene una identidad. Encuéntrala aquí.",
        "SISTEMA NACIONAL DE REGISTRO"
    )

    st.markdown(
        '<div class="search-card">',
        unsafe_allow_html=True
    )

    st.subheader("Consultar placa aérea")

    st.caption(
        "Ingresa la placa para conocer el propietario, "
        "la documentación y el historial de infracciones."
    )

    with st.form("busqueda_registro"):

        placa = st.text_input(
            "Placa del vehículo",
            placeholder="ABC123A"
        )

        consultar = st.form_submit_button(
            "Buscar vehículo"
        )

        if consultar:
            buscar_placa(placa)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.get("mostrar_resultado", False):

        ficha_vehiculo(
            st.session_state.placa_consultada
        )

    st.markdown("---")

    st.subheader("Vehículos inscritos en Colombia")

    total = len(st.session_state.registro)

    vigentes = sum(
        1 for v in st.session_state.registro.values()
        if v["soat"] == "Vigente"
    )

    a, b = st.columns(2)

    with a:
        indicador(
            "VEHÍCULOS EN EL REGISTRO DEMO",
            total
        )

    with b:
        indicador(
            "SOAT VIGENTE",
            vigentes
        )

    st.caption(
        "Los datos de propietarios y vehículos mostrados "
        "son ficticios y pertenecen al prototipo."
    )

    for placa, datos in st.session_state.registro.items():

        st.markdown(f"""
        <div class="card">
            <div class="plate">{placa}</div>
            <div class="card-title" style="margin-top:15px">
                {datos['modelo']}
            </div>
            <div class="card-description">
                {datos['fabricante']} · {datos['categoria']}
            </div>
            <div class="card-description">
                Propietario: {datos['propietario']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "Consultar ficha " + placa,
            key="ficha_" + placa
        ):

            st.session_state.placa_consultada = placa
            st.session_state.mostrar_resultado = True
            st.rerun()


# =====================================================
# MULTAS
# =====================================================

elif pagina == "Multas":

    hero(
        "Consulta de comparendos",
        "Mantén tu historial de circulación al día.",
        "SISTEMA NACIONAL DE INFRACCIONES"
    )

    placa = st.text_input(
        "Buscar multas por placa",
        placeholder="ABC123A"
    )

    if st.button("Consultar multas"):

        placa = placa.strip().upper()

        if not re.fullmatch(r"[A-Z]{3}[0-9]{3}[A-Z]", placa):

            st.error(
                "Formato inválido. Ejemplo: ABC123A."
            )

        elif placa not in st.session_state.registro:

            st.warning(
                "No encontramos esta placa."
            )

        else:

            st.session_state.placa_multas = placa

    if st.session_state.get("placa_multas"):

        placa = st.session_state.placa_multas

        datos = st.session_state.registro[placa]

        st.markdown("---")

        st.subheader(
            f"Comparendos de {placa}"
        )

        pendientes = [
            m for m in datos["multas"]
            if m["estado"] == "Pendiente"
        ]

        st.markdown(
            f"**Propietario:** {datos['propietario']}"
        )

        if not datos["multas"]:

            st.success(
                "Este vehículo no registra multas."
            )

        else:

            for i, multa in enumerate(datos["multas"]):

                st.markdown(f"""
                <div class="card">
                    <div class="card-title">{multa['motivo']}</div>
                    <div class="card-description">
                        {multa['codigo']} · {multa['fecha']}
                    </div>
                    <h3>${multa['valor']:,.0f} COP</h3>
                    {estado(multa['estado'])}
                </div>
                """, unsafe_allow_html=True)

                if multa["estado"] == "Pendiente":

                    if st.button(
                        "Pagar comparendo " + multa["codigo"],
                        key="pagar_" + multa["codigo"]
                    ):

                        multa["estado"] = "Pagada"

                        st.success(
                            "Pago simulado realizado correctamente."
                        )

                        st.rerun()

            total = sum(
                m["valor"]
                for m in pendientes
            )

            st.warning(
                f"Total pendiente: ${total:,.0f} COP"
            )


# =====================================================
# REGULACIÓN
# =====================================================

elif pagina == "Regulación":

    hero(
        "Regulación del espacio aéreo",
        "Conoce las reglas para compartir el cielo colombiano.",
        "NORMATIVA Y SEGURIDAD"
    )

    st.markdown("""
    <div class="card">
        <div class="section-label">DOCUMENTO NACIONAL</div>
        <h2>CRTEC</h2>
        <h3>Código de Regulación de Tecnología y Espacio Aéreo</h3>
        <p>
        Consulta las disposiciones que regulan la circulación,
        identificación y operación de vehículos aéreos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🟢 Zonas permitidas"):

        st.write(
            "Espacios habilitados para la circulación "
            "de vehículos aéreos bajo condiciones generales."
        )

    with st.expander("🟡 Zonas condicionadas"):

        st.write(
            "Espacios que requieren permisos especiales, "
            "horarios autorizados o restricciones de altura."
        )

    with st.expander("🔴 Zonas prohibidas"):

        st.write(
            "Aeropuertos, hospitales, infraestructura crítica "
            "y zonas de emergencia."
        )

    with st.expander("📋 Requisitos de circulación"):

        st.write("""
        - Licencia aérea vigente.
        - Placa registrada.
        - SOAT vigente.
        - Revisión técnica.
        - Identificación digital.
        - Cumplimiento del pico y placa.
        """)

    with st.expander("⚖️ Infracciones"):

        st.write("""
        - Circular en zonas prohibidas.
        - Operar sin documentación.
        - Incumplir el pico y placa.
        - Exceder los límites de altura.
        - Desactivar sistemas de seguridad.
        """)

    CRTEC = """
    CRTEC - CODIGO DE REGULACION DE TECNOLOGIA
    Y ESPACIO AEREO

    TRANSITO AEREO COLOMBIANO

    DOCUMENTO DEMOSTRATIVO

    1. ZONAS PERMITIDAS
    Espacios habilitados para la movilidad aérea.

    2. ZONAS CONDICIONADAS
    Requieren autorización especial.

    3. ZONAS PROHIBIDAS
    Aeropuertos, hospitales e infraestructura crítica.

    4. DOCUMENTACION
    Licencia, placa, SOAT y revisión técnica vigentes.

    5. RESPONSABILIDAD
    El operador debe respetar las restricciones de circulación.

    Este documento es ficticio y académico.
    """

    st.download_button(
        "⬇ Descargar CRTEC",
        data=CRTEC,
        file_name="CRTEC_Tránsito_Aéreo_Colombiano.txt"
    )

    st.markdown("---")

    st.subheader("Calendario de pico y placa")

    calendario = pd.DataFrame([
        ["Lunes", "1 y 2", "06:00 - 09:00 / 16:00 - 19:00"],
        ["Martes", "3 y 4", "06:00 - 09:00 / 16:00 - 19:00"],
        ["Miércoles", "5 y 6", "06:00 - 09:00 / 16:00 - 19:00"],
        ["Jueves", "7 y 8", "06:00 - 09:00 / 16:00 - 19:00"],
        ["Viernes", "9 y 0", "06:00 - 09:00 / 16:00 - 19:00"]
    ], columns=["Día", "Terminaciones", "Horario"])

    st.dataframe(
        calendario,
        use_container_width=True,
        hide_index=True
    )


# =====================================================
# NOTICIAS
# =====================================================

elif pagina == "Noticias":

    hero(
        "Noticias y actualidad",
        "Lo que sucede en el espacio aéreo colombiano.",
        "SALA DE PRENSA TAC"
    )

    noticias = [
        (
            "06 NOVIEMBRE 2026",
            "Nueva actualización del CRTEC",
            "Se anuncian nuevas disposiciones sobre identificación "
            "digital de vehículos aéreos."
        ),
        (
            "02 NOVIEMBRE 2026",
            "Habilitación de nuevos corredores aéreos",
            "Se amplían los corredores de movilidad personal "
            "en diferentes regiones del país."
        ),
        (
            "28 OCTUBRE 2026",
            "Calendario de pico y placa",
            "Conoce las nuevas restricciones de circulación "
            "para el mes de noviembre."
        ),
        (
            "20 OCTUBRE 2026",
            "Campaña nacional de seguridad aérea",
            "El TAC presenta una iniciativa para promover "
            "la movilidad aérea responsable."
        )
    ]

    for fecha, titulo, descripcion in noticias:

        st.markdown(f"""
        <div class="news-card">
            <div class="news-date">{fecha}</div>
            <h3>{titulo}</h3>
            <p>{descripcion}</p>
            <span class="status ok">COMUNICADO TAC</span>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">

    <h3 style="color:white!important">
        ✈️ TRÁNSITO AÉREO COLOMBIANO
    </h3>

    <p>
        Movilidad aérea para un nuevo futuro.
    </p>

    <p>
        Portal ciudadano · Proyecto de futuros imaginados · 2026
    </p>

</div>
""", unsafe_allow_html=True)

st.caption(
    "Prototipo académico. Los registros, propietarios, "
    "normativas, multas y transacciones son ficticios."
)
