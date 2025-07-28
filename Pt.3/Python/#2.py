# Input

faturamento = input("Preencha com o faturamento (apenas números)")
faturamento = faturamento.replace("R$", " "). replace(",",".")
faturamento = float(faturamento)
custo = 600

lucro = faturamento - custo
print (lucro)

vendas_dia1 = input("Venda Dia 1")
vendas_dia2 = input("Venda Dia 2")

# print(vendas_dia1 + vendas_dia2)
lista_vendas = [100, 50, 1000, 800, 35]
print(lista_vendas[0]) #pegar um item da lista

# tamanho da lista
print(len(lista_vendas))

# somar todos os itens
total_de_vendas = sum(lista_vendas)
print(total_de_vendas)

# max, min, media
print(max(lista_vendas))
print(min(lista_vendas))
print(total_de_vendas / len(lista_vendas))

# encontrar um elemento (a posição do elemento)
print(1000 in lista_vendas)

lista_produtos = ["iphone", "ipad", "apple watch" , "airpods", "macbook"]
print("Airpods" in lista_produtos)

posicao = lista_produtos.index("airpods")
print(posicao)

pedaco_lista = lista_produtos[posicao:]
print (pedaco_lista)

# edita um item
lista_precos = [5000, 7000, 3000, 1000, 10000]
novo_preco = lista_precos[0] * 1.1
lista_precos[0] = novo_preco
print (lista_precos)

# remover um item
# lista_produtos.remove("macbook")
item_removido = lista_produtos.pop(-1)
print (item_removido)

# adicionar um item na lista
print (lista_produtos)
lista_produtos.append("macbook")

lista2_produtos = ["PC", "air tag", "caixa de som"]
lista_produtos.extend(lista2_produtos)
print (lista_produtos)

#insert um item em uma posição específica
lista_produtos.insert(1, "airpods")
print(lista_produtos)

# contar quantas vezes um itema aparece na lista
print(lista_produtos.count("airpods"))

# ordenar uma lista
lista_precos.sort(reverse=True)
print(lista_precos)

