from pandas.io.formats.format import return_docstring


def aplicar_regras(df):
    df["falta"] = df["estoque_minimo"] - df["em_estoque"]

    def status(row):
        if row["em_estoque"] == 0:
            return "sem_estoque"
        elif row["em_estoque"] < row["estoque_minimo"]:
            return "alerta"
        else:
            return "ok"

    df["status"] = df.apply(status, axis=1)
    return df