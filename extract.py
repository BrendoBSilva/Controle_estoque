import pandas as pd
from db import connect

def extrair_estoque():
    conn = connect()

    query = """
    SELECT
        p.produto_id,
        p.nome AS produto,
        p.categoria,
        e.quantidade AS em_estoque,
        p.estoque_minimo
    FROM produtos p
    JOIN estoque e ON p.produto_id = e.produto_id;
    """

    df = pd.read_sql(query, conn)
    conn.close()
    return df


