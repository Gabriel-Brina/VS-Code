nome = "joao paulo lira"
email = "emailfalsodolira@gmail.com"

# servidor
#posição
posicao = email.find("@")
servidor = email[posicao+1:]
print (servidor)

# primeiro nome
espaço = nome.find(" ")
primeiro_nome = nome[:espaço]
primeiro_nome = primeiro_nome.capitalize()
print (primeiro_nome)

# criar uma msg persolnalizada dizendo 'O usuário ... foi cadastrado com sucesso no email ...'
print (f"O usuário {primeiro_nome} foi cadastrado no servidor {servidor} .")
