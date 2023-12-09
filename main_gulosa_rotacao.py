import pandas as pd
import math
import time

altura_caixa = 12
largura_caixa = 12
comprimento_caixa = 12


class Produto:
    def __init__(self, altura, largura, comprimento):
        self.altura = altura
        self.largura = largura
        self.comprimento = comprimento
        self.rotacoes = [
            (altura, largura, comprimento),
            (largura, comprimento, altura),
            (comprimento, altura, largura),
        ]
        self.volume = altura * largura * comprimento
        self.encaixado = False


class Caixa:
    def __init__(self, altura, largura, comprimento):
        self.altura = altura
        self.largura = largura
        self.comprimento = comprimento
        self.espaco_disponivel = [
            [[True for _ in range(comprimento)] for _ in range(largura)]
            for _ in range(altura)
        ]


def encaixar_produto(produto, caixas):
    for caixa in caixas:
        for rotacao in produto.rotacoes:
            if not produto.encaixado:
                if encaixar_caixa(produto, caixa, rotacao):
                    produto.encaixado = True
                    return


def encaixar_caixa(produto, caixa, rotacao):
    altura, largura, comprimento = rotacao
    for i in range(caixa.altura - altura + 1):
        for j in range(caixa.largura - largura + 1):
            for k in range(caixa.comprimento - comprimento + 1):
                if verificar_espaco_disponivel(
                    produto, caixa, i, j, k, altura, largura, comprimento
                ):
                    ocupar_espaco(produto, caixa, i, j, k, altura, largura, comprimento)
                    return True
    return False


def verificar_espaco_disponivel(produto, caixa, x, y, z, altura, largura, comprimento):
    for i in range(x, x + altura):
        for j in range(y, y + largura):
            for k in range(z, z + comprimento):
                if not caixa.espaco_disponivel[i][j][k]:
                    return False
    return True


def ocupar_espaco(produto, caixa, x, y, z, altura, largura, comprimento):
    for i in range(x, x + altura):
        for j in range(y, y + largura):
            for k in range(z, z + comprimento):
                caixa.espaco_disponivel[i][j][k] = False


def empacotar_produtos(produtos, altura_caixa, largura_caixa, comprimento_caixa):
    caixas = [Caixa(altura_caixa, largura_caixa, comprimento_caixa)]

    produtos.sort(key=lambda p: p.volume, reverse=True)

    for produto in produtos:
        # print(
        #     f"Altura: {produto.altura} - Largura: {produto.largura} - Comprimento: {produto.comprimento}"
        # )
        if not produto.encaixado:
            encaixar_produto(produto, caixas)
            if not produto.encaixado:
                nova_caixa = Caixa(altura_caixa, largura_caixa, comprimento_caixa)
                caixas.append(nova_caixa)
                encaixar_produto(produto, caixas)

    return caixas


def mostrar_caixas(caixas):
    for idx, caixa in enumerate(caixas):
        print(f"Caixa {idx + 1}:")
        for i in range(caixa.altura):
            for j in range(caixa.largura):
                for k in range(caixa.comprimento):
                    print("." if caixa.espaco_disponivel[i][j][k] else "X", end=" ")
                print()
            print()


def obter_por_dia(df: pd.DataFrame):
    grupos_por_dia = df.groupby(df["order_approved_at"].dt.date)

    with open("output_guloso_rotacao.txt", "w", encoding="utf-8") as arquivo:
        for dia, grupo in grupos_por_dia:
            produtos = []
            # if len(grupo) > 5 and len(grupo) <= 10:
            # if dia.strftime("%Y-%m-%d") == "2016-10-06":
            print(f"Dia: {dia}")
            arquivo.write(f"Dia: {dia}\n")
            for indice, linha in grupo.iterrows():
                produto = Produto(
                    math.ceil(linha.product_height_cm / 10),
                    math.ceil(linha.product_width_cm / 10),
                    math.ceil(linha.product_length_cm / 10),
                )
                produtos.append(produto)

                arquivo.write(
                    f"{indice} - Altura: {produto.altura} - Largura: {produto.largura} - Comprimento: {produto.comprimento}\n"
                )

            caixas_empacotadas_guloso = empacotar_produtos(
                produtos, altura_caixa, largura_caixa, comprimento_caixa
            )
            arquivo.write(
                f"Total de caixas utilizadas (abordagem gulosa rotação): {len(caixas_empacotadas_guloso)}\n\n"
            )
            # mostrar_caixas(caixas_empacotadas_guloso)


df_produtos_pedidos = pd.read_csv("tables/olist_order_items_dataset.csv")
df_pedidos = pd.read_csv("tables/olist_orders_dataset.csv")
df_produtos = pd.read_csv("tables/olist_products_dataset.csv")
df_clientes = pd.read_csv("tables/olist_customers_dataset.csv")

df_final = pd.merge(df_produtos_pedidos, df_pedidos, on="order_id", how="inner")
df_final = pd.merge(df_final, df_produtos, on="product_id", how="inner")
df_final = pd.merge(df_final, df_clientes, on="customer_id", how="inner")
df_final = df_final.dropna(
    subset=["product_length_cm", "product_height_cm", "product_width_cm"]
)
df_final["order_approved_at"] = pd.to_datetime(df_final["order_approved_at"])
df_final = df_final.sort_values(by="order_approved_at")


colunas_desejadas = [
    "order_id",
    "order_item_id",
    "product_id",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
    "order_approved_at",
]
df_final = df_final[colunas_desejadas]
# maior_altura = df_final["product_height_cm"].max()
# maior_largura = df_final["product_length_cm"].max()
# maior_comprimento = df_final["product_width_cm"].max()
# print(f"{maior_altura=} - {maior_largura=} - {maior_comprimento=}")

ini = time.time()
obter_por_dia(df_final)
fim = time.time()

print(f"Tempo de exec: {fim - ini}")
