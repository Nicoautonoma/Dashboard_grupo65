
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Tienda de Conveniencia", layout="wide")

# Título
st.title("📊 Dashboard de Ventas - Tienda de Conveniencia")
st.markdown("### Análisis basado en datos de ventas simuladas (supermarket_sales.csv)")

# Carga de datos
df = pd.read_csv("supermarket_sales.csv")

# Conversión de fecha
df["Date"] = pd.to_datetime(df["Date"])

# Filtros
col1, col2 = st.columns(2)
with col1:
    ciudad = st.selectbox("Selecciona una ciudad", options=df["City"].unique())
with col2:
    linea_producto = st.selectbox("Selecciona una línea de producto", options=df["Product line"].unique())

df_filtro = df[(df["City"] == ciudad) & (df["Product line"] == linea_producto)]

# KPIs
ventas_totales = df_filtro["Total"].sum()
promedio_rating = df_filtro["Rating"].mean()
ingresos_brutos = df_filtro["gross income"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas Totales", f"${ventas_totales:,.2f}")
col2.metric("⭐ Rating Promedio", f"{promedio_rating:.2f}")
col3.metric("📈 Ingreso Bruto", f"${ingresos_brutos:,.2f}")

# Gráfica: Ventas por Fecha
ventas_por_fecha = df_filtro.groupby("Date")["Total"].sum()

st.subheader(f"🗓️ Ventas Diarias en {ciudad} - {linea_producto}")
st.line_chart(ventas_por_fecha)

# Tabla de datos
st.subheader("📋 Vista tabular de los datos filtrados")
st.dataframe(df_filtro)
