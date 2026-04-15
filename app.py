"""Streamlit app for the Rappi Operational Intelligence Agent MVP."""

from pathlib import Path

import pandas as pd
import streamlit as st

OUTPUT_FILE = Path("data/output/enriched_restaurants_output.csv")
URGENCY_ORDER = ["Immediate", "Soon", "Low"]
LANG_OPTIONS = ["English", "Español", "Português"]

UI_TEXT = {
    "English": {
        "page_title": "Rappi Operational Intelligence Agent",
        "title": "Rappi Operational Intelligence Agent",
        "description": (
            "This MVP helps KAMs identify restaurants that need attention based on "
            "operational risk signals."
        ),
        "language_label": "Language",
        "missing_file_error": (
            "Enriched data file not found. Run `python -m src.recommendations` first "
            "to generate `data/output/enriched_restaurants_output.csv`."
        ),
        "kam_filter_label": "Filter by KAM",
        "all_kams": "All KAMs",
        "kpi_total": "Total Restaurants",
        "kpi_critical": "Critical",
        "kpi_at_risk": "At Risk",
        "kpi_stable": "Stable",
        "overview_header": "Restaurants Overview",
        "critical_header": "Critical Restaurants",
        "drilldown_header": "Restaurant Drill-down",
        "restaurant_select_label": "Select restaurant",
        "field_header": "Field",
        "value_header": "Value",
        "no_restaurants_info": "No restaurants available for the current filter.",
    },
    "Español": {
        "page_title": "Agente de Inteligencia Operacional Rappi",
        "title": "Agente de Inteligencia Operacional Rappi",
        "description": (
            "Este MVP ayuda a los KAMs a identificar restaurantes que requieren "
            "atención según señales de riesgo operacional."
        ),
        "language_label": "Idioma",
        "missing_file_error": (
            "No se encontró el archivo enriquecido. Ejecuta `python -m src.recommendations` "
            "para generar `data/output/enriched_restaurants_output.csv`."
        ),
        "kam_filter_label": "Filtrar por KAM",
        "all_kams": "Todos los KAMs",
        "kpi_total": "Restaurantes Totales",
        "kpi_critical": "Crítico",
        "kpi_at_risk": "En Riesgo",
        "kpi_stable": "Estable",
        "overview_header": "Resumen de Restaurantes",
        "critical_header": "Restaurantes Críticos",
        "drilldown_header": "Detalle del Restaurante",
        "restaurant_select_label": "Seleccionar restaurante",
        "field_header": "Campo",
        "value_header": "Valor",
        "no_restaurants_info": "No hay restaurantes disponibles para el filtro actual.",
    },
    "Português": {
        "page_title": "Agente de Inteligência Operacional Rappi",
        "title": "Agente de Inteligência Operacional Rappi",
        "description": (
            "Este MVP ajuda KAMs a identificar restaurantes que precisam de atenção "
            "com base em sinais de risco operacional."
        ),
        "language_label": "Idioma",
        "missing_file_error": (
            "Arquivo enriquecido não encontrado. Execute `python -m src.recommendations` "
            "para gerar `data/output/enriched_restaurants_output.csv`."
        ),
        "kam_filter_label": "Filtrar por KAM",
        "all_kams": "Todos os KAMs",
        "kpi_total": "Restaurantes Totais",
        "kpi_critical": "Crítico",
        "kpi_at_risk": "Em Risco",
        "kpi_stable": "Estável",
        "overview_header": "Visão Geral dos Restaurantes",
        "critical_header": "Restaurantes Críticos",
        "drilldown_header": "Detalhe do Restaurante",
        "restaurant_select_label": "Selecionar restaurante",
        "field_header": "Campo",
        "value_header": "Valor",
        "no_restaurants_info": "Não há restaurantes disponíveis para o filtro atual.",
    },
}

COLUMN_LABELS = {
    "English": {
        "restaurant_id": "Restaurant ID",
        "nombre": "Restaurant Name",
        "ciudad": "City",
        "vertical": "Vertical",
        "kam_asignado": "Assigned KAM",
        "risk_score": "Risk Score",
        "risk_level": "Risk Level",
        "urgency": "Urgency",
        "risk_drivers": "Risk Drivers",
        "recommended_action": "Recommended Action",
        "semaforo_riesgo": "Reference Risk Flag",
    },
    "Español": {
        "restaurant_id": "ID del restaurante",
        "nombre": "Restaurante",
        "ciudad": "Ciudad",
        "vertical": "Vertical",
        "kam_asignado": "KAM asignado",
        "risk_score": "Puntaje de riesgo",
        "risk_level": "Nivel de riesgo",
        "urgency": "Urgencia",
        "risk_drivers": "Señales de riesgo",
        "recommended_action": "Acción recomendada",
        "semaforo_riesgo": "Semáforo de referencia",
    },
    "Português": {
        "restaurant_id": "ID do restaurante",
        "nombre": "Restaurante",
        "ciudad": "Cidade",
        "vertical": "Vertical",
        "kam_asignado": "KAM responsável",
        "risk_score": "Pontuação de risco",
        "risk_level": "Nível de risco",
        "urgency": "Urgência",
        "risk_drivers": "Sinais de risco",
        "recommended_action": "Ação recomendada",
        "semaforo_riesgo": "Semáforo de referência",
    },
}

RISK_LEVEL_TRANSLATIONS = {
    "English": {"Stable": "Stable", "At Risk": "At Risk", "Critical": "Critical"},
    "Español": {"Stable": "Estable", "At Risk": "En Riesgo", "Critical": "Crítico"},
    "Português": {"Stable": "Estável", "At Risk": "Em Risco", "Critical": "Crítico"},
}

URGENCY_TRANSLATIONS = {
    "English": {"Low": "Low", "Soon": "Soon", "Immediate": "Immediate"},
    "Español": {"Low": "Baja", "Soon": "Pronto", "Immediate": "Inmediata"},
    "Português": {"Low": "Baixa", "Soon": "Em Breve", "Immediate": "Imediata"},
}

SEMAFORO_TRANSLATIONS = {
    "English": {"ESTABLE": "STABLE", "EN RIESGO": "AT RISK", "CRÍTICO": "CRITICAL"},
    "Español": {"ESTABLE": "ESTABLE", "EN RIESGO": "EN RIESGO", "CRÍTICO": "CRÍTICO"},
    "Português": {"ESTABLE": "ESTÁVEL", "EN RIESGO": "EM RISCO", "CRÍTICO": "CRÍTICO"},
}

RISK_DRIVER_TRANSLATIONS = {
    "English": {
        "No major risk signals": "No major risk signals",
        "Strong rating drop": "Strong rating drop",
        "High cancellation rate": "High cancellation rate",
        "Delivery delays": "Delivery delays",
        "Order volume decline": "Order volume decline",
        "Complaint spike": "Complaint spike",
        "Low NPS": "Low NPS",
    },
    "Español": {
        "No major risk signals": "Sin señales de riesgo relevantes",
        "Strong rating drop": "Caída fuerte en rating",
        "High cancellation rate": "Alta tasa de cancelación",
        "Delivery delays": "Retrasos en entrega",
        "Order volume decline": "Caída en volumen de órdenes",
        "Complaint spike": "Pico de quejas",
        "Low NPS": "NPS bajo",
    },
    "Português": {
        "No major risk signals": "Sem sinais relevantes de risco",
        "Strong rating drop": "Queda forte de avaliação",
        "High cancellation rate": "Alta taxa de cancelamento",
        "Delivery delays": "Atrasos na entrega",
        "Order volume decline": "Queda no volume de pedidos",
        "Complaint spike": "Pico de reclamações",
        "Low NPS": "NPS baixo",
    },
}

RECOMMENDED_ACTION_TRANSLATIONS = {
    "English": {
        "Contact the partner today to review customer experience issues and recent complaints.": (
            "Contact the partner today to review customer experience issues and recent complaints."
        ),
        "Review menu availability, prep flow, and operational bottlenecks with the partner.": (
            "Review menu availability, prep flow, and operational bottlenecks with the partner."
        ),
        "Review recent operational changes and monitor commercial impact over the next 48 hours.": (
            "Review recent operational changes and monitor commercial impact over the next 48 hours."
        ),
        "Check preparation and delivery bottlenecks and align on corrective actions with the partner.": (
            "Check preparation and delivery bottlenecks and align on corrective actions with the partner."
        ),
        "Review recent service quality issues and define a short-term recovery follow-up plan.": (
            "Review recent service quality issues and define a short-term recovery follow-up plan."
        ),
        "No immediate action required. Keep under routine monitoring.": (
            "No immediate action required. Keep under routine monitoring."
        ),
    },
    "Español": {
        "Contact the partner today to review customer experience issues and recent complaints.": (
            "Contacta al aliado hoy para revisar temas de experiencia de cliente y quejas recientes."
        ),
        "Review menu availability, prep flow, and operational bottlenecks with the partner.": (
            "Revisa la disponibilidad de menú, el flujo de preparación y cuellos de botella operativos con el aliado."
        ),
        "Review recent operational changes and monitor commercial impact over the next 48 hours.": (
            "Revisa cambios operativos recientes y monitorea el impacto comercial durante las próximas 48 horas."
        ),
        "Check preparation and delivery bottlenecks and align on corrective actions with the partner.": (
            "Verifica cuellos de botella de preparación y entrega y alinea acciones correctivas con el aliado."
        ),
        "Review recent service quality issues and define a short-term recovery follow-up plan.": (
            "Revisa problemas recientes de calidad de servicio y define un plan de seguimiento de recuperación a corto plazo."
        ),
        "No immediate action required. Keep under routine monitoring.": (
            "No se requiere acción inmediata. Mantener en monitoreo rutinario."
        ),
    },
    "Português": {
        "Contact the partner today to review customer experience issues and recent complaints.": (
            "Contate o parceiro hoje para revisar problemas de experiência do cliente e reclamações recentes."
        ),
        "Review menu availability, prep flow, and operational bottlenecks with the partner.": (
            "Revise disponibilidade do cardápio, fluxo de preparo e gargalos operacionais com o parceiro."
        ),
        "Review recent operational changes and monitor commercial impact over the next 48 hours.": (
            "Revise mudanças operacionais recentes e monitore o impacto comercial nas próximas 48 horas."
        ),
        "Check preparation and delivery bottlenecks and align on corrective actions with the partner.": (
            "Verifique gargalos de preparo e entrega e alinhe ações corretivas com o parceiro."
        ),
        "Review recent service quality issues and define a short-term recovery follow-up plan.": (
            "Revise problemas recentes de qualidade de serviço e defina um plano de acompanhamento de recuperação de curto prazo."
        ),
        "No immediate action required. Keep under routine monitoring.": (
            "Nenhuma ação imediata é necessária. Mantenha em monitoramento de rotina."
        ),
    },
}

if "language" not in st.session_state:
    st.session_state["language"] = "English"

st.set_page_config(
    page_title=UI_TEXT[st.session_state["language"]]["page_title"], layout="wide"
)


def t(key: str, language: str) -> str:
    return UI_TEXT[language][key]


def translate_risk_level(value: str, language: str) -> str:
    return RISK_LEVEL_TRANSLATIONS[language].get(value, value)


def translate_urgency(value: str, language: str) -> str:
    return URGENCY_TRANSLATIONS[language].get(value, value)


def translate_semaforo(value: str, language: str) -> str:
    if not isinstance(value, str):
        return value
    translated = value
    for raw, localized in SEMAFORO_TRANSLATIONS[language].items():
        translated = translated.replace(raw, localized)
    return translated


def translate_risk_drivers(value: str, language: str) -> str:
    if not isinstance(value, str):
        return value
    parts = [part.strip() for part in value.split(",")]
    translated = [
        RISK_DRIVER_TRANSLATIONS[language].get(part, part) for part in parts if part
    ]
    return ", ".join(translated)


def translate_recommended_action(value: str, language: str) -> str:
    if not isinstance(value, str):
        return value
    return RECOMMENDED_ACTION_TRANSLATIONS[language].get(value, value)


if not OUTPUT_FILE.exists():
    st.error(t("missing_file_error", st.session_state["language"]))
    st.stop()

df = pd.read_csv(OUTPUT_FILE)

language = st.selectbox(
    t("language_label", st.session_state["language"]),
    LANG_OPTIONS,
    index=LANG_OPTIONS.index(st.session_state["language"]),
)
st.session_state["language"] = language

st.title(t("title", language))
st.write(t("description", language))

kam_values = sorted(df["kam_asignado"].dropna().unique().tolist())
selected_kam = st.selectbox(t("kam_filter_label", language), [t("all_kams", language)] + kam_values)

filtered_df = df.copy()
if selected_kam != t("all_kams", language):
    filtered_df = filtered_df[filtered_df["kam_asignado"] == selected_kam].copy()

total_restaurants = len(filtered_df)
critical_count = (filtered_df["risk_level"] == "Critical").sum()
at_risk_count = (filtered_df["risk_level"] == "At Risk").sum()
stable_count = (filtered_df["risk_level"] == "Stable").sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric(t("kpi_total", language), int(total_restaurants))
col2.metric(t("kpi_critical", language), int(critical_count))
col3.metric(t("kpi_at_risk", language), int(at_risk_count))
col4.metric(t("kpi_stable", language), int(stable_count))

# Keep raw urgency for sorting, and add display-only translated fields.
filtered_df["urgency_sort"] = pd.Categorical(
    filtered_df["urgency"], categories=URGENCY_ORDER, ordered=True
)

sorted_df = filtered_df.sort_values(
    by=["urgency_sort", "risk_score"], ascending=[True, False]
).copy()

sorted_df["risk_level_display"] = sorted_df["risk_level"].apply(
    lambda value: translate_risk_level(value, language)
)
sorted_df["urgency_display"] = sorted_df["urgency"].apply(
    lambda value: translate_urgency(value, language)
)
sorted_df["risk_drivers_display"] = sorted_df["risk_drivers"].apply(
    lambda value: translate_risk_drivers(value, language)
)
sorted_df["recommended_action_display"] = sorted_df["recommended_action"].apply(
    lambda value: translate_recommended_action(value, language)
)
sorted_df["semaforo_riesgo_display"] = sorted_df["semaforo_riesgo"].apply(
    lambda value: translate_semaforo(value, language)
)

st.subheader(t("overview_header", language))
main_table = sorted_df[
    [
        "restaurant_id",
        "nombre",
        "ciudad",
        "kam_asignado",
        "risk_score",
        "risk_level_display",
        "urgency_display",
        "risk_drivers_display",
        "recommended_action_display",
    ]
].rename(
    columns={
        "risk_level_display": "risk_level",
        "urgency_display": "urgency",
        "risk_drivers_display": "risk_drivers",
        "recommended_action_display": "recommended_action",
    }
)
main_table = main_table.rename(columns=COLUMN_LABELS[language])
st.dataframe(main_table, use_container_width=True, hide_index=True)

st.subheader(t("critical_header", language))
critical_df = sorted_df[sorted_df["risk_level"] == "Critical"].copy()
critical_table = critical_df[
    [
        "restaurant_id",
        "nombre",
        "kam_asignado",
        "risk_score",
        "risk_drivers_display",
        "recommended_action_display",
    ]
].rename(
    columns={
        "risk_drivers_display": "risk_drivers",
        "recommended_action_display": "recommended_action",
    }
)
critical_table = critical_table.rename(columns=COLUMN_LABELS[language])
st.dataframe(critical_table, use_container_width=True, hide_index=True)

st.subheader(t("drilldown_header", language))
restaurant_names = sorted_df["nombre"].dropna().unique().tolist()

if restaurant_names:
    selected_restaurant = st.selectbox(t("restaurant_select_label", language), restaurant_names)
    detail_row = sorted_df[sorted_df["nombre"] == selected_restaurant].iloc[0]

    detail_pairs = [
        ("restaurant_id", detail_row["restaurant_id"]),
        ("nombre", detail_row["nombre"]),
        ("ciudad", detail_row["ciudad"]),
        ("vertical", detail_row["vertical"]),
        ("kam_asignado", detail_row["kam_asignado"]),
        ("risk_score", detail_row["risk_score"]),
        ("risk_level", detail_row["risk_level_display"]),
        ("urgency", detail_row["urgency_display"]),
        ("risk_drivers", detail_row["risk_drivers_display"]),
        ("recommended_action", detail_row["recommended_action_display"]),
        ("semaforo_riesgo", detail_row["semaforo_riesgo_display"]),
    ]
    detail_df = pd.DataFrame(
        {
            t("field_header", language): [
                COLUMN_LABELS[language].get(field, field) for field, _ in detail_pairs
            ],
            t("value_header", language): [value for _, value in detail_pairs],
        }
    )
    value_col = t("value_header", language)
    detail_df[value_col] = detail_df[value_col].astype(str)
    st.dataframe(detail_df, use_container_width=True, hide_index=True)
else:
    st.info(t("no_restaurants_info", language))
