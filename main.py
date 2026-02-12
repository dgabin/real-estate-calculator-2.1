import streamlit as st
import pandas as pd
import plotly.express as px
from logic import calculate_payment_plan, calculate_mortgage
from pdf_generator import generar_pdf

st.set_page_config(page_title="Calculadora Inmobiliaria", page_icon="🏢", layout="wide")

# --- Sidebar ---
st.sidebar.header("1. Fase de Construcción")
price = st.sidebar.number_input("Precio Propiedad ($)", min_value=0.0, value=150000.0, step=1000.0, format="%.2f")
separation = st.sidebar.number_input("Separación ($)", min_value=0.0, value=2000.0, step=100.0)

initial_percent = st.sidebar.number_input("% Firma Contrato", min_value=0.0, max_value=100.0, value=10.0, step=0.5)
total_construction_percent = st.sidebar.number_input("% Total Durante Construcción", min_value=0.0, max_value=100.0, value=30.0, step=0.5)
months = st.sidebar.number_input("Meses Construcción", min_value=1, value=24, step=1)

st.sidebar.markdown("---")
st.sidebar.header("2. Fase de Financiamiento")
interest_rate = st.sidebar.number_input("Tasa de Interés Anual (%)", min_value=0.0, value=11.5, step=0.25, help="Tasa promedio actual en bancos.")
loan_years = st.sidebar.number_input("Plazo del Préstamo (Años)", min_value=1, value=20, step=1)
insurance_rate = st.sidebar.number_input("Seguro Anual Estimado (%)", min_value=0.0, value=0.9, step=0.1, help="Seguro de vida e incendio (aprox 0.8% - 1.2% del préstamo).")

# --- Lógica ---
result = calculate_payment_plan(price, separation, initial_percent, total_construction_percent, months)

if "error" in result:
    st.error(result["error"])
else:
    summary = result["summary"]
    # Calcular Hipoteca basada en el monto final
    mortgage = calculate_mortgage(summary['final_payment'], interest_rate, loan_years, insurance_rate)

    st.title("🏢 Calculadora Inmobiliaria Integral")
    
    # --- FASE 1: Construcción ---
    st.header("Fase 1: Durante la Construcción")
    c1, c2, c3 = st.columns(3)
    c1.metric("A Completar en Firma", f"${summary['due_at_signing']:,.2f}")
    c2.metric("Cuota Mensual (Construcción)", f"${summary['monthly_payment']:,.2f}", f"{months} Meses")
    c3.metric("Monto a Financiar", f"${summary['final_payment']:,.2f}", "Contra Entrega")

    # --- FASE 2: Financiamiento ---
    st.markdown("---")
    st.header("Fase 2: Financiamiento Bancario")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Cuota Banco (Capital+Interés)", f"${mortgage['monthly_principal_interest']:,.2f}")
    m2.metric("Seguros Estimados", f"${mortgage['monthly_insurance']:,.2f}", f"{insurance_rate}% Anual")
    m3.metric("CUOTA TOTAL MENSUAL", f"${mortgage['monthly_total']:,.2f}", "Aprox. Banco")

    # --- Gráfico ---
    st.markdown("---")
    st.subheader("Flujo de Caja del Cliente")
    chart_data = pd.DataFrame({
        "Etapa": ["Firma Contrato", "Cuota Construcción", "Cuota Banco (Futura)"],
        "Monto Mensual": [
            summary['due_at_signing'], # Un solo pago, pero sirve de referencia visual
            summary['monthly_payment'],
            mortgage['monthly_total']
        ]
    })
    
    fig = px.bar(chart_data, x="Etapa", y="Monto Mensual", title="Comparativa de Pagos", text_auto="$.2s", color="Etapa")
    st.plotly_chart(fig, use_container_width=True)

    # --- PDF ---
    st.markdown("---")
    # Pasamos AMBOS resultados al generador de PDF
    pdf_file = generar_pdf(summary, result['percentages'], mortgage)

    st.download_button(
        label="📥 Descargar Análisis Completo (PDF)",
        data=pdf_file,
        file_name="analisis_inmobiliario.pdf",
        mime="application/pdf",
        type="primary"
    )
