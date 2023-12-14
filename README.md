# PAA - Empacotamento 3D

## Visão Geral

Código para resolução no problema do Empacotamento 3D em Python, desenvolvido para o trabalho final de Projeto e Análise de Algoritmos | PUC Minas
Prof. Daniel Capanema

## Definição

O problema do empacotamento 3D consiste em empacotar um conjunto de itens retangulares em um conjunto de caixas retangulares, de forma que nenhum item se sobreponha e que o número de caixas seja o menor possível. Este problema é NP-completo, o que significa que não existe um algoritmo que possa encontrar a solução ótima em tempo polinomial.

Nesse trabalho, foram realizadas três versões para otimização do problema:

- **Guloso sem rotação de itens:** O código tenta empacotar os itens na sua forma padrão, caso não seja possível inserir no pacote atual, gera outra;
- **Guloso com rotação de itens:** O código tenta empacotar os itens na sua forma padrão, caso não seja possível inserir nessa posição, rotaciona o item e tenta novamente. Somente após testar as 3 rotações diferentes, gera outro pacote;
- **Força Bruta:** Cria todas as combinações possíveis de produtos. Para cada combinação gerada, verifica como esses produtos podem ser armazenados nos recipientes disponíveis.

## Códigos

- O código **main_simulacao.py**, ao ser executado, realiza simulações com bases de dados gerada pelo algoritmo, implementado para testes;
- O código **main_guloso_sem_rotacao.py**, ao ser executado, realiza a otimização para a base de dados real, utilizando o método _Guloso sem rotação de itens_;
- O código **main_guloso_rotacao.py**, ao ser executado, realiza a otimização para a base de dados real, utilizando o método _Guloso com rotação de itens_;
- O código **main_forca_bruta.py**, ao ser executado, realiza a otimização para a base de dados real, utilizando o método _Força Bruta_.
