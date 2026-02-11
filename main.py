# main.py
import streamlit as st
import pandas as pd
import plotly.express as px  # For the interactive graph
from logic import calculate_payment_plan

# --- Page Configuration ---
st.set_page_config(
    page_title="Real Estate Payment Calculator",
    page_icon="🏢",
    layout="wide"
)

# --- Sidebar: User Inputs ---
st.sidebar.header("Property Details")

# Using 'number_input' for precise amounts
price = st.sidebar.number_input(
    "Property Price ($)", 
    min_value=0.0, 
    value=150000.0, 
    step=1000.0,
    format="%.2f"
)

separation = st.sidebar.number_input(
    "Separation Fee ($)", 
    min_value=0.0, 
    value=2000.0, 
    step=100.0
)

st.sidebar.markdown("---")
st.sidebar.header("Payment Terms")

# Initial % (Contract Signing) - Default 10%
initial_percent = st.sidebar.slider(
    "Initial Down Payment (%)", 
    min_value=0.0, 
    max_value=100.0, 
    value=10.0,
    help="0% if only Separation is required to sign."
)

# Total Construction % - Default 30%
total_construction_percent = st.sidebar.slider(
    "Total Construction Equity (%)", 
    min_value=initial_percent, 
    max_value=100.0, 
    value=30.0,
    help="Total % paid before final delivery (includes initial)."
)

months = st.sidebar.number_input(
    "Months to Pay (Construction Duration)", 
    min_value=1, 
    value=24, 
    step=1
)

# --- Main App Logic ---

st.title("🏗️ Pre-Construction Payment Calculator")
st.markdown("Calculate monthly installments for off-plan properties.")

# Call the logic function
result = calculate_payment_plan(
    price, 
    separation, 
    initial_percent, 
    total_construction_percent, 
    months
)

# Error Handling
if "error" in result:
    st.error(result["error"])
else:
    # Extract data for easier reading
    summary = result["summary"]
    
    # --- Section 1: Key Metrics (The "Cards") ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Due at Signing", 
            value=f"${summary['due_at_signing']:,.2f}",
            delta=f"Initial {result['percentages']['initial_target']}%"
        )
        
    with col2:
        st.metric(
            label="Monthly Payment", 
            value=f"${summary['monthly_payment']:,.2f}",
            delta=f"{months} Months"
        )
        
    with col3:
        st.metric(
            label="Final Payment (Contra Entrega)", 
            value=f"${summary['final_payment']:,.2f}",
            delta="Due on Delivery"
        )

    st.markdown("---")

    # --- Section 2: The Visual Graph ---
    st.subheader("💰 Payment Breakdown")

    # Prepare data for the chart
    chart_data = pd.DataFrame({
        "Stage": ["Separation", "Contract Signing", "During Construction (Total)", "Final Payment"],
        "Amount": [
            summary['separation_paid'],
            summary['due_at_signing'],
            summary['total_during_construction'],
            summary['final_payment']
        ]
    })

    # Create a nice bar chart using Plotly
    fig = px.bar(
        chart_data, 
        x="Stage", 
        y="Amount", 
        text_auto='.2s',
        title="Payment Structure Visualization",
        color="Stage",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Section 3: Detailed Summary Table ---
    with st.expander("See Detailed Breakdown"):
        st.table(pd.DataFrame({
            "Description": [
                "Total Property Price",
                "Separation Fee (Paid Now)",
                "Due at Signing (Initial % - Sep)",
                "Monthly Installments (Total)",
                "Final Payment (Financing/Cash)"
            ],
            "Amount": [
                f"${summary['property_price']:,.2f}",
                f"${summary['separation_paid']:,.2f}",
                f"${summary['due_at_signing']:,.2f}",
                f"${summary['total_during_construction']:,.2f}",
                f"${summary['final_payment']:,.2f}"
            ]
        }))
