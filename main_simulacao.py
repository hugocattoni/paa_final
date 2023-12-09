import pandas as pd
from datetime import datetime, timedelta
import random
import time
from main import obter_por_dia as obter_por_dia_guloso
from main_gulosa_rotacao import obter_por_dia as obter_por_dia_guloso_rotacao


class Produto:
    def __init__(self, altura, largura, comprimento):
        self.altura = altura
        self.largura = largura
        self.comprimento = comprimento
        self.volume = altura * largura * comprimento
        self.encaixado = False


# Função para gerar uma data aleatória entre 1/1/2023 e 31/12/2023
def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


# Data inicial e final para as datas aleatórias
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

# Lista para armazenar os produtos
produtos = []

# Gerar produtos
for _ in range(200000):
    altura = random.randint(10, 30)
    largura = random.randint(10, 30)
    comprimento = random.randint(10, 30)
    data_venda = random_date(start_date, end_date)
    produto = Produto(altura, largura, comprimento)
    produto.order_approved_at = data_venda
    produtos.append(produto)

# Criar um DataFrame com os produtos
df = pd.DataFrame(
    {
        "order_id": [i for i in range(200000)],
        "order_item_id": None,
        "product_id": None,
        "product_weight_g": None,
        "product_width_cm": [produto.largura for produto in produtos],
        "product_height_cm": [produto.altura for produto in produtos],
        "product_length_cm": [produto.comprimento for produto in produtos],
        "order_approved_at": [produto.order_approved_at for produto in produtos],
    }
)

ini_guloso = time.time()
obter_por_dia_guloso(df, "output_guloso_ficticio")
fim_guloso = time.time()

ini_guloso_rotacao = time.time()
obter_por_dia_guloso_rotacao(df, "output_guloso_rotacao_ficticio")
fim_guloso_rotacao = time.time()

print(f"Tempo de exec guloso: {fim_guloso - ini_guloso}")
print(f"Tempo de exec guloso rotação: {fim_guloso_rotacao - ini_guloso_rotacao}")
