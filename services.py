import json
import os
import hashlib
import pandas as pd
from datetime import datetime

# ==============================
# 📁 CONFIGURAÇÃO
# ==============================

ARQUIVO_USUARIOS = "usuarios.json"
PASTA_DADOS = "data"


# ==============================
# 🔐 LOGIN / USUÁRIOS
# ==============================

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f)

    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)


def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def criar_conta(usuario, senha):
    usuarios = carregar_usuarios()

    if usuario in usuarios:
        return False

    usuarios[usuario] = hash_senha(senha)
    salvar_usuarios(usuarios)

    # Criar arquivo individual do usuário
    os.makedirs(PASTA_DADOS, exist_ok=True)

    with open(f"{PASTA_DADOS}/{usuario}.json", "w") as f:
        json.dump({"produtos": [], "movimentacoes": []}, f, indent=4)

    return True


def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()
    return usuario in usuarios and usuarios[usuario] == hash_senha(senha)


# ==============================
# 📦 DADOS DO USUÁRIO
# ==============================

def carregar_dados_usuario(usuario):
    caminho = f"{PASTA_DADOS}/{usuario}.json"

    if not os.path.exists(caminho):
        return {"produtos": [], "movimentacoes": []}

    with open(caminho, "r") as f:
        return json.load(f)


def salvar_dados_usuario(usuario, dados):
    os.makedirs(PASTA_DADOS, exist_ok=True)

    with open(f"{PASTA_DADOS}/{usuario}.json", "w") as f:
        json.dump(dados, f, indent=4)


# ==============================
# 📦 PRODUTOS
# ==============================

def inserir_produto(usuario, nome, categoria, estoque_minimo, quantidade):
    dados = carregar_dados_usuario(usuario)

    novo_produto = {
        "id": len(dados["produtos"]) + 1,
        "nome": nome,
        "categoria": categoria,
        "estoque_minimo": estoque_minimo,
        "em_estoque": quantidade
    }

    dados["produtos"].append(novo_produto)
    salvar_dados_usuario(usuario, dados)


def atualizar_produto(usuario, produto_id, nome, categoria, estoque_minimo, quantidade):
    dados = carregar_dados_usuario(usuario)

    for produto in dados["produtos"]:
        if produto["id"] == produto_id:
            produto["nome"] = nome
            produto["categoria"] = categoria
            produto["estoque_minimo"] = estoque_minimo
            produto["em_estoque"] = quantidade
            break

    salvar_dados_usuario(usuario, dados)


def excluir_produto(usuario, produto_id):
    dados = carregar_dados_usuario(usuario)

    dados["produtos"] = [
        p for p in dados["produtos"] if p["id"] != produto_id
    ]

    salvar_dados_usuario(usuario, dados)


# ==============================
# 🔄 MOVIMENTAÇÕES
# ==============================

def registrar_movimentacao(usuario, produto_id, tipo, quantidade):
    dados = carregar_dados_usuario(usuario)

    for produto in dados["produtos"]:
        if produto["id"] == produto_id:
            if tipo == "ENTRADA":
                produto["em_estoque"] += quantidade
            elif tipo == "SAIDA":
                produto["em_estoque"] -= quantidade

    movimentacao = {
        "produto_id": produto_id,
        "tipo": tipo,
        "quantidade": quantidade,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    dados["movimentacoes"].append(movimentacao)

    salvar_dados_usuario(usuario, dados)


# ==============================
# 📊 DASHBOARD / ANÁLISE
# ==============================

def produtos_para_dataframe(usuario):
    dados = carregar_dados_usuario(usuario)
    df = pd.DataFrame(dados["produtos"])

    if not df.empty:
        df["status"] = df.apply(
            lambda row: "alerta"
            if row["em_estoque"] <= row["estoque_minimo"]
            else "ok",
            axis=1
        )
        df["falta"] = df["estoque_minimo"] - df["em_estoque"]

    return df


def produtos_em_alerta(df):
    if df.empty:
        return df
    return df[df["status"] == "alerta"]


def produtos_ok(df):
    if df.empty:
        return df
    return df[df["status"] == "ok"]


def produto_mais_critico(df):
    df_alerta = produtos_em_alerta(df)

    if df_alerta.empty:
        return None

    return df_alerta.sort_values(by="falta", ascending=False).iloc[0]

def historico_para_dataframe(usuario):
    dados = carregar_dados_usuario(usuario)

    produtos = dados["produtos"]
    movimentacoes = dados["movimentacoes"]

    if not movimentacoes:
        return pd.DataFrame()

    df_mov = pd.DataFrame(movimentacoes)
    df_prod = pd.DataFrame(produtos)

    df_final = df_mov.merge(
        df_prod[["id", "nome"]],
        left_on="produto_id",
        right_on="id",
        how="left"
    )

    df_final = df_final.rename(columns={"nome": "produto"})

    # 🔥 Se não existir coluna data, criar automaticamente
    if "data" not in df_final.columns:
        df_final["data"] = "Registro antigo"

    df_final = df_final[["produto", "tipo", "quantidade", "data"]]

    return df_final.sort_values(by="data", ascending=False)