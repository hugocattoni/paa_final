guloso = list()
with open("output_guloso_final.txt", "r") as arquivo:
    for linha in arquivo:
        if "Total de caixas utilizadas" in linha:
            guloso.append(int(linha.split(":")[-1].strip()))

media_guloso = sum(guloso) / len(guloso)
print(f"Número de caixas (guloso): {sum(guloso)}")
print(f"Número de dias (guloso): {len(guloso)}")

guloso_rotacao = list()
with open("output_guloso_rotacao_final.txt", "r") as arquivo2:
    for linha in arquivo2:
        if "Total de caixas utilizadas" in linha:
            guloso_rotacao.append(int(linha.split(":")[-1].strip()))

media_guloso_rotacao = sum(guloso_rotacao) / len(guloso_rotacao)
print(f"Número de caixas (guloso rotação): {sum(guloso_rotacao)}")
print(f"Número de dias (guloso rotação): {len(guloso_rotacao)}")

print(f"Media Guloso: {media_guloso} - Media Guloso Rotação: {media_guloso_rotacao}")

quant_guloso = list()
guloso.sort()
ultimo_numero = 0
for numero in guloso:
    if numero <= ultimo_numero:
        continue
    else:
        ultimo_numero = numero
    quant_guloso.append(
        {
            "numero": numero,
            "quant": guloso.count(numero),
        }
    )

quant_guloso_rotacao = list()
guloso_rotacao.sort()
ultimo_numero = 0
for numero in guloso_rotacao:
    if numero <= ultimo_numero:
        continue
    else:
        ultimo_numero = numero

    quant_guloso_rotacao.append(
        {
            "numero": numero,
            "quant": guloso_rotacao.count(numero),
        }
    )

print(f"{quant_guloso=}")
print(f"{quant_guloso_rotacao=}")
