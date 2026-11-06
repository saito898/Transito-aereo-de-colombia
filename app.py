import streamlit as st
import pandas as pd
from datetime import date

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Tránsito Aéreo Colombiano | TAC",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# IDENTIDAD VISUAL
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #07152f, #0b1e42, #17143e);
    color: #f4f7ff;
    font-family: 'DM Sans', sans-serif;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08152e, #11153e);
    border-right: 1px solid #294477;
}

section[data-testid="stSidebar"] * {
    color: #e9efff !important;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: white !important;
}

.hero {
    padding: 30px;
    border: 1px solid #294477;
    border-radius: 22px;
    background: linear-gradient(
        110deg,
        rgba(23,107,255,.25),
        rgba(128,87,255,.22)
    );
    margin-bottom: 22px;
}

.hero h1 {
    font-size: 38px;
    margin: 8px 0;
}

.hero p {
    color: #c4d2ef;
}

.eyebrow {
    color: #70d5ff;
    letter-spacing: 2px;
    font-size: 11px;
    font-weight: 700;
}

.metric {
    background: linear-gradient(145deg, #122b55, #171c4c);
    border: 1px solid #2a4779;
    padding: 20px;
    border-radius: 17px;
    min-height: 110px;
}

.metric small {
    color: #9eb5dc;
}

.metric strong {
    display: block;
    font-size: 27px;
    margin-top: 8px;
    color: white;
}

.metric em {
    color: #75d6ff;
    font-style: normal;
    font-size: 12px;
}

.panel {
    background: rgba(17,37,76,.85);
    border: 1px solid #2b4776;
    border-radius: 17px;
    padding: 20px;
}

.notice {
    border-left: 4px solid #8a69ff;
    background: #171d49;
    padding: 14px;
    border-radius: 8px;
    margin: 10px 0;
    color: #dce5ff;
}

.tag {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    background: #173e70;
    color: #8fe0ff;
}

.stButton > button,
.stDownloadButton > button {
    background: linear-gradient(90deg, #176bff, #8057ff);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

.stButton > button:hover {
    border: 1px solid #9de5ff;
    color: white;
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"],
.stDateInput input {
    background: #0b1b3a !important;
    color: white !important;
    border-color: #385789 !important;
}

hr {
    border-color: #294477;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# DATOS DE DEMOSTRACIÓN
# =====================================================

if "multas" not in st.session_state:

    st.session_state.multas = [
        {
            "Código": "TAC-20481",
            "Fecha": "12/10/2026",
            "Infracción": "Vuelo en horario restringido",
            "Placa": "AVN-204",
            "Valor": 180000,
            "Estado": "Pendiente"
        },
        {
            "Código": "TAC-19832",
            "Fecha": "03/08/2026",
            "Infracción": "Exceso de altura autorizada",
            "Placa": "AVN-204",
            "Valor": 250000,
            "Estado": "Pendiente"
        },
        {
            "Código": "TAC-17604",
            "Fecha": "19/05/2026",
            "Infracción": "Estacionamiento en corredor aéreo",
            "Placa": "SKY-811",
            "Valor": 120000,
            "Estado": "Pagada"
        }
    ]


if "vehiculos" not in st.session_state:

    st.session_state.vehiculos = [
        {
            "Placa": "AVN-204",
            "Modelo": "AeroX One",
            "Tipo": "Vehículo personal",
            "SOAT": "Vigente",
            "Vencimiento": "18/02/2027"
        },
        {
            "Placa": "SKY-811",
            "Modelo": "Nimbus 4",
            "Tipo": "Transporte liviano",
            "SOAT": "Por vencer",
            "Vencimiento": "20/11/2026"
        }
    ]


if "solicitud" not in st.session_state:
    st.session_state.solicitud = False


# =====================================================
# CRTEC
# =====================================================

CRTEC = """
# CRTEC
## Código de Regulación de Tecnología y Espacio Aéreo
### Tránsito Aéreo Colombiano

Versión 1.0 - 2026

DOCUMENTO DEMOSTRATIVO DE FUTUROS IMAGINADOS.
No corresponde a una normativa gubernamental real.

## 1. Clasificación de zonas aéreas

ZONA VERDE - VUELO PERMITIDO
Corredores habilitados para tránsito personal y recreativo.

ZONA AMARILLA - VUELO CONDICIONADO
Requiere autorización previa y cumplimiento de horarios.

ZONA ROJA - VUELO PROHIBIDO
Aeropuertos, hospitales, infraestructura crítica,
edificios gubernamentales y zonas de emergencia.

## 2. Requisitos de los vehículos

- Placa aérea visible.
- Sistema de geolocalización activo.
- SOAT aéreo vigente.
- Revisión técnica anual.
- Sistema de prevención de colisiones.

## 3. Requisitos del conductor

- Licencia aérea vigente.
- Identificación digital.
- Cumplimiento de corredores y alturas.
- Respeto por las restricciones de circulación.

## 4. Infracciones

- Volar en zonas prohibidas.
- Ignorar el pico y placa aéreo.
- Operar sin licencia o SOAT.
- Superar los límites de altura.
- Desactivar sistemas de seguridad.

## 5. Responsabilidad

El operador debe verificar las condiciones
meteorológicas, restricciones temporales y
estado técnico del vehículo antes de cada vuelo.
"""


# =====================================================
# FUNCIONES DE DISEÑO
# =====================================================

def encabezado(seccion, titulo, descripcion):

    st.markdown(f"""
    <div class="hero">
        <div class="eyebrow">{seccion}</div>
        <h1>{titulo}</h1>
        <p>{descripcion}</p>
    </div>
    """, unsafe_allow_html=True)


def indicador(titulo, valor, detalle):

    st.markdown(f"""
    <div class="metric">
        <small>{titulo}</small>
        <strong>{valor}</strong>
        <em>{detalle}</em>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# MENÚ LATERAL
# =====================================================

st.sidebar.markdown("# ✈️ TAC")

st.sidebar.caption(
    "TRÁNSITO AÉREO COLOMBIANO"
)

st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "PORTAL CIUDADANO",
    [
        "Inicio",
        "Mi licencia aérea",
        "Vehículos y SOAT",
        "Multas y pagos",
        "Mapa de zonas aéreas",
        "Pico y placa",
        "CRTEC",
        "Noticias"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Atención al ciudadano")

st.sidebar.caption(
    "Centro de atención TAC"
)

st.sidebar.caption(
    "Línea nacional: 01 8000 TAC"
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    '<span class="tag">SISTEMA OPERATIVO · DEMO</span>',
    unsafe_allow_html=True
)


# =====================================================
# 1. INICIO
# =====================================================

if pagina == "Inicio":

    encabezado(
        "PORTAL ÚNICO DEL CIUDADANO",
        "El cielo también tiene reglas.",
        "Gestiona tu movilidad aérea desde un solo lugar."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        indicador(
            "LICENCIA AÉREA",
            "Vigente",
            "Vence el 24/03/2027"
        )

    with c2:
        indicador(
            "SOAT AÉREO",
            "1 por vencer",
            "Consulta tus vehículos"
        )

    with c3:
        indicador(
            "MULTAS PENDIENTES",
            "2",
            "Total: $430.000 COP"
        )

    with c4:
        indicador(
            "VEHÍCULOS",
            "2 registrados",
            "Identificación activa"
        )

    st.write("")

    izquierda, derecha = st.columns([1.4, 1])

    with izquierda:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.subheader("Centro de notificaciones")

        st.markdown("""
        <div class="notice">
        ⚠️ <b>SOAT próximo a vencer:</b>
        El vehículo SKY-811 requiere renovación.
        </div>

        <div class="notice">
        📅 <b>Pico y placa:</b>
        Consulta las restricciones antes de despegar.
        </div>

        <div class="notice">
        🛰️ <b>Actualización CRTEC:</b>
        Se publicó una nueva versión del código.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with derecha:

        st.markdown(
            '<div class="panel">',
            unsafe_allow_html=True
        )

        st.subheader("Accesos rápidos")

        st.write("📄 Renovar licencia aérea")
        st.write("🚁 Consultar vehículos")
        st.write("💳 Pagar comparendos")
        st.write("🗺️ Consultar zonas de vuelo")
        st.write("📘 Descargar CRTEC")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    st.subheader("Estado de documentación")

    st.progress(
        0.82,
        text="Documentación del ciudadano: 82% completa"
    )


# =====================================================
# 2. LICENCIA AÉREA
# =====================================================

elif pagina == "Mi licencia aérea":

    encabezado(
        "GESTIÓN DOCUMENTAL",
        "Mi licencia aérea",
        "Consulta y renueva tu autorización de conducción aérea."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        indicador(
            "NÚMERO DE LICENCIA",
            "LA-0928-441",
            "Categoría personal"
        )

    with c2:
        indicador(
            "ESTADO",
            "Vigente",
            "Sin restricciones"
        )

    with c3:
        indicador(
            "VENCIMIENTO",
            "24 MAR 2027",
            "Renovación disponible"
        )

    st.subheader("Datos del titular")

    a, b = st.columns(2)

    with a:

        st.text_input(
            "Nombre completo",
            "Ciudadano de prueba",
            disabled=True
        )

        st.text_input(
            "Documento de identidad",
            "1.000.000.000",
            disabled=True
        )

    with b:

        st.text_input(
            "Categoría autorizada",
            "A2 - Movilidad personal",
            disabled=True
        )

        st.text_input(
            "Organismo expedidor",
            "Tránsito Aéreo Colombiano",
            disabled=True
        )

    st.markdown("---")

    st.subheader("Solicitud de renovación")

    with st.form("renovacion"):

        st.info(
            "Completa la solicitud para renovar tu licencia aérea."
        )

        confirmacion = st.checkbox(
            "Confirmo que mis datos están actualizados."
        )

        enviar = st.form_submit_button(
            "Solicitar renovación"
        )

        if enviar:

            if confirmacion:

                st.session_state.solicitud = True

                st.success(
                    "Solicitud registrada correctamente. "
                    "Radicado: TAC-REN-2026-00841"
                )

            else:

                st.warning(
                    "Debes confirmar tus datos."
                )

    if st.session_state.solicitud:

        st.success(
            "Estado de solicitud: RECIBIDA - EN VALIDACIÓN"
        )


# =====================================================
# 3. VEHÍCULOS Y SOAT
# =====================================================

elif pagina == "Vehículos y SOAT":

    encabezado(
        "REGISTRO AERONÁUTICO",
        "Mis vehículos y SOAT",
        "Administra las placas y seguros de tus vehículos."
    )

    df = pd.DataFrame(
        st.session_state.vehiculos
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Registrar nuevo vehículo")

    with st.form("nuevo_vehiculo"):

        a, b = st.columns(2)

        with a:

            placa = st.text_input(
                "Placa aérea",
                placeholder="Ej. AER-520"
            )

            tipo = st.selectbox(
                "Tipo de vehículo",
                [
                    "Vehículo personal",
                    "Transporte liviano",
                    "Carga",
                    "Emergencias"
                ]
            )

        with b:

            modelo = st.text_input(
                "Modelo",
                placeholder="Ej. AeroX Pro"
            )

            seguro = st.selectbox(
                "Estado del SOAT",
                [
                    "Vigente",
                    "Por vencer",
                    "Pendiente"
                ]
            )

        vencimiento = st.date_input(
            "Vencimiento del SOAT",
            value=date(2027, 1, 31)
        )

        registrar = st.form_submit_button(
            "Registrar vehículo"
        )

        if registrar:

            if not placa.strip() or not modelo.strip():

                st.error(
                    "Completa todos los campos."
                )

            elif any(
                v["Placa"] == placa.strip().upper()
                for v in st.session_state.vehiculos
            ):

                st.error(
                    "Esta placa ya está registrada."
                )

            else:

                st.session_state.vehiculos.append({
                    "Placa": placa.strip().upper(),
                    "Modelo": modelo,
                    "Tipo": tipo,
                    "SOAT": seguro,
                    "Vencimiento": vencimiento.strftime("%d/%m/%Y")
                })

                st.success(
                    "Vehículo registrado correctamente."
                )

                st.rerun()

    st.markdown("---")

    st.subheader("Consultar SOAT")

    placas = [
        v["Placa"]
        for v in st.session_state.vehiculos
    ]

    seleccion = st.selectbox(
        "Selecciona una placa",
        placas
    )

    vehiculo = next(
        v for v in st.session_state.vehiculos
        if v["Placa"] == seleccion
    )

    st.info(
        f"Modelo: {vehiculo['Modelo']} | "
        f"SOAT: {vehiculo['SOAT']} | "
        f"Vencimiento: {vehiculo['Vencimiento']}"
    )

    if st.button("Simular renovación del SOAT"):

        st.success(
            f"Solicitud simulada para {seleccion}. "
            "No se ha realizado ningún cobro."
        )


# =====================================================
# 4. MULTAS Y PAGOS
# =====================================================

elif pagina == "Multas y pagos":

    encabezado(
        "SISTEMA DE INFRACCIONES",
        "Multas y comparendos",
        "Consulta tus infracciones y gestiona los pagos."
    )

    multas = pd.DataFrame(
        st.session_state.multas
    )

    pendiente = sum(
        m["Valor"]
        for m in st.session_state.multas
        if m["Estado"] == "Pendiente"
    )

    a, b = st.columns(2)

    with a:

        indicador(
            "SALDO PENDIENTE",
            f"${pendiente:,.0f}",
            "Pesos colombianos"
        )

    with b:

        indicador(
            "INFRACCIONES",
            str(len(multas)),
            "Historial registrado"
        )

    st.subheader("Historial de comparendos")

    st.dataframe(
        multas,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Pagar una multa")

    opciones = [
        m["Código"]
        for m in st.session_state.multas
        if m["Estado"] == "Pendiente"
    ]

    if opciones:

        codigo = st.selectbox(
            "Selecciona el comparendo",
            opciones
        )

        multa = next(
            m for m in st.session_state.multas
            if m["Código"] == codigo
        )

        st.write(
            f"**{multa['Infracción']}**"
        )

        st.write(
            f"Valor: ${multa['Valor']:,.0f} COP"
        )

        metodo = st.selectbox(
            "Medio de pago",
            [
                "PSE",
                "Tarjeta débito/crédito",
                "Billetera digital"
            ]
        )

        if st.button("Confirmar pago"):

            multa["Estado"] = "Pagada"

            st.success(
                f"Pago simulado aprobado mediante {metodo}. "
                f"Referencia: PAY-{codigo}"
            )

            st.rerun()

    else:

        st.success(
            "No tienes multas pendientes."
        )

    st.caption(
        "Los pagos son demostrativos. No se conecta con bancos."
    )


# =====================================================
# 5. MAPA DE ZONAS AÉREAS
# =====================================================

elif pagina == "Mapa de zonas aéreas":

    encabezado(
        "GESTIÓN DEL ESPACIO AÉREO",
        "Zonas de vuelo",
        "Consulta dónde está permitido y restringido volar."
    )

    st.warning(
        "Mapa conceptual de Medellín. Las zonas son ficticias "
        "y no deben utilizarse para navegación real."
    )

    zonas = pd.DataFrame([
        {
            "Zona": "Corredor Norte",
            "Sector": "Bello - Copacabana",
            "Clasificación": "Permitida",
            "Altura máxima": "120 m"
        },
        {
            "Zona": "Corredor Río",
            "Sector": "Centro - Industriales",
            "Clasificación": "Condicionada",
            "Altura máxima": "60 m"
        },
        {
            "Zona": "Perímetro Hospitalario",
            "Sector": "Laureles",
            "Clasificación": "Prohibida",
            "Altura máxima": "0 m"
        },
        {
            "Zona": "Corredor Oriente",
            "Sector": "El Poblado - Envigado",
            "Clasificación": "Permitida",
            "Altura máxima": "100 m"
        },
        {
            "Zona": "Área Institucional",
            "Sector": "Centro administrativo",
            "Clasificación": "Prohibida",
            "Altura máxima": "0 m"
        },
        {
            "Zona": "Corredor Sur",
            "Sector": "Itagüí - Sabaneta",
            "Clasificación": "Condicionada",
            "Altura máxima": "80 m"
        }
    ])

    filtro = st.multiselect(
        "Filtrar zonas",
        [
            "Permitida",
            "Condicionada",
            "Prohibida"
        ],
        default=[
            "Permitida",
            "Condicionada",
            "Prohibida"
        ]
    )

    resultado = zonas[
        zonas["Clasificación"].isin(filtro)
    ]

    st.dataframe(
        resultado,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Leyenda")

    a, b, c = st.columns(3)

    with a:
        st.success("VERDE · Permitida")

    with b:
        st.warning("AMARILLO · Condicionada")

    with c:
        st.error("ROJO · Prohibida")


# =====================================================
# 6. PICO Y PLACA
# =====================================================

elif pagina == "Pico y placa":

    encabezado(
        "GESTIÓN DE MOVILIDAD",
        "Pico y placa aéreo",
        "Consulta las restricciones según la terminación de tu placa."
    )

    st.info(
        "Calendario ficticio de demostración."
    )

    calendario = pd.DataFrame([
        {
            "Día": "Lunes",
            "Terminaciones": "1 - 2",
            "Horario": "06:00-09:00 / 16:00-19:00"
        },
        {
            "Día": "Martes",
            "Terminaciones": "3 - 4",
            "Horario": "06:00-09:00 / 16:00-19:00"
        },
        {
            "Día": "Miércoles",
            "Terminaciones": "5 - 6",
            "Horario": "06:00-09:00 / 16:00-19:00"
        },
        {
            "Día": "Jueves",
            "Terminaciones": "7 - 8",
            "Horario": "06:00-09:00 / 16:00-19:00"
        },
        {
            "Día": "Viernes",
            "Terminaciones": "9 - 0",
            "Horario": "06:00-09:00 / 16:00-19:00"
        },
        {
            "Día": "Sábado y domingo",
            "Terminaciones": "Sin restricción general",
            "Horario": "Sujeto a zonas y eventos"
        }
    ])

    st.dataframe(
        calendario,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    st.subheader("Consulta tu placa")

    placa = st.text_input(
        "Ingresa tu placa aérea",
        placeholder="Ej. AVN-204"
    )

    dia = st.selectbox(
        "Día de consulta",
        [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo"
        ]
    )

    if st.button("Consultar restricción"):

        if len(placa.strip()) < 3:

            st.warning(
                "Ingresa una placa válida."
            )

        else:

            ultimo = placa.strip()[-1]

            if dia in ["Sábado", "Domingo"]:

                st.success(
                    "No hay pico y placa general."
                )

            else:

                fila = calendario[
                    calendario["Día"] == dia
                ].iloc[0]

                numeros = fila["Terminaciones"]

                if ultimo in numeros:

                    st.error(
                        f"La placa {placa.upper()} "
                        f"tiene restricción el {dia}."
                    )

                else:

                    st.success(
                        f"La placa {placa.upper()} "
                        f"no tiene restricción general el {dia}."
                    )


# =====================================================
# 7. CRTEC
# =====================================================

elif pagina == "CRTEC":

    encabezado(
        "NORMATIVA Y SEGURIDAD",
        "CRTEC",
        "Código de Regulación de Tecnología y Espacio Aéreo."
    )

    st.markdown(
        '<div class="panel">'
        '<span class="tag">DOCUMENTO · DEMO</span>'
        '<h3>Reglas para compartir el cielo.</h3>'
        '<p>Lineamientos de circulación, identificación, seguridad '
        'y uso responsable del espacio aéreo.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander(
        "1. Clasificación de zonas",
        expanded=True
    ):

        st.write(
            "Verde: vuelo permitido. "
            "Amarillo: vuelo condicionado a autorización. "
            "Rojo: vuelo prohibido."
        )

    with st.expander("2. Requisitos de los vehículos"):

        st.write(
            "Placa visible, geolocalización activa, "
            "SOAT vigente, revisión técnica y sistemas de seguridad."
        )

    with st.expander("3. Requisitos de los conductores"):

        st.write(
            "Licencia vigente, identificación digital "
            "y cumplimiento de corredores, alturas y horarios."
        )

    with st.expander("4. Infracciones y sanciones"):

        st.write(
            "Operar en zonas prohibidas, ignorar restricciones, "
            "volar sin documentos o desactivar sistemas de seguridad."
        )

    with st.expander("5. Responsabilidad del conductor"):

        st.write(
            "Verificar las condiciones meteorológicas, "
            "restricciones temporales y estado técnico del vehículo."
        )

    st.download_button(
        label="⬇ Descargar código CRTEC",
        data=CRTEC,
        file_name="CRTEC_Trafico_Aereo_Colombiano.md",
        mime="text/markdown"
    )

    st.caption(
        "Documento ficticio para el proyecto de futuros imaginados."
    )


# =====================================================
# 8. NOTICIAS
# =====================================================

elif pagina == "Noticias":

    encabezado(
        "SALA DE PRENSA",
        "Noticias y comunicados",
        "Mantente informado sobre las novedades del tránsito aéreo."
    )

    noticias = [
        (
            "06 NOV 2026",
            "Nueva actualización del CRTEC",
            "Se presenta una actualización conceptual para "
            "fortalecer la identificación digital."
        ),
        (
            "02 NOV 2026",
            "Nuevo corredor aéreo del Oriente",
            "El corredor de demostración Oriente amplía "
            "sus horarios de operación."
        ),
        (
            "28 OCT 2026",
            "Calendario de pico y placa de noviembre",
            "Consulta las terminaciones de placa y horarios "
            "de restricción del próximo mes."
        )
    ]

    for fecha, titulo, descripcion in noticias:

        st.markdown(f"""
        <div class="panel" style="margin-bottom:15px">

            <div class="eyebrow">
                {fecha} · COMUNICADO OFICIAL DEMOSTRATIVO
            </div>

            <h3>{titulo}</h3>

            <p style="color:#c4d2ef">
                {descripcion}
            </p>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# PIE DE PÁGINA
# =====================================================

st.markdown("---")

st.markdown("""
<center>

**TRÁNSITO AÉREO COLOMBIANO · TAC**

Portal ciudadano de movilidad aérea.

© 2026 · Proyecto de futuros imaginados.

</center>
""", unsafe_allow_html=True)
