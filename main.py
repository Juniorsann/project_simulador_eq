import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Process Chemical Simulator", layout="wide")
st.title("Simulador cinético e de processos químicos")

# --- Sidebar para configuração ---
st.sidebar.header("Escolha a operação")
op = st.sidebar.selectbox("Operação", ["Reatores", "Trocador de Calor", "Destilação"])

# --- Inputs do reator ---
if op == "Reatores":
    st.sidebar.subheader("Tipo de Reator")
    tipo_reator = st.sidebar.selectbox("Modelo cinético", ["Batch", "CSTR", "PFR", "Série", "Paralelo", "Reversível"])
    CA0 = st.sidebar.number_input("Conc. inicial A (mol/L)", 0.1, 10.0, 4.0)
    k = st.sidebar.number_input("Const. velocidade k (1/h)", 0.01, 3.0, 0.5)
    k2 = st.sidebar.number_input("Const. velocidade k2 (paralelo/reversível/2° reator)", 0.0, 3.0, 0.0)
    Q = st.sidebar.number_input("Vazão (L/h)", 10, 10000, 1000)
    tempo_resid = st.sidebar.number_input("Tempo ou tempo de residência (h)", 0.1, 48.0, 10.0)
    conv_desejada = st.sidebar.slider("Conversão desejada (%)", 10, 99, 90)/100

    t = np.linspace(0, tempo_resid, 100)

    if tipo_reator=="Batch":
        CA = CA0 * np.exp(-k * t)
        df = pd.DataFrame({'Tempo (h)': t, 'CA (mol/L)': CA})
        st.line_chart(df.set_index('Tempo (h)'))
        # Resultados finais
        CA_final = CA[-1]
        conversao = 1 - CA_final/CA0 if CA0 > 0 else np.nan
        st.subheader(f"Resultados finais após {tempo_resid:.1f} h")
        col1, col2 = st.columns(2)
        col1.metric("CA final (mol/L)", f"{CA_final:.3f}")
        col2.metric("Conversão (%)", f"{conversao*100:.1f}")

    elif tipo_reator=="CSTR":
        CA = CA0 / (1 + k * t)
        df = pd.DataFrame({'Tempo de residência (h)': t, 'CA (mol/L)': CA})
        st.line_chart(df.set_index('Tempo de residência (h)'))
        CA_final = CA[-1]
        conversao = 1 - CA_final/CA0 if CA0 > 0 else np.nan
        st.subheader(f"Resultados finais para tempo de residência {tempo_resid:.1f} h")
        col1, col2 = st.columns(2)
        col1.metric("CA final (mol/L)", f"{CA_final:.3f}")
        col2.metric("Conversão (%)", f"{conversao*100:.1f}")

    elif tipo_reator=="PFR":
        CA = CA0 * np.exp(-k * t)
        df = pd.DataFrame({'Tempo de residência (h)': t, 'CA (mol/L)': CA})
        st.line_chart(df.set_index('Tempo de residência (h)'))
        CA_final = CA[-1]
        conversao = 1 - CA_final/CA0 if CA0 > 0 else np.nan
        st.subheader(f"Resultados finais para tempo de residência {tempo_resid:.1f} h")
        col1, col2 = st.columns(2)
        col1.metric("CA final (mol/L)", f"{CA_final:.3f}")
        col2.metric("Conversão (%)", f"{conversao*100:.1f}")

    elif tipo_reator=="Série":
        # Dois reatores em série (k = 1º, k2 = 2º)
        CA_S1 = CA0 * np.exp(-k * t)
        CA_S2 = CA_S1 * np.exp(-k2 * t) if k2 > 0 else CA_S1
        df = pd.DataFrame({'Tempo (h)': t, 'Reator 1 (CA1)': CA_S1, 'Reator 2 (CA2)': CA_S2})
        st.line_chart(df.set_index('Tempo (h)'))
        CA1_final = CA_S1[-1]
        CA2_final = CA_S2[-1]
        conv1 = 1 - CA1_final/CA0 if CA0 > 0 else np.nan
        conv2 = 1 - CA2_final/CA0 if CA0 > 0 else np.nan
        st.subheader(f"Resultados finais após {tempo_resid:.1f} h")
        col1, col2, col3 = st.columns(3)
        col1.metric("CA1 final (mol/L)", f"{CA1_final:.3f}")
        col2.metric("CA2 final (mol/L)", f"{CA2_final:.3f}")
        col3.metric("Conversão global (%)", f"{conv2*100:.1f}")

    elif tipo_reator=="Paralelo":
        # A → B (k), A → C (k2)
        if (k + k2) > 0:
            CA = CA0 * np.exp(-(k + k2) * t)
            CB = CA0 * k / (k + k2) * (1 - np.exp(-(k + k2) * t))
            CC = CA0 * k2 / (k + k2) * (1 - np.exp(-(k + k2) * t))
        else:
            CA = np.full_like(t, CA0)
            CB = np.zeros_like(t)
            CC = np.zeros_like(t)
        df = pd.DataFrame({'Tempo (h)': t, 'CA': CA, 'CB': CB, 'CC': CC})
        st.line_chart(df.set_index('Tempo (h)'))
        # Resultados finais
        CA_final, CB_final, CC_final = CA[-1], CB[-1], CC[-1]
        conversao = 1 - CA_final/CA0 if CA0 > 0 else np.nan
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("CA final (mol/L)", f"{CA_final:.3f}")
        col2.metric("CB final (mol/L)", f"{CB_final:.3f}")
        col3.metric("CC final (mol/L)", f"{CC_final:.3f}")
        col4.metric("Conversão de A (%)", f"{conversao*100:.1f}")

    elif tipo_reator=="Reversível":
        def diffs(y, t, kf, kr):
            CA, CB = y
            dydt = [-kf * CA + kr * CB, kf * CA - kr * CB]
            return dydt
        y0 = [CA0, 0]
        sol = odeint(diffs, y0, t, args=(k, k2))
        CA = sol[:, 0]
        CB = sol[:, 1]
        df = pd.DataFrame({'Tempo (h)': t, 'A': CA, 'B': CB})
        st.line_chart(df.set_index('Tempo (h)'))
        CA_final = CA[-1]
        CB_final = CB[-1]
        conversao = 1 - CA_final/CA0 if CA0 > 0 else np.nan
        col1, col2, col3 = st.columns(3)
        col1.metric("A final (mol/L)", f"{CA_final:.3f}")
        col2.metric("B final (mol/L)", f"{CB_final:.3f}")
        col3.metric("Conversão de A (%)", f"{conversao*100:.1f}")

    # --- Upload e ajuste de dados experimentais ---
    st.markdown("#### Ajuste de dados experimentais (diferencial!)")
    uploaded_file = st.file_uploader("Upload do CSV experimental (tempos, CA, CB ...)")
    if uploaded_file is not None:
        df_exp = pd.read_csv(uploaded_file)
        st.write("Dados experimentais:", df_exp.head())
        # Exemplo: ajuste linear para reações de 1a ordem (ln(CA) vs t)
        if 'CA' in df_exp.columns and 'tempo' in df_exp.columns:
            lnCA = np.log(df_exp['CA'])
            model = LinearRegression()
            model.fit(df_exp[['tempo']], lnCA)
            k_fit = -model.coef_[0]
            st.success(f"Constante ajustada (k): {k_fit:.3f} 1/h")
            fig, ax = plt.subplots()
            ax.scatter(df_exp['tempo'], lnCA, label='ln CA exp')
            ax.plot(df_exp['tempo'], model.predict(df_exp[['tempo']]), 'r--', label='Ajuste')
            ax.set_xlabel('Tempo (h)')
            ax.set_ylabel('ln(CA)')
            ax.legend()
            st.pyplot(fig)


# --- Módulos para outras operações unitárias ---
if op == "Trocador de Calor":
    st.write("Em breve: cálculo de trocadores de calor (balanço de energia, dimensionamento)...")
if op == "Destilação":
    st.write("Em breve: Selecione tipo de destilação (simples, flash, multicomponente)...")

# # --- Painel de otimização multiobjetivo (diferencial!) ---
# st.markdown("#### Simulação multiobjetivo e análise de sensibilidade")
# if op == "Reatores":
#     st.write("(Futuro) Otimize parâmetros para máximo Lucro, Conversão, Sustentabilidade, etc...")

st.markdown("---")
st.caption("Simulador modular & robusto • Python • Engenharia Química • Ciência de Dados • Machine Learning")