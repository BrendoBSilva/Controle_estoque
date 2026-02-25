import streamlit as st
import pandas as pd
import altair as alt
from services import *

st.set_page_config(layout="wide")

# =============================
# 🔐 LOGIN
# =============================

if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:

    st.title("🔐 Sistema de Login")
    opcao = st.radio("Escolha:", ["Login", "Criar Conta"])

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if opcao == "Login":
        if st.button("Entrar"):
            if verificar_login(usuario, senha):
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.success("Login realizado!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

    else:
        if st.button("Criar Conta"):
            if criar_conta(usuario, senha):
                st.success("Conta criada com sucesso!")
            else:
                st.warning("Usuário já existe.")

    st.stop()

# =============================
# 📦 SISTEMA
# =============================

usuario = st.session_state.usuario
df = produtos_para_dataframe(usuario)

st.sidebar.title(f"📦 Estoque - {usuario}")

menu = st.sidebar.selectbox(
    "Navegação",
    [
        "🏠 Dashboard",
        "➕ Cadastrar Produto",
        "🔄 Movimentação",
        "⚙️ Gerenciar Produtos",
        "📋 Histórico",
        "🚪 Logout"
    ]
)

# ================= DASHBOARD =================
if menu == "🏠 Dashboard":

    st.title("📊 Dashboard")

    if df.empty:
        st.info("Nenhum produto cadastrado.")
    else:
        col1, col2, col3 = st.columns(3)

        col1.metric("📦 Produtos", len(df))
        col2.metric("📊 Total em estoque", df["em_estoque"].sum())
        col3.metric("⚠️ Em alerta", len(produtos_em_alerta(df)))

        st.divider()

        categoria_df = (
            df.groupby("categoria")["em_estoque"]
            .sum()
            .reset_index()
        )

        chart = alt.Chart(categoria_df).mark_bar().encode(
            x="categoria",
            y="em_estoque",
            tooltip=["categoria", "em_estoque"]
        ).interactive()

        st.altair_chart(chart, use_container_width=True)

        st.divider()
        st.dataframe(df, use_container_width=True)

# ================= CADASTRO =================
elif menu == "➕ Cadastrar Produto":

    st.title("➕ Cadastro de Produto")

    with st.form("form_produto"):
        nome = st.text_input("Nome do Produto")
        categoria = st.text_input("Categoria")
        estoque_minimo = st.number_input("Estoque Mínimo", min_value=0)
        quantidade = st.number_input("Quantidade Inicial", min_value=0)

        submit = st.form_submit_button("Cadastrar")

        if submit and nome and categoria:
            inserir_produto(usuario, nome, categoria, estoque_minimo, quantidade)
            st.success("Produto cadastrado!")
            st.rerun()

# ================= MOVIMENTAÇÃO =================
elif menu == "🔄 Movimentação":

    st.title("🔄 Movimentação")

    if df.empty:
        st.info("Nenhum produto cadastrado.")
    else:
        produto_id = st.selectbox(
            "Produto",
            df["id"],
            format_func=lambda x: df[df["id"] == x]["nome"].values[0]
        )

        tipo = st.radio("Tipo", ["ENTRADA", "SAIDA"])
        quantidade = st.number_input("Quantidade", min_value=1)

        if st.button("Registrar"):
            registrar_movimentacao(usuario, produto_id, tipo, quantidade)
            st.success("Movimentação registrada!")
            st.rerun()

# ================= GERENCIAR =================
elif menu == "⚙️ Gerenciar Produtos":

    st.title("⚙️ Gerenciar Produtos")

    if df.empty:
        st.info("Nenhum produto cadastrado.")
    else:
        produto_id = st.selectbox(
            "Produto",
            df["id"],
            format_func=lambda x: df[df["id"] == x]["nome"].values[0]
        )

        produto = df[df["id"] == produto_id].iloc[0]

        with st.form("editar"):
            nome = st.text_input("Nome", value=produto["nome"])
            categoria = st.text_input("Categoria", value=produto["categoria"])
            minimo = st.number_input("Estoque Mínimo", value=int(produto["estoque_minimo"]))
            quantidade = st.number_input("Quantidade", value=int(produto["em_estoque"]))

            col1, col2 = st.columns(2)
            atualizar = col1.form_submit_button("Atualizar")
            excluir = col2.form_submit_button("Excluir")

            if atualizar:
                atualizar_produto(usuario, produto_id, nome, categoria, minimo, quantidade)
                st.success("Atualizado!")
                st.rerun()

            if excluir:
                excluir_produto(usuario, produto_id)
                st.warning("Excluído!")
                st.rerun()

# ================= HISTÓRICO =================
elif menu == "📋 Histórico":

    st.title("📋 Histórico de Movimentações")

    historico = historico_para_dataframe(usuario)

    if historico.empty:
        st.info("Nenhuma movimentação registrada.")
    else:
        st.dataframe(historico, use_container_width=True)

# ================= LOGOUT =================
elif menu == "🚪 Logout":

    st.session_state.logado = False
    st.session_state.usuario = None
    st.rerun()