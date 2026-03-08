import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

#Set browser tab title and layout setting
st.set_page_config(page_title="Mein Wohlfühl-Münster", layout="wide")

#Anlegen der Pfade
DATA_PATH = Path("data/streets.geojson")
HTML_PATH = Path("frontend/map.html")

#Catch missing data exceptions
if not DATA_PATH.exists():
    st.error("Missing data/streets.geojson. Export it from your notebook first.")
    st.stop()

if not HTML_PATH.exists():
    st.error("Missing frontend/map.html.")
    st.stop()

#Cache loading (performance improvement for big geojson)
def load_geojson(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))

#load local streets data (exported from colab)
geojson = load_geojson(str(DATA_PATH))

#configuration of all the factor items
FACTOR_CFG = {
    "has_lamp":     {"label": "💡 Straßenbeleuchtung", "weight": 3, "default": True},
    "has_bus":      {"label": "🚌 Buslinie",           "weight": 1.0, "default": True},
    "has_bus_stop": {"label": "🚏 Haltestelle",        "weight": 1.0, "default": True},
    "has_accident": {"label": "💥 Unfälle",           "weight": -0.5, "default": True},
    "has_police":   {"label": "👮‍♂️ Polizei",         "weight": 1.5, "default": True},
    "has_taxi":     {"label": "🚕 Taxi",               "weight": 1.0, "default": True},
    "has_noise":    {"label": "🔊 Lärm",               "weight": -0.5, "default": False},
}

#Create dictionaries with the corresponding values for selection state, weights, and the labels
cfg_payload = {
    "selected": {k: v["default"] for k, v in FACTOR_CFG.items()},
    "weights": {k: v["weight"] for k, v in FACTOR_CFG.items()},
    "factorLabels": {k: v["label"] for k, v in FACTOR_CFG.items()},
}

#Load html from other file
html = HTML_PATH.read_text(encoding="utf-8")
#Inject html with data
html = html.replace("__STREETS__", json.dumps(geojson)).replace("__CFG__", json.dumps(cfg_payload))

#Set map title
st.title("Mein Wohlfühl-Münster")
components.html(html, height=900, scrolling=False)