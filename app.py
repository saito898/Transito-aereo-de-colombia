import base64
import inspect
import re
from datetime import date, datetime

import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURACIÓN
# =========================================================
st.set_page_config(
    page_title="Tránsito Aéreo Colombiano",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# COMPATIBILIDAD (use_container_width -> width="stretch")
# =========================================================
def _ancho(fn):
    try:
        if "width" in inspect.signature(fn).parameters:
            return {"width": "stretch"}
    except (TypeError, ValueError):
        pass
    return {"use_container_width": True}


BTN_W = _ancho(st.button)
SUBMIT_W = _ancho(st.form_submit_button)
DL_W = _ancho(st.download_button)
DF_W = _ancho(st.dataframe)


def h(texto):
    """Compacta HTML en una sola línea para que Markdown no lo rompa."""
    return " ".join(l.strip() for l in texto.splitlines() if l.strip())


# =========================================================
# CARRO VOLADOR (SVG embebido)
# =========================================================
CAR_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 140">
<defs>
<linearGradient id="b" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#9dbdf2"/>
</linearGradient>
<linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#8fdcff"/><stop offset="1" stop-color="#0b3f94"/>
</linearGradient>
<radialGradient id="p">
<stop offset="0" stop-color="#ffffff"/>
<stop offset=".35" stop-color="#5de0ff"/>
<stop offset="1" stop-color="#5de0ff" stop-opacity="0"/>
</radialGradient>
</defs>
<ellipse cx="85" cy="112" rx="40" ry="14" fill="url(#p)"/>
<ellipse cx="215" cy="112" rx="40" ry="14" fill="url(#p)"/>
<path d="M20 88 C20 70 50 64 80 60 L110 40 C125 30 175 30 195 42 L225 60 C262 64 282 72 282 88 C282 100 270 104 258 104 L42 104 C28 104 20 100 20 88 Z" fill="url(#b)" stroke="#5141A8" stroke-width="2.5"/>
<path d="M118 58 L132 42 C145 36 170 36 183 43 L204 58 Z" fill="url(#g)"/>
<line x1="160" y1="38" x2="160" y2="58" stroke="#ffffff" stroke-width="2.5"/>
<path d="M32 84 L268 84" stroke="#0753B8" stroke-width="3.5" stroke-linecap="round"/>
<path d="M32 92 L200 92" stroke="#5141A8" stroke-width="2" stroke-linecap="round" opacity=".6"/>
<rect x="262" y="76" width="16" height="6" rx="3" fill="#ffd966"/>
<rect x="22" y="76" width="11" height="6" rx="3" fill="#ff6b6b"/>
<ellipse cx="85" cy="104" rx="30" ry="8" fill="#073B8C"/>
<ellipse cx="85" cy="104" rx="21" ry="4.5" fill="#5de0ff"/>
<ellipse cx="215" cy="104" rx="30" ry="8" fill="#073B8C"/>
<ellipse cx="215" cy="104" rx="21" ry="4.5" fill="#5de0ff"/>
</svg>
"""
CAR_URI = "data:image/svg+xml;base64," + base64.b64encode(CAR_SVG.encode()).decode()

SKY_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 40">
<g fill="#2f6fd0" fill-opacity=".55">
<rect x="0" y="20" width="16" height="20"/><rect x="16" y="10" width="12" height="30"/>
<rect x="28" y="24" width="14" height="16"/><rect x="42" y="14" width="18" height="26"/>
<rect x="60" y="26" width="12" height="14"/><rect x="72" y="8" width="14" height="32"/>
<rect x="86" y="22" width="18" height="18"/><rect x="104" y="16" width="12" height="24"/>
<rect x="116" y="28" width="16" height="12"/><rect x="132" y="12" width="14" height="28"/>
<rect x="146" y="22" width="16" height="18"/><rect x="162" y="6" width="12" height="34"/>
<rect x="174" y="20" width="14" height="20"/><rect x="188" y="26" width="12" height="14"/>
</g>
</svg>
"""
CITY_URI = "data:image/svg+xml;base64," + base64.b64encode(SKY_SVG.encode()).decode()

# =========================================================
# ESTILOS
# =========================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    color-scheme: light;
    --azul: #0753B8;
    --azul-oscuro: #073B8C;
    --morado: #5141A8;
    --cyan: #36D1FF;
    --texto: #263653;
    --texto-sec: #65718A;
    --borde: rgba(120, 150, 215, 0.25);
    --good: #138a5b;
    --warn: #b27a17;
    --bad: #c23b3b;
}

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ---------- FONDO DE CIELO ---------- */
.stApp {
    background: linear-gradient(180deg, #7ec8ff 0%, #bfe3ff 30%, #e6f3ff 62%, #f8fbff 100%) fixed;
    color: var(--texto);
}
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    position: relative;
    z-index: 1;
}

.stApp div[data-testid="stMarkdownContainer"] p,
.stApp div[data-testid="stMarkdownContainer"] li { color: var(--texto); }
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Space Grotesk', sans-serif;
    color: #12306b;
}

/* Capa fija de cielo (nubes + carro lejano) */
.sky-layer { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
div[data-testid="stElementContainer"]:has(.sky-layer),
div.element-container:has(.sky-layer) { height: 0 !important; margin: 0 !important; }

.sun {
    position: absolute; top: -120px; right: -100px; width: 420px; height: 420px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.95), rgba(255,244,200,.55) 38%, transparent 70%);
    animation: pulse 7s ease-in-out infinite;
}
.cloud {
    position: absolute; left: -320px; background: #fff; border-radius: 100px; opacity: .8;
    filter: blur(.6px); animation: drift linear infinite; box-shadow: 0 12px 30px rgba(120,160,230,.18);
}
.cloud::before, .cloud::after { content: ""; position: absolute; background: #fff; border-radius: 50%; }
.cloud::before { width: 48%; height: 170%; top: -75%; left: 14%; }
.cloud::after  { width: 36%; height: 130%; top: -48%; right: 14%; }
.c1 { top: 9%;  width: 190px; height: 52px; animation-duration: 75s; animation-delay: -10s; }
.c2 { top: 24%; width: 130px; height: 36px; animation-duration: 55s; animation-delay: -40s; opacity: .6; }
.c3 { top: 45%; width: 230px; height: 62px; animation-duration: 95s; animation-delay: -60s; opacity: .7; }
.c4 { top: 66%; width: 150px; height: 42px; animation-duration: 65s; animation-delay: -25s; opacity: .55; }
.c5 { top: 82%; width: 210px; height: 56px; animation-duration: 85s; animation-delay: -5s; opacity: .65; }
.bg-car {
    position: absolute; top: 18%; left: -220px; width: 150px; height: 70px; opacity: .45;
    background: url("__CAR__") center / contain no-repeat;
    animation: crossSky 40s linear infinite, bob 3.4s ease-in-out infinite;
}
.bg-car.second { top: 57%; width: 100px; height: 48px; opacity: .3; animation-duration: 62s, 4s; animation-delay: -28s, 0s; }

@keyframes drift { from { transform: translateX(0); } to { transform: translateX(calc(100vw + 650px)); } }
@keyframes crossSky { from { left: -220px; } to { left: 105%; } }
@keyframes bob {
    0%, 100% { transform: translateY(0) rotate(-1deg); }
    50% { transform: translateY(-10px) rotate(1.2deg); }
}
@keyframes pulse { 0%, 100% { opacity: .85; transform: scale(1); } 50% { opacity: 1; transform: scale(1.06); } }

/* ---------- ENCABEZADO ---------- */
.hero-header {
    position: relative; overflow: hidden; text-align: center;
    padding: 34px 20px 30px; margin-bottom: 22px; border-radius: 24px;
    background: linear-gradient(115deg, #073B8C 0%, #0753B8 45%, #5141A8 100%);
    box-shadow: 0 14px 40px rgba(7, 59, 140, .28);
    border: 1px solid rgba(255,255,255,.25);
}
.hero-header::before {
    content: ""; position: absolute; inset: 0;
    background:
        radial-gradient(circle at 12% 120%, rgba(255,255,255,.28), transparent 45%),
        radial-gradient(circle at 90% -20%, rgba(54,209,255,.35), transparent 45%);
}
.hero-car {
    position: absolute; top: 14px; left: -200px; width: 150px; height: 70px; opacity: .5;
    background: url("__CAR__") center / contain no-repeat;
    animation: crossSky 18s linear infinite, bob 3s ease-in-out infinite;
}
.stApp .hero-header .hero-title {
    position: relative; z-index: 2; color: #FFFFFF !important;
    font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 700;
    letter-spacing: 2px; margin: 0 0 10px 0; padding: 0; text-shadow: 0 3px 14px rgba(0,0,40,.35);
}
.stApp .hero-header .hero-subtitle {
    position: relative; z-index: 2; color: #FFFFFF !important; font-size: 18px; margin: 0 0 6px 0;
}
.stApp .hero-header .hero-caption {
    position: relative; z-index: 2; color: #D6E4FF !important; font-size: 12px; margin: 0; letter-spacing: 1px;
}

/* Encabezado de cada página */
.page-header {
    position: relative; overflow: hidden; padding: 26px 30px; margin-bottom: 22px; border-radius: 20px;
    background: linear-gradient(115deg, #073B8C, #0753B8 55%, #5141A8);
    box-shadow: 0 10px 28px rgba(7, 59, 140, .22);
}
.page-header::after {
    content: ""; position: absolute; right: 28px; top: 50%; width: 130px; height: 62px; margin-top: -31px;
    background: url("__CAR__") center / contain no-repeat; opacity: .85;
    animation: bob 3s ease-in-out infinite;
}
.stApp .page-header h1 {
    color: #FFFFFF !important; font-size: 32px; margin: 0 0 6px 0; padding: 0; position: relative; z-index: 1;
}
.stApp .page-header p { color: #DCE8FF !important; margin: 0; font-size: 15px; position: relative; z-index: 1; max-width: 70%; }

/* ---------- NAVBAR ---------- */
.st-key-navbar {
    background: rgba(255,255,255,.85); backdrop-filter: blur(10px);
    border: 1px solid var(--borde); border-radius: 16px; padding: 8px 12px; margin-bottom: 28px;
    box-shadow: 0 6px 20px rgba(30, 70, 150, .08);
}
.st-key-navbar button {
    background: transparent !important; color: #53617C !important; border: none !important;
    border-radius: 12px !important; font-weight: 600 !important; font-size: 14px !important;
    min-height: 43px; box-shadow: none !important; transition: all .2s ease;
}
.st-key-navbar button:hover { background: #EAF2FF !important; color: var(--azul) !important; transform: translateY(-1px); }
.st-key-navbar button[kind="primary"] {
    background: linear-gradient(100deg, #0753B8, #6551B8) !important; color: #FFFFFF !important;
    box-shadow: 0 6px 16px rgba(7, 83, 184, .3) !important;
}
.st-key-navbar button[kind="primary"] p { color: #FFFFFF !important; }

/* ---------- BOTONES ---------- */
.stButton button, .stDownloadButton button, .stFormSubmitButton button {
    border-radius: 12px !important; font-weight: 600 !important; transition: all .2s ease;
}
.stButton button[kind="primary"], .stDownloadButton button, .stFormSubmitButton button[kind="primary"],
.stFormSubmitButton button {
    background: linear-gradient(100deg, #0753B8, #6551B8) !important; color: #FFFFFF !important; border: none !important;
}
.stButton button[kind="primary"] p, .stDownloadButton button p, .stFormSubmitButton button p { color: #FFFFFF !important; }
.stButton button[kind="primary"]:hover, .stDownloadButton button:hover, .stFormSubmitButton button:hover {
    filter: brightness(1.1); transform: translateY(-1px); box-shadow: 0 8px 18px rgba(65, 70, 170, .3);
}

/* ---------- PORTADA ---------- */
.welcome-banner {
    position: relative; overflow: hidden;
    background: linear-gradient(115deg, #073B8C, #0753B8 55%, #5141A8);
    padding: 52px 44px; border-radius: 24px; margin-bottom: 32px;
    box-shadow: 0 14px 40px rgba(7, 59, 140, .28);
}
.welcome-banner::after {
    content: ""; position: absolute; right: 40px; top: 50%; width: 320px; height: 150px; margin-top: -75px;
    background: url("__CAR__") center / contain no-repeat; animation: bob 3.2s ease-in-out infinite;
    filter: drop-shadow(0 22px 22px rgba(0, 20, 80, .35));
}
.stApp .welcome-banner h1 {
    color: #FFFFFF !important; font-size: 40px; font-weight: 700; line-height: 1.2; margin: 14px 0 12px; padding: 0;
}
.stApp .welcome-banner p { color: #E5EBFF !important; font-size: 16px; max-width: 520px; line-height: 1.6; }
.stApp .welcome-banner .welcome-tag {
    color: #BFE6FF !important; font-size: 11px; font-weight: 700; letter-spacing: 2px;
}

/* ---------- TARJETAS ---------- */
.info-card, .news-card {
    background: rgba(255,255,255,.92); backdrop-filter: blur(8px);
    border: 1px solid var(--borde); border-radius: 18px; padding: 24px; min-height: 180px;
    transition: all .25s ease; margin-bottom: 12px; box-shadow: 0 6px 20px rgba(30, 70, 150, .06);
}
.info-card:hover, .news-card:hover {
    transform: translateY(-6px); border-color: #7fb4ff; box-shadow: 0 16px 34px rgba(30, 80, 170, .16);
}
.stApp .info-card h3, .stApp .news-card h3 { color: #12306b !important; font-size: 18px; margin-top: 0; }
.stApp .info-card p, .stApp .news-card p { color: #65718A !important; font-size: 14px; line-height: 1.6; }
.stApp .news-label { color: #6554B8 !important; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; }

/* ---------- PANEL DE CONSULTA ---------- */
.search-panel {
    background: rgba(255,255,255,.92); border: 1px solid var(--borde); border-radius: 20px;
    padding: 26px 28px; margin: 6px 0 18px; box-shadow: 0 8px 24px rgba(30, 70, 150, .08);
}
.stApp .search-panel h3 { margin: 0 0 8px 0; color: #12306b !important; }
.stApp .search-description { color: #65718A !important; font-size: 14px; margin-bottom: 14px; }
.plate-example {
    display: inline-block; background: linear-gradient(180deg, #fff, #eaf1ff); color: #073B8C;
    border: 2px solid #073B8C; border-radius: 8px; padding: 6px 16px; font-size: 15px;
    font-weight: 700; letter-spacing: 4px; font-family: 'Space Grotesk', sans-serif;
}

/* ---------- FORMULARIOS / INPUTS ---------- */
div[data-testid="stForm"] {
    background: rgba(255,255,255,.92); border: 1px solid var(--borde); border-radius: 20px; padding: 22px;
    box-shadow: 0 8px 24px rgba(30, 70, 150, .07);
}
.stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label, .stNumberInput label {
    color: #344665 !important; font-weight: 600 !important;
}
.stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
    background: #FFFFFF !important; color: #263653 !important; border: 1px solid #C5D3EA !important;
    border-radius: 12px !important; min-height: 45px; box-shadow: none !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #929DB0 !important; opacity: 1; }
.stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus, .stDateInput input:focus {
    border: 1px solid #6551B8 !important; box-shadow: 0 0 0 3px rgba(101, 81, 184, .15) !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: #FFFFFF !important; border-color: #C5D3EA !important; border-radius: 12px !important;
}
.stSelectbox div[data-baseweb="select"] span { color: #263653 !important; }
.stCheckbox label, .stCheckbox p { color: #344665 !important; }

/* Contenedores con borde */
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"]) { border-radius: 16px; }
div[data-testid="stExpander"] { background: #FFFFFF; border: 1px solid var(--borde); border-radius: 14px; }
div[data-testid="stDataFrame"] { background: #FFFFFF; border-radius: 14px; overflow: hidden; }
div[data-testid="stAlert"] p { color: inherit !important; }

/* ---------- RESULTADO DE VEHÍCULO ---------- */
.veh-head {
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
    background: rgba(255,255,255,.95); border: 1px solid var(--borde); border-radius: 18px;
    padding: 18px 24px; margin: 10px 0 16px; box-shadow: 0 8px 24px rgba(30, 70, 150, .08);
}
.stApp .veh-title { font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #5141A8 !important; }
.diag { padding: 9px 16px; border-radius: 999px; font-weight: 700; font-size: 14px; }
.diag.good { background: #E3F6EE; color: #0f7a51 !important; }
.diag.warn { background: #FFF3D9; color: #9a6a10 !important; }
.diag.bad  { background: #FDE5E5; color: #b23232 !important; }

.data-card {
    background: rgba(255,255,255,.95); border: 1px solid var(--borde); border-radius: 18px;
    padding: 20px 24px; height: 100%; box-shadow: 0 6px 20px rgba(30, 70, 150, .06);
}
.stApp .data-card h4 { margin: 0 0 12px 0; color: #12306b !important; font-size: 17px; }
.data-row { display: flex; justify-content: space-between; gap: 12px; padding: 8px 0; border-bottom: 1px dashed #DCE6F5; }
.data-row:last-child { border-bottom: none; }
.stApp .data-row .k { color: #65718A !important; font-size: 14px; }
.stApp .data-row .v { color: #1d2f55 !important; font-weight: 600; font-size: 14px; text-align: right; }

.section-title { margin: 26px 0 12px; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; color: #12306b !important; }

.docs-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; }
.doc-card {
    position: relative; background: #FFFFFF; border: 1px solid var(--borde); border-radius: 18px;
    padding: 20px 22px 20px 26px; overflow: hidden; box-shadow: 0 6px 20px rgba(30, 70, 150, .06);
    transition: transform .2s ease;
}
.doc-card:hover { transform: translateY(-4px); }
.doc-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 7px; background: var(--c); }
.doc-card.good { --c: linear-gradient(180deg, #2fd39a, #138a5b); }
.doc-card.warn { --c: linear-gradient(180deg, #ffcf66, #d99a1c); }
.doc-card.bad  { --c: linear-gradient(180deg, #ff8585, #c23b3b); }
.stApp .doc-name { color: #65718A !important; font-size: 13px; font-weight: 600; letter-spacing: .5px; text-transform: uppercase; }
.stApp .doc-status { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; margin: 6px 0 4px; }
.stApp .doc-card.good .doc-status { color: #138a5b !important; }
.stApp .doc-card.warn .doc-status { color: #b27a17 !important; }
.stApp .doc-card.bad  .doc-status { color: #c23b3b !important; }
.stApp .doc-date { color: #344665 !important; font-size: 13px; }
.stApp .doc-days { color: #8993A9 !important; font-size: 12px; margin-top: 2px; }

.fine-list { display: flex; flex-direction: column; gap: 10px; }
.fine-row {
    display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap;
    background: #FFFFFF; border: 1px solid var(--borde); border-radius: 14px; padding: 14px 18px;
}
.stApp .fine-desc { color: #1d2f55 !important; font-weight: 600; font-size: 15px; }
.stApp .fine-amount { color: #12306b !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 18px; }
.badge { padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 700; }
.badge.pend { background: #FFF3D9; color: #9a6a10 !important; }
.badge.paid { background: #E3F6EE; color: #0f7a51 !important; }

.total-card {
    display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
    margin-top: 16px; padding: 18px 24px; border-radius: 18px; color: #fff;
    background: linear-gradient(110deg, #073B8C, #5141A8); box-shadow: 0 10px 26px rgba(7, 59, 140, .25);
}
.stApp .total-card .t-label { color: #D6E4FF !important; font-size: 14px; }
.stApp .total-card .t-value { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; }

.empty-ok {
    background: #E9F8F1; border: 1px solid #BDE9D6; border-radius: 14px; padding: 14px 18px;
    color: #0f7a51 !important; font-weight: 600;
}

/* ---------- TABLA PICO Y PLACA ---------- */
.pp-table { width: 100%; border-collapse: separate; border-spacing: 0; background: #fff; border-radius: 16px; overflow: hidden; border: 1px solid var(--borde); }
.pp-table th { background: linear-gradient(100deg, #073B8C, #5141A8); color: #fff !important; padding: 12px 16px; text-align: left; font-size: 13px; letter-spacing: .5px; }
.pp-table td { padding: 12px 16px; color: #263653 !important; font-size: 14px; border-top: 1px solid #E5ECF8; }
.pp-table tr.hoy td { background: #EAF3FF; font-weight: 700; color: #073B8C !important; }

/* ---------- PIE ---------- */
.footer-info { text-align: center; padding: 26px; margin-top: 30px; }
.stApp .footer-info h3 { color: #12306b !important; }
.stApp .footer-info p { color: #52618a !important; }
.stApp .footer-info small { color: #6f7ea1 !important; }
hr { border-color: rgba(100, 140, 210, .25) !important; }

/* =========================================================
   BARRA LATERAL CON CARRO LEVITANDO
   ========================================================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(185deg, #073B8C 0%, #1d5bc9 55%, #5141A8 100%);
    border-right: 1px solid rgba(255,255,255,.2);
}
section[data-testid="stSidebar"] > div { padding-top: 1.2rem; }

.side-brand { text-align: center; margin-bottom: 14px; }
.stApp .side-brand .sb-title { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 17px; letter-spacing: 1.5px; margin: 0; }
.stApp .side-brand .sb-sub { color: #BFD6FF !important; font-size: 12px; margin: 2px 0 0; }

.side-scene {
    position: relative; height: 215px; border-radius: 20px; overflow: hidden;
    background: linear-gradient(180deg, #3b9bff 0%, #9fd2ff 60%, #e6f4ff 100%);
    border: 1px solid rgba(255,255,255,.45); box-shadow: inset 0 0 30px rgba(255,255,255,.25), 0 10px 24px rgba(0,20,80,.3);
}
.s-sun { position: absolute; top: -30px; right: -20px; width: 110px; height: 110px; border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.95), rgba(255,240,190,.4) 50%, transparent 72%); }
.s-cloud { position: absolute; left: -130px; background: #fff; border-radius: 50px; opacity: .9; animation: sdrift linear infinite; }
.s-cloud::before, .s-cloud::after { content: ""; position: absolute; background: #fff; border-radius: 50%; }
.s-cloud::before { width: 46%; height: 160%; top: -70%; left: 14%; }
.s-cloud::after  { width: 34%; height: 120%; top: -40%; right: 14%; }
.sc1 { top: 24px; width: 70px; height: 20px; animation-duration: 14s; animation-delay: -3s; }
.sc2 { top: 78px; width: 50px; height: 15px; animation-duration: 9s; animation-delay: -6s; opacity: .7; }
.sc3 { top: 128px; width: 86px; height: 24px; animation-duration: 17s; animation-delay: -10s; opacity: .8; }
@keyframes sdrift { from { transform: translateX(0); } to { transform: translateX(520px); } }

.s-line { position: absolute; right: -120px; height: 2px; border-radius: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.95)); animation: sline 1.3s linear infinite; }
.l1 { top: 66px; width: 80px; animation-delay: 0s; }
.l2 { top: 108px; width: 60px; animation-delay: -.5s; }
.l3 { top: 92px; width: 100px; animation-delay: -.9s; }
.l4 { top: 140px; width: 70px; animation-delay: -.3s; }
@keyframes sline { from { transform: translateX(0); } to { transform: translateX(-560px); } }

.s-car {
    position: absolute; left: 50%; top: 52px; width: 176px; height: 84px; margin-left: -88px;
    background: url("__CAR__") center / contain no-repeat;
    animation: bob 2.8s ease-in-out infinite; filter: drop-shadow(0 8px 10px rgba(7, 59, 140, .25));
}
.s-shadow {
    position: absolute; left: 50%; bottom: 50px; width: 130px; height: 14px; margin-left: -65px;
    background: radial-gradient(ellipse, rgba(7, 59, 140, .45), transparent 70%); animation: shadowPulse 2.8s ease-in-out infinite;
}
@keyframes shadowPulse { 0%, 100% { transform: scale(1); opacity: .9; } 50% { transform: scale(.82); opacity: .5; } }
.s-city {
    position: absolute; left: 0; right: 0; bottom: 0; height: 40px;
    background: url("__CITY__") repeat-x bottom left / 200px 40px; animation: cityMove 6s linear infinite;
}
.s-city.far { height: 28px; opacity: .45; animation-duration: 12s; bottom: 6px; }
@keyframes cityMove { from { background-position-x: 0; } to { background-position-x: -200px; } }

.side-card {
    background: rgba(255,255,255,.13); border: 1px solid rgba(255,255,255,.25); border-radius: 16px;
    padding: 14px 16px; margin-top: 14px; backdrop-filter: blur(6px);
}
.stApp .side-card .sc-title { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 14px; margin: 0 0 8px; letter-spacing: .5px; }
.stApp .side-card .sc-row { display: flex; justify-content: space-between; align-items: center; color: #E3EEFF !important; font-size: 13px; padding: 5px 0; }
.stApp .side-card .sc-row b { color: #FFFFFF !important; }
.dot { display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 7px; animation: blink 1.8s ease-in-out infinite; }
.dot.g { background: #38e0a0; box-shadow: 0 0 8px #38e0a0; }
.dot.y { background: #ffd35c; box-shadow: 0 0 8px #ffd35c; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: .35; } }
.stApp .side-note { color: #BFD6FF !important; font-size: 11px; text-align: center; margin-top: 14px; }

@media (max-width: 800px) {
    .welcome-banner::after, .page-header::after { display: none; }
    .stApp .page-header p { max-width: 100%; }
    .stApp .hero-header .hero-title { font-size: 24px; }
}
@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }
</style>
"""
st.markdown(h(CSS.replace("__CAR__", CAR_URI).replace("__CITY__", CITY_URI)), unsafe_allow_html=True)

# Capa de cielo animada (nubes + carros lejanos)
st.markdown(
    h("""
    <div class="sky-layer">
        <div class="sun"></div>
        <div class="cloud c1"></div><div class="cloud c2"></div><div class="cloud c3"></div>
        <div class="cloud c4"></div><div class="cloud c5"></div>
        <div class="bg-car"></div><div class="bg-car second"></div>
    </div>
    """),
    unsafe_allow_html=True,
)

# =========================================================
# DATOS DE EJEMPLO
# =========================================================
def datos_iniciales():
    return {
        "ABC123A": {
            "propietario": "Mariana Restrepo Gómez", "documento": "1039456782",
            "modelo": "AeroX One", "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal", "color": "Blanco perla",
            "documentos": {"licencia": "15/08/2027", "soat": "20/12/2026", "revision": "10/06/2027"},
            "multas": [{"descripcion": "Circulación en zona de restricción", "valor": 350000, "estado": "Pendiente"}],
        },
        "XYZ456B": {
            "propietario": "Andrés Felipe Molina", "documento": "1023456789",
            "modelo": "Nimbus 4", "fabricante": "SkyMotion",
            "categoria": "Transporte ligero", "color": "Azul metálico",
            "documentos": {"licencia": "12/11/2027", "soat": "18/05/2027", "revision": "05/09/2027"},
            "multas": [],
        },
        "TAC789C": {
            "propietario": "Daniela Vélez Arango", "documento": "1002345678",
            "modelo": "AeroCity Pro", "fabricante": "AeroTech Colombia",
            "categoria": "Movilidad personal", "color": "Negro espacial",
            "documentos": {"licencia": "10/10/2026", "soat": "15/09/2026", "revision": "20/03/2027"},
            "multas": [
                {"descripcion": "Operación sin autorización vigente", "valor": 520000, "estado": "Pendiente"},
                {"descripcion": "Exceso de velocidad aérea", "valor": 250000, "estado": "Pagada"},
            ],
        },
        "DEF321D": {
            "propietario": "Sebastián Ospina López", "documento": "985678432",
            "modelo": "Falcon Air", "fabricante": "Future Mobility",
            "categoria": "Transporte ejecutivo", "color": "Gris titanio",
            "documentos": {"licencia": "01/12/2027", "soat": "20/11/2026", "revision": "01/10/2026"},
            "multas": [],
        },
        "GHI654E": {
            "propietario": "Valentina Cárdenas Ruiz", "documento": "1012345678",
            "modelo": "Cloud X", "fabricante": "SkyMotion",
            "categoria": "Movilidad personal", "color": "Púrpura aurora",
            "documentos": {"licencia": "30/07/2027", "soat": "15/04/2027", "revision": "10/02/2027"},
            "multas": [{"descripcion": "Estacionamiento en zona no autorizada", "valor": 180000, "estado": "Pendiente"}],
        },
    }


def migrar_vehiculo(veh):
    """Convierte registros guardados con el formato antiguo al formato actual."""
    if "documentos" not in veh:
        veh["documentos"] = {
            clave: veh.get(f"vencimiento_{clave}", "")
            for clave in ("licencia", "soat", "revision")
        }
    for clave in ("licencia", "soat", "revision"):
        veh["documentos"].setdefault(clave, "")
    veh.setdefault("multas", [])
    return veh


if "registro" not in st.session_state:
    st.session_state.registro = datos_iniciales()
else:
    # Sesión abierta con una versión anterior del código: se adapta sin perder pagos.
    for _placa, _veh in st.session_state.registro.items():
        migrar_vehiculo(_veh)

defaults = {
    "pagina": "Inicio",
    "resultado_registro": None,
    "resultado_multas": None,
    "solicitudes": [],
    "pagos": [],
    "flash": None,
}
for clave, valor in defaults.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor

# =========================================================
# FUNCIONES AUXILIARES
# =========================================================
PLACA_RE = r"[A-Z]{3}[0-9]{3}[A-Z]"
DIAS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
PICO = ["1 - 2", "3 - 4", "5 - 6", "7 - 8", "9 - 0", "Sin restricción", "Sin restricción"]
DOCUMENTOS = [
    ("licencia", "Licencia de operación", "🪪"),
    ("soat", "SOAT aéreo", "🛡️"),
    ("revision", "Revisión técnica", "🔧"),
]


def dinero(valor):
    return f"${valor:,.0f}".replace(",", ".")


def consultar_placa(placa):
    placa = placa.upper().strip()
    if not re.fullmatch(PLACA_RE, placa):
        return None
    return st.session_state.registro.get(placa)


def total_pendiente(vehiculo):
    return sum(m["valor"] for m in vehiculo["multas"] if m["estado"] == "Pendiente")


def estado_documento(fecha_txt):
    """Calcula el estado real del documento a partir de su fecha de vencimiento."""
    try:
        venc = datetime.strptime(fecha_txt, "%d/%m/%Y").date()
    except ValueError:
        return {"texto": "Sin datos", "clase": "warn", "detalle": "Fecha no disponible"}
    dias = (venc - date.today()).days
    if dias < 0:
        return {"texto": "Vencido", "clase": "bad", "detalle": f"Venció hace {-dias} días"}
    if dias <= 30:
        return {"texto": "Próximo a vencer", "clase": "warn", "detalle": f"Vence en {dias} días"}
    return {"texto": "Vigente", "clase": "good", "detalle": f"Vence en {dias} días"}


def diagnostico(vehiculo):
    estados = [estado_documento(f)["clase"] for f in vehiculo["documentos"].values()]
    if "bad" in estados:
        return "bad", "⛔ No autorizado para operar"
    if "warn" in estados or total_pendiente(vehiculo) > 0:
        return "warn", "⚠️ Operación con novedades"
    return "good", "✅ Apto para operar"


def html_documentos(vehiculo):
    tarjetas = ""
    for clave, nombre, icono in DOCUMENTOS:
        fecha = vehiculo["documentos"][clave]
        e = estado_documento(fecha)
        tarjetas += f"""
        <div class="doc-card {e['clase']}">
            <div class="doc-name">{icono} {nombre}</div>
            <div class="doc-status">{e['texto']}</div>
            <div class="doc-date">Vencimiento: {fecha}</div>
            <div class="doc-days">{e['detalle']}</div>
        </div>"""
    return h(f'<div class="docs-grid">{tarjetas}</div>')


def html_multas(vehiculo):
    if not vehiculo["multas"]:
        return h('<div class="empty-ok">✅ Este vehículo no registra comparendos.</div>')
    filas = ""
    for m in vehiculo["multas"]:
        pendiente = m["estado"] == "Pendiente"
        badge = "pend" if pendiente else "paid"
        filas += f"""
        <div class="fine-row">
            <div>
                <div class="fine-desc">{m['descripcion']}</div>
                <span class="badge {badge}">{m['estado']}</span>
            </div>
            <div class="fine-amount">{dinero(m['valor'])}</div>
        </div>"""
    return h(f'<div class="fine-list">{filas}</div>')


def html_total(vehiculo):
    return h(f"""
    <div class="total-card">
        <div class="t-label">Total de comparendos pendientes</div>
        <div class="t-value">{dinero(total_pendiente(vehiculo))}</div>
    </div>""")


def page_header(titulo, subtitulo):
    st.markdown(
        h(f'<div class="page-header"><h1>{titulo}</h1><p>{subtitulo}</p></div>'),
        unsafe_allow_html=True,
    )


def section(titulo):
    st.markdown(f'<div class="section-title">{titulo}</div>', unsafe_allow_html=True)


def tarjeta_info(icono, titulo, texto):
    return h(f'<div class="info-card"><h3>{icono} {titulo}</h3><p>{texto}</p></div>')


# =========================================================
# BARRA LATERAL (carro levitando)
# =========================================================
hoy_idx = date.today().weekday()
with st.sidebar:
    st.markdown(
        h(f"""
        <div class="side-brand">
            <p class="sb-title">✈️ CENTRO DE CONTROL</p>
            <p class="sb-sub">Corredores aéreos en tiempo simulado</p>
        </div>
        <div class="side-scene">
            <div class="s-sun"></div>
            <div class="s-cloud sc1"></div><div class="s-cloud sc2"></div><div class="s-cloud sc3"></div>
            <div class="s-line l1"></div><div class="s-line l2"></div>
            <div class="s-line l3"></div><div class="s-line l4"></div>
            <div class="s-car"></div>
            <div class="s-shadow"></div>
            <div class="s-city far"></div>
            <div class="s-city"></div>
        </div>
        <div class="side-card">
            <p class="sc-title">ESTADO DEL CIELO</p>
            <div class="sc-row"><span><span class="dot g"></span>Corredor norte</span><b>Despejado</b></div>
            <div class="sc-row"><span><span class="dot g"></span>Corredor centro</span><b>Fluido</b></div>
            <div class="sc-row"><span><span class="dot y"></span>Corredor sur</span><b>Viento medio</b></div>
        </div>
        <div class="side-card">
            <p class="sc-title">PICO Y PLACA HOY</p>
            <div class="sc-row"><span>{DIAS_ES[hoy_idx]}</span><b>{PICO[hoy_idx]}</b></div>
        </div>
        <p class="side-note">Datos ficticios · Proyecto académico</p>
        """),
        unsafe_allow_html=True,
    )

# =========================================================
# ENCABEZADO
# =========================================================
st.markdown(
    h("""
    <div class="hero-header">
        <div class="hero-car"></div>
        <h1 class="hero-title">✈️ TRÁNSITO AÉREO COLOMBIANO</h1>
        <p class="hero-subtitle">Movilidad aérea para un nuevo futuro.</p>
        <p class="hero-caption">Portal ciudadano · Proyecto de futuros imaginados · 2026</p>
    </div>
    """),
    unsafe_allow_html=True,
)

# =========================================================
# NAVBAR
# =========================================================
paginas = ["Inicio", "Servicios", "Registro nacional", "Multas", "Regulación", "Noticias"]
with st.container(key="navbar"):
    columnas = st.columns(len(paginas))
    for columna, nombre_pagina in zip(columnas, paginas):
        with columna:
            if st.button(
                nombre_pagina,
                key=f"nav_{nombre_pagina}",
                type="primary" if st.session_state.pagina == nombre_pagina else "secondary",
                **BTN_W,
            ):
                st.session_state.pagina = nombre_pagina
                st.session_state.resultado_registro = None
                st.session_state.resultado_multas = None
                st.rerun()

pagina = st.session_state.pagina

# =========================================================
# INICIO
# =========================================================
if pagina == "Inicio":
    st.markdown(
        h("""
        <div class="welcome-banner">
            <span class="welcome-tag">PORTAL OFICIAL · 2026</span>
            <h1>El futuro de la movilidad<br>también está en el aire.</h1>
            <p>Consulta información, conoce las normas y realiza tus trámites
            relacionados con la movilidad aérea en Colombia.</p>
        </div>
        """),
        unsafe_allow_html=True,
    )
    section("¿Qué puedes hacer en el portal?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(tarjeta_info("🪪", "Licencias aéreas",
                    "Consulta los requisitos y realiza la renovación de tu licencia de operación aérea."),
                    unsafe_allow_html=True)
    with col2:
        st.markdown(tarjeta_info("📋", "Registro nacional",
                    "Consulta los vehículos aéreos registrados en Colombia mediante su placa de identificación."),
                    unsafe_allow_html=True)
    with col3:
        st.markdown(tarjeta_info("⚠️", "Comparendos",
                    "Revisa tus infracciones, consulta los valores pendientes y gestiona tus pagos."),
                    unsafe_allow_html=True)

    section("Actualidad del tránsito aéreo")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(h("""
        <div class="news-card"><span class="news-label">REGULACIÓN</span>
        <h3>Conoce el CRTEC</h3>
        <p>Consulta el Código de Regulación de Tecnología y conoce las disposiciones
        para operar vehículos aéreos en Colombia.</p></div>"""), unsafe_allow_html=True)
    with col2:
        st.markdown(h("""
        <div class="news-card"><span class="news-label">MOVILIDAD</span>
        <h3>Consulta el pico y placa aéreo</h3>
        <p>Infórmate sobre las restricciones de circulación aérea y las fechas
        establecidas para cada categoría de vehículo.</p></div>"""), unsafe_allow_html=True)

# =========================================================
# SERVICIOS
# =========================================================
elif pagina == "Servicios":
    page_header("Servicios ciudadanos", "Realiza tus trámites relacionados con la movilidad aérea.")
    section("Renovación de licencia aérea")
    st.info("Solicita la renovación de la licencia que autoriza la operación de tu vehículo aéreo.")

    with st.form("form_renovacion"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre completo", placeholder="Ej. Mariana Restrepo Gómez")
            documento = st.text_input("Número de documento")
        with col2:
            placa = st.text_input("Placa del vehículo", placeholder="ABC123A", max_chars=7)
            correo = st.text_input("Correo electrónico")
        motivo = st.selectbox(
            "Motivo de la solicitud",
            ["Renovación por vencimiento", "Actualización de datos", "Reposición de licencia", "Otro"],
        )
        fecha = st.date_input("Fecha de solicitud", value=date.today())
        aceptar = st.checkbox("Declaro que la información suministrada es correcta.")
        enviar = st.form_submit_button("Enviar solicitud", type="primary", **SUBMIT_W)

    if enviar:
        if not nombre or not documento or not placa or not correo:
            st.error("Completa todos los campos para continuar.")
        elif not re.fullmatch(PLACA_RE, placa.upper().strip()):
            st.error("La placa debe tener el formato ABC123A.")
        elif not aceptar:
            st.warning("Debes aceptar la declaración para continuar.")
        else:
            solicitud = {
                "nombre": nombre, "documento": documento, "placa": placa.upper().strip(),
                "correo": correo, "motivo": motivo, "fecha": str(fecha),
                "radicado": f"TAC-{len(st.session_state.solicitudes) + 1001}",
            }
            st.session_state.solicitudes.append(solicitud)
            st.success("¡Solicitud registrada correctamente!")
            st.write(f"Número de radicado: **{solicitud['radicado']}**")

    if st.session_state.solicitudes:
        section("Mis solicitudes en esta sesión")
        st.dataframe(pd.DataFrame(st.session_state.solicitudes), hide_index=True, **DF_W)

    section("Otros trámites disponibles")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(tarjeta_info("📄", "Certificado de registro",
                    "Consulta la información de registro de un vehículo aéreo y sus documentos asociados."),
                    unsafe_allow_html=True)
    with col2:
        st.markdown(tarjeta_info("🔄", "Actualización de propietario",
                    "Consulta el procedimiento para actualizar la información del titular de un vehículo aéreo."),
                    unsafe_allow_html=True)

# =========================================================
# REGISTRO NACIONAL
# =========================================================
elif pagina == "Registro nacional":
    page_header(
        "Registro Nacional de Vehículos Aéreos",
        "Consulta la información de los vehículos aéreos registrados en el territorio colombiano.",
    )
    st.markdown(h("""
    <div class="search-panel">
        <h3>🔎 Consulta de vehículos</h3>
        <p class="search-description">Ingresa la placa de identificación para consultar los datos
        del vehículo, su propietario y documentación.</p>
        <span class="plate-example">ABC 123 A</span>
    </div>"""), unsafe_allow_html=True)

    with st.form("form_busqueda_placa"):
        placa_busqueda = st.text_input(
            "Número de placa", placeholder="Escribe aquí la placa del vehículo", max_chars=7
        )
        consultar = st.form_submit_button("✈️ Consultar vehículo", type="primary", **SUBMIT_W)

    if consultar:
        placa_busqueda = placa_busqueda.upper().strip()
        if not re.fullmatch(PLACA_RE, placa_busqueda):
            st.session_state.resultado_registro = None
            st.error("Formato incorrecto. La placa debe tener tres letras, tres números y una letra. Ejemplo: ABC123A.")
        elif placa_busqueda in st.session_state.registro:
            st.session_state.resultado_registro = placa_busqueda
        else:
            st.session_state.resultado_registro = None
            st.error("No encontramos un vehículo registrado con esa placa.")

    placa_resultado = st.session_state.resultado_registro
    if placa_resultado:
        v = st.session_state.registro[placa_resultado]
        clase, texto_diag = diagnostico(v)

        st.markdown(h(f"""
        <div class="veh-head">
            <span class="veh-title">✈️ Vehículo {placa_resultado}</span>
            <span class="diag {clase}">{texto_diag}</span>
        </div>"""), unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(h(f"""
            <div class="data-card"><h4>🚀 Información del vehículo</h4>
            <div class="data-row"><span class="k">Modelo</span><span class="v">{v['modelo']}</span></div>
            <div class="data-row"><span class="k">Fabricante</span><span class="v">{v['fabricante']}</span></div>
            <div class="data-row"><span class="k">Categoría</span><span class="v">{v['categoria']}</span></div>
            <div class="data-row"><span class="k">Color</span><span class="v">{v['color']}</span></div>
            </div>"""), unsafe_allow_html=True)
        with col2:
            st.markdown(h(f"""
            <div class="data-card"><h4>👤 Propietario</h4>
            <div class="data-row"><span class="k">Nombre</span><span class="v">{v['propietario']}</span></div>
            <div class="data-row"><span class="k">Documento</span><span class="v">{v['documento']}</span></div>
            </div>"""), unsafe_allow_html=True)

        section("📑 Estado de documentación")
        st.markdown(html_documentos(v), unsafe_allow_html=True)

        section("⚠️ Historial de comparendos")
        st.markdown(html_multas(v), unsafe_allow_html=True)
        st.markdown(html_total(v), unsafe_allow_html=True)

    section("Vehículos registrados en el sistema")
    busqueda_tabla = st.text_input("Filtrar registros", placeholder="Buscar por placa o propietario...").lower()
    filas = []
    for placa_reg, veh in st.session_state.registro.items():
        if busqueda_tabla in placa_reg.lower() or busqueda_tabla in veh["propietario"].lower():
            filas.append({
                "Placa": placa_reg,
                "Propietario": veh["propietario"],
                "Modelo": veh["modelo"],
                "Categoría": veh["categoria"],
                "Licencia": estado_documento(veh["documentos"]["licencia"])["texto"],
            })
    if filas:
        st.dataframe(pd.DataFrame(filas), hide_index=True, **DF_W)
    else:
        st.info("No se encontraron vehículos.")

# =========================================================
# MULTAS
# =========================================================
elif pagina == "Multas":
    page_header(
        "Comparendos y sanciones",
        "Consulta las infracciones asociadas a un vehículo aéreo y revisa los valores pendientes de pago.",
    )
    if st.session_state.flash:
        st.success(st.session_state.flash)
        st.session_state.flash = None

    st.markdown(h("""
    <div class="search-panel">
        <h3>⚠️ Consulta de comparendos</h3>
        <p class="search-description">Introduce la placa de tu vehículo para consultar las infracciones
        y obligaciones pendientes.</p>
        <span class="plate-example">ABC 123 A</span>
    </div>"""), unsafe_allow_html=True)

    with st.form("form_busqueda_multas"):
        placa_multa = st.text_input(
            "Número de placa", placeholder="Escribe aquí la placa del vehículo", max_chars=7
        )
        consultar_multa = st.form_submit_button("Consultar comparendos", type="primary", **SUBMIT_W)

    if consultar_multa:
        placa_multa = placa_multa.upper().strip()
        if consultar_placa(placa_multa) is None:
            st.session_state.resultado_multas = None
            st.error("Placa inválida o vehículo no registrado.")
        else:
            st.session_state.resultado_multas = placa_multa

    placa_resultado = st.session_state.resultado_multas
    if placa_resultado:
        v = st.session_state.registro[placa_resultado]
        clase, texto_diag = diagnostico(v)

        st.markdown(h(f"""
        <div class="veh-head">
            <span class="veh-title">Comparendos de {placa_resultado}</span>
            <span class="diag {clase}">{texto_diag}</span>
        </div>"""), unsafe_allow_html=True)
        st.write(f"Propietario: **{v['propietario']}**")

        section("📑 Vencimiento de documentos")
        st.markdown(html_documentos(v), unsafe_allow_html=True)

        section("🧾 Detalle de comparendos")
        if v["multas"]:
            for indice, multa in enumerate(v["multas"]):
                pendiente = multa["estado"] == "Pendiente"
                badge = "pend" if pendiente else "paid"
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1.3, 1.4], vertical_alignment="center")
                    with c1:
                        st.markdown(h(f"""
                        <div class="fine-desc">{multa['descripcion']}</div>
                        <span class="badge {badge}">{multa['estado']}</span>"""), unsafe_allow_html=True)
                    with c2:
                        st.markdown(f'<div class="fine-amount">{dinero(multa["valor"])}</div>', unsafe_allow_html=True)
                    with c3:
                        if pendiente:
                            if st.button("Pagar comparendo", key=f"pagar_{placa_resultado}_{indice}",
                                         type="primary", **BTN_W):
                                multa["estado"] = "Pagada"
                                st.session_state.pagos.append({
                                    "placa": placa_resultado,
                                    "descripcion": multa["descripcion"],
                                    "valor": dinero(multa["valor"]),
                                    "fecha": str(date.today()),
                                })
                                st.session_state.flash = "✅ Pago simulado realizado correctamente."
                                st.rerun()
                        else:
                            st.markdown('<span class="badge paid">Comparendo pagado</span>', unsafe_allow_html=True)
            st.markdown(html_total(v), unsafe_allow_html=True)
        else:
            st.markdown(html_multas(v), unsafe_allow_html=True)

    section("Historial de pagos simulados")
    if st.session_state.pagos:
        st.dataframe(pd.DataFrame(st.session_state.pagos), hide_index=True, **DF_W)
    else:
        st.info("Todavía no hay pagos registrados en esta sesión.")

# =========================================================
# REGULACIÓN
# =========================================================
elif pagina == "Regulación":
    page_header(
        "Regulación del tránsito aéreo",
        "Consulta las disposiciones que organizan la movilidad de vehículos aéreos en Colombia.",
    )
    section("Código de Regulación de Tecnología (CRTEC)")
    st.info("Documento de referencia del proyecto de futuros imaginados. Su contenido es una propuesta ficticia.")

    capitulos = [
        ("Capítulo I. Disposiciones generales",
         "El Código de Regulación de Tecnología y Tránsito Aéreo (CRTEC) establece los lineamientos para la "
         "circulación, operación, identificación y control de vehículos aéreos en el territorio colombiano."),
        ("Capítulo II. Registro e identificación",
         "Todo vehículo aéreo deberá contar con una placa única, compuesta por tres letras, tres números y una letra. "
         "Todo vehículo deberá estar asociado a un propietario registrado y mantener su documentación vigente."),
        ("Capítulo III. Seguridad y operación",
         "Los vehículos deberán respetar las alturas de operación establecidas, mantener una distancia mínima de "
         "seguridad y realizar sus operaciones en corredores autorizados. Los conductores deberán contar con licencia vigente."),
        ("Capítulo IV. Zonas de circulación",
         "La circulación aérea estará organizada en zonas autorizadas, restringidas y prohibidas."),
        ("Capítulo V. Infracciones",
         "El incumplimiento de las disposiciones podrá generar comparendos, sanciones económicas y suspensión de la licencia."),
    ]
    for i, (titulo_cap, texto_cap) in enumerate(capitulos):
        with st.expander(titulo_cap, expanded=(i == 0)):
            st.write(texto_cap)

    documento_crtec = "CÓDIGO DE REGULACIÓN DE TECNOLOGÍA Y TRÁNSITO AÉREO\nCRTEC - COLOMBIA 2026\n\n"
    for titulo_cap, texto_cap in capitulos:
        documento_crtec += f"{titulo_cap.upper()}\n{texto_cap}\n\n"
    documento_crtec += "Documento ficticio para proyecto académico de futuros imaginados."

    st.download_button(
        "⬇️ Descargar documento CRTEC",
        data=documento_crtec,
        file_name="CRTEC_Colombia_2026.txt",
        mime="text/plain",
        **DL_W,
    )

    section("Zonas de circulación aérea")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(tarjeta_info("🟢", "Zona autorizada",
                    "Espacios habilitados para la circulación de vehículos aéreos bajo las condiciones establecidas."),
                    unsafe_allow_html=True)
    with col2:
        st.markdown(tarjeta_info("🟡", "Zona restringida",
                    "Espacios donde la circulación requiere permisos o condiciones especiales."),
                    unsafe_allow_html=True)
    with col3:
        st.markdown(tarjeta_info("🔴", "Zona prohibida",
                    "Espacios en los que no se permite la circulación de vehículos aéreos."),
                    unsafe_allow_html=True)

    section("Pico y placa aéreo")
    filas_pp = ""
    for i, (dia, digitos) in enumerate(zip(DIAS_ES, PICO)):
        horario = "Todo el día" if i >= 5 else "6:00 a.m. - 8:00 p.m."
        clase_fila = "hoy" if i == hoy_idx else ""
        marca = " (hoy)" if i == hoy_idx else ""
        filas_pp += f'<tr class="{clase_fila}"><td>{dia}{marca}</td><td>{digitos}</td><td>{horario}</td></tr>'
    st.markdown(
        h(f'<table class="pp-table"><thead><tr><th>Día</th><th>Último dígito</th><th>Horario</th></tr></thead>'
          f"<tbody>{filas_pp}</tbody></table>"),
        unsafe_allow_html=True,
    )
    st.caption("Calendario ficticio de ejemplo para el proyecto académico.")

# =========================================================
# NOTICIAS
# =========================================================
elif pagina == "Noticias":
    page_header(
        "Noticias y actualidad",
        "Conoce las novedades, anuncios y actualizaciones del sistema de tránsito aéreo colombiano.",
    )
    noticias = [
        ("REGULACIÓN", "Nuevo código de circulación aérea", "06 de noviembre de 2026",
         "El sistema presenta el CRTEC, un documento que reúne las disposiciones para organizar la movilidad aérea."),
        ("MOVILIDAD", "Actualización del pico y placa aéreo", "03 de noviembre de 2026",
         "Conoce la distribución semanal de circulación según el último dígito de la placa."),
        ("SERVICIOS", "Renovación digital de licencias", "28 de octubre de 2026",
         "Los ciudadanos podrán gestionar solicitudes de renovación de licencia desde el portal."),
        ("SEGURIDAD", "Recomendaciones para la movilidad aérea", "20 de octubre de 2026",
         "Consulta las recomendaciones para operar vehículos aéreos de manera responsable."),
    ]
    for categoria, titulo_n, fecha_n, desc_n in noticias:
        st.markdown(h(f"""
        <div class="news-card" style="min-height:0">
            <span class="news-label">{categoria}</span>
            <h3>{titulo_n}</h3>
            <p style="margin:0 0 8px;font-size:12px;color:#8993A9 !important">{fecha_n}</p>
            <p>{desc_n}</p>
        </div>"""), unsafe_allow_html=True)

# =========================================================
# PIE DE PÁGINA
# =========================================================
st.markdown("---")
st.markdown(h("""
<div class="footer-info">
    <h3>✈️ Tránsito Aéreo Colombiano</h3>
    <p>Movilidad aérea para un nuevo futuro.</p>
    <small>Proyecto de futuros imaginados · 2026<br>Plataforma de demostración académica.</small>
</div>
"""), unsafe_allow_html=True)
