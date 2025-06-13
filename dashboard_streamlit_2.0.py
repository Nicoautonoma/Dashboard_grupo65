
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard Grupo 65", layout="wide")
st.title("📊 Análisis de Ventas - Tienda de Conveniencia")

# Cargar datos
df = pd.read_csv("supermarket_sales.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Month"] = df["Date"].dt.to_period("M")

# Filtros
with st.sidebar:
    st.header("🔎 Filtros")
    ciudad = st.selectbox("Ciudad", df["City"].unique())
    genero = st.selectbox("Género", df["Gender"].unique())
    tipo_cliente = st.selectbox("Tipo de Cliente", df["Customer type"].unique())

df_filtro = df[(df["City"] == ciudad) & (df["Gender"] == genero) & (df["Customer type"] == tipo_cliente)]

# 1. Visualización Básica de Datos
st.subheader("1️⃣ Visualización Básica de Datos")

tab1, tab2, tab3, tab4 = st.tabs(["Tendencia de Ventas", "Distribución de Ventas", "Boxplot por Producto", "Cantidad vs Total"])

with tab1:
    st.markdown("**Tendencia de Ventas Totales**")
    ventas_dia = df.groupby("Date")["Total"].sum()
    fig, ax = plt.subplots()
    ventas_dia.plot(ax=ax)
    ax.set_title("Tendencia de Ventas Totales")
    ax.set_ylabel("Total")
    st.pyplot(fig)

with tab2:
    st.markdown("**Distribución de Montos Totales de Venta**")
    fig, ax = plt.subplots()
    sns.histplot(df["Total"], bins=30, kde=False, color="skyblue", ax=ax)
    ax.set_title("Distribución de Ventas Totales")
    st.pyplot(fig)

with tab3:
    st.markdown("**Ventas por Línea de Producto (Box Plot)**")
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x="Product line", y="Total", palette="pastel", ax=ax)
    ax.set_title("Ventas por Línea de Producto")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

with tab4:
    st.markdown("**Cantidad vs Total por Tipo de Cliente**")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x="Quantity", y="Total", hue="Customer type", palette="Set1", alpha=0.7, ax=ax)
    ax.set_title("Dispersión: Cantidad vs Total")
    st.pyplot(fig)

# 2. Gráficos Compuestos y Contextualización
st.subheader("2️⃣ Gráficos Compuestos y Contextualización")

tab5, tab6 = st.tabs(["Mapa de Calor por Sucursal y Producto", "Ventas Mensuales por Línea de Producto"])

with tab5:
    st.markdown("**Ventas por Línea de Producto y Sucursal (Heatmap)**")
    pivot = df.pivot_table(index="Product line", columns="Branch", values="Total", aggfunc="sum")
    fig, ax = plt.subplots()
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues", ax=ax)
    ax.set_title("Ventas por Línea de Producto y Sucursal")
    st.pyplot(fig)

with tab6:
    st.markdown("**Ventas Mensuales por Línea de Producto**")
    ventas_mensuales = df.groupby(["Month", "Product line"])["Total"].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 4))
    ventas_mensuales.plot(ax=ax)
    ax.set_title("Tendencia de Ventas Mensuales")
    ax.set_ylabel("Ventas")
    st.pyplot(fig)

# 3. Visualización Multivariada
st.subheader("3️⃣ Visualización Multivariada")

tab7, tab8 = st.tabs(["Matriz de Correlación", "Pair Plot"])

with tab7:
    st.markdown("**Matriz de Correlación**")
    numericas = df.select_dtypes(include="number")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(numericas.corr(), annot=True, cmap="coolwarm", ax=ax)
    ax.set_title("Matriz de Correlación entre Variables Numéricas")
    st.pyplot(fig)

with tab8:
    st.markdown("**Pair Plot: Precio, Cantidad y Total por Línea de Producto**")
    df_sample = df.sample(n=500, random_state=42)
    df_sample = df_sample[["Unit price", "Quantity", "Total", "Product line"]].dropna()
    df_sample = df_sample.astype({"Unit price": "float", "Quantity": "int", "Total": "float"})
    pair = sns.pairplot(df_sample, vars=["Unit price", "Quantity", "Total"], hue="Product line", diag_kind="hist", plot_kws={"alpha": 0.6})
    st.pyplot(pair)

# 4. Visualización 3D (opcional con plotly si se desea más adelante)
st.subheader("4️⃣ Visualización 3D (no incluida aquí por simplicidad, puede implementarse con Plotly)")

st.markdown("Este dashboard forma parte del trabajo del curso *Visualización de Información en la Era del Big Data* - Grupo 65.")
