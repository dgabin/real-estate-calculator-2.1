import streamlit as st
import pandas as pd
import plotly.express as px
from logic import calculate_payment_plan
from pdf_generator import generar_pdf  # <--- IMPORTANTE: Importar el generador

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Calculadora Inmobiliaria",
    page_icon="🏢",
    layout="wide"
)

# --- Barra Lateral: Entradas (Inputs) ---
st.sidebar.header("Detalles de la Propiedad")

price = st.sidebar.number_input(
    "Precio de la Propiedad ($)", 
    min_value=0.0, 
    value=150000.0, 
    step=1000.0,
    format="%.2f"
)

separation = st.sidebar.number_input(
    "Separación / Reserva ($)", 
    min_value=0.0, 
    value=2000.0, 
    step=100.0
)

st.sidebar.markdown("---")
st.sidebar.header("Plan de Pagos")

initial_percent = st.sidebar.number_input(
    "% Inicial a la Firma", 
    min_value=0.0, 
    max_value=100.0, 
    value=10.0,
    step=0.5,
    help="Porcentaje que se debe completar al firmar contrato (usualmente 10%). Poner 0 si solo se requiere separación."
)

total_construction_percent = st.sidebar.number_input(
    "% Total Durante Construcción", 
    min_value=0.0, 
    max_value=100.0, 
    value=30.0,
    step=0.5,
    help="Porcentaje total pagado antes de la entrega final (incluye el inicial)."
)

months = st.sidebar.number_input(
    "Meses para Pagar (Construcción)", 
    min_value=1, 
    value=24, 
    step=1
)

# --- Lógica Principal ---

st.title("🏗️ Calculadora de Pagos: Pre-Construcción")
st.markdown("Calcule las cuotas mensuales para propiedades en plano.")

# Llamar a la función de lógica
result = calculate_payment_plan(
    price, 
    separation, 
    initial_percent, 
    total_construction_percent, 
    months
)

# Manejo de Errores
if "error" in result:
    st.error(f"⚠️ {result['error']}")
else:
    summary = result["summary"]
    
    # --- Sección 1: Métricas Clave (Tarjetas) ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="A Completar en Firma", 
            value=f"${summary['due_at_signing']:,.2f}",
            delta=f"Meta Inicial: {result['percentages']['initial_target']}%"
        )
        
    with col2:
        st.metric(
            label="Cuota Mensual", 
            value=f"${summary['monthly_payment']:,.2f}",
            delta=f"{months} Meses"
        )
        
    with col3:
        st.metric(
            label="Contra Entrega (Final)", 
            value=f"${summary['final_payment']:,.2f}",
            delta="Al recibir la llave"
        )

    st.markdown("---")

    # --- Sección 2: Gráfico Visual ---
    st.subheader("💰 Desglose de Pagos")

    chart_data = pd.DataFrame({
        "Etapa": ["Separación", "Completivo Firma", "Cuotas Mensuales (Total)", "Contra Entrega"],
        "Monto": [
            summary['separation_paid'],
            summary['due_at_signing'],
            summary['total_during_construction'],
            summary['final_payment']
        ]
    })

    fig = px.bar(
        chart_data, 
        x="Etapa", 
        y="Monto", 
        text_auto='.2s',
        title="Estructura de Pagos",
        color="Etapa",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Sección 3: Tabla Detallada ---
    with st.expander("Ver Tabla Detallada"):
        st.table(pd.DataFrame({
            "Concepto": [
                "Precio Total Propiedad",
                "Separación (Pagado Ya)",
                "Completivo a la Firma",
                "Total en Cuotas Mensuales",
                "Pago Final (Financiamiento/Cash)"
            ],
            "Monto": [
                f"${summary['property_price']:,.2f}",
                f"${summary['separation_paid']:,.2f}",
                f"${summary['due_at_signing']:,.2f}",
                f"${summary['total_during_construction']:,.2f}",
                f"${summary['final_payment']:,.2f}"
            ]
        }))

    # --- Sección 4: Botón de PDF ---
    st.markdown("---")
    st.subheader("📄 Exportar")

    pdf_file = generar_pdf(summary, result['percentages'])

    st.download_button(
        label="📥 Descargar Plan de Pagos (PDF)",
        data=pdf_file,
        file_name="plan_de_pagos.pdf",
        mime="application/pdf",
        type="primary"
    )
