import pandas as pd
import math

altura_caixa = 12
largura_caixa = 12
comprimento_caixa = 12


class Produto:
    def __init__(self, altura, largura, comprimento):
        self.altura = altura
        self.largura = largura
        self.comprimento = comprimento
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


def empacotar_produtos_guloso(produtos, altura_caixa, largura_caixa, comprimento_caixa):
    caixas = [Caixa(altura_caixa, largura_caixa, comprimento_caixa)]

    # Ordenar produtos por volume
    produtos.sort(key=lambda p: p.volume, reverse=True)

    for produto in produtos:
        if (
            produto.altura > altura_caixa
            or produto.largura > largura_caixa
            or produto.comprimento > comprimento_caixa
        ):
            print(
                f"Tamanho incompatível: Altura: {produto.altura} - Largura: {produto.largura} - Comprimento: {produto.comprimento}"
            )
            continue

        # print(
        #     f"Altura: {produto.altura} - Largura: {produto.largura} - Comprimento: {produto.comprimento}"
        # )
        for caixa in caixas:
            if not produto.encaixado:
                if encaixar_produto_caixa(produto, caixa):
                    produto.encaixado = True
                    break
        if not produto.encaixado:
            nova_caixa = Caixa(altura_caixa, largura_caixa, comprimento_caixa)
            caixas.append(nova_caixa)
            encaixar_produto_caixa(produto, nova_caixa)

    return caixas


def encaixar_produto_caixa(produto, caixa):
    for i in range(caixa.altura - produto.altura + 1):
        for j in range(caixa.largura - produto.largura + 1):
            for k in range(caixa.comprimento - produto.comprimento + 1):
                if verificar_espaco_disponivel_caixa(produto, caixa, i, j, k):
                    ocupar_espaco_caixa(produto, caixa, i, j, k)
                    return True
    return False


def verificar_espaco_disponivel_caixa(produto, caixa, x, y, z):
    for i in range(x, x + produto.altura):
        for j in range(y, y + produto.largura):
            for k in range(z, z + produto.comprimento):
                if not caixa.espaco_disponivel[i][j][k]:
                    return False
    return True


def ocupar_espaco_caixa(produto, caixa, x, y, z):
    for i in range(x, x + produto.altura):
        for j in range(y, y + produto.largura):
            for k in range(z, z + produto.comprimento):
                caixa.espaco_disponivel[i][j][k] = False


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
    produtos = []

    for dia, grupo in grupos_por_dia:
        print(f"Dia: {dia}")
        print(len(grupo))

        # if len(grupo) > 45 and len(grupo) <= 50:
        # if dia.strftime("%Y-%m-%d") != "2017-01-30":

        for indice, linha in grupo.iterrows():
            produtos.append(
                Produto(
                    math.ceil(linha.product_height_cm / 10),
                    math.ceil(linha.product_width_cm / 10),
                    math.ceil(linha.product_length_cm / 10),
                )
            )

        caixas_empacotadas_guloso = empacotar_produtos_guloso(
            produtos, altura_caixa, largura_caixa, comprimento_caixa
        )
        print(
            f"Total de caixas utilizadas (abordagem gulosa): {len(caixas_empacotadas_guloso)}\n"
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
obter_por_dia(df_final)
