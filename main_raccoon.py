import json
from functions import * # This is a external module, where are all functions to this code.
import pandas as pd
import requests

# Open files from Links

file_compras = open("psel_de_compras.txt")
file_shows = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows')
file_ingressos = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos')

shows = json.loads(file_shows.content)
tickets = json.loads(file_ingressos.content)
df_tickets = pd.DataFrame(tickets)

# Transform the file with purchases datas.
list_purchases = file_compras.read()
all_purchases = getListPurchases(list_purchases)

# Start the iteration with the User.

print("Olá! Esse é um projeto de engenharia de dados, nível estágio.\nAqui posso responder as seguintes questões...")

# Infinite loop to answer any question how much times the user want to.
while True:

    # Create a menu for the User
    print("*" * 60)
    print("1 - Qual a média de gastos de pessoas com ingresso Pista?")
    print("2 - Quais pessoas não compareceram aos shows?")
    print("3 - Quais pessoas compraram ingressos com concorrentes?")
    print("4 - Qual o dia com maior gasto?")
    print("5 - Criar uma lista com os clientes que desistiram de comprar o ingresso com a AT,\n"
          "a soma do valor que foi gasto durante os shows e e quais shows eles desistiram decomprar.")
    print("*" * 60)
    print("Qual pergunta você deseja a resposta?")

    # Another infinite loop to get the option of user. While he/she don't choice a valid option, the code not continues.
    while True:
        opcao = input('Digite de 1 a 5: ')
        if opcao not in ['1', '2', '3', '4', '5']:
            print('Opção inválida! Digite somente números de "1" a "5"!')
        else:
            print("*" * 60)
            break

    # Start the answers from each question
    if opcao == '1':
        # Answer the First Question:
        getGastosPista(tickets, all_purchases, shows)

    elif opcao == '2':
        # Answer the Second Question:
        getNotPresents(tickets, all_purchases, shows)

    elif opcao == '3':
        # Answer the Third Question:
        getPurchasesCompetitors(tickets, all_purchases, shows)

    elif opcao == '4':
        # Answer the Forth Question:
        getBiggestSpending(all_purchases, shows)

    elif opcao == '5':
        # Answer the Fifth Question:
        # Create a file(json) with clients who have given up buying tickets with AT
        print("\nEssa opção irá gerar um arquivo Json com os dados, que será salvo no mesmo local em que o código está rodando!\n")
        input("Digite qualquer tecla para continuar...")
        file_clients = getJsonGiveUp(tickets, all_purchases, shows)
        json_not_clients = json.dumps(file_clients)
        json_file = open("psel_nao_clientes.json", "w")
        json_file.write(json_not_clients)
        json_file.close()

    # Final infinite loop, to know if the user want to continue using the code or not.
    while True:
        op = str(input('Deseja Continuar? [S/N]')).upper()
        if op not in ['S', 'N']:
            print('Opção inválida!')
        else:
            break
    if op == 'N':
        print("Obrigado! Até a próxima")
        break

file_shows.close()
file_ingressos.close()
file_compras.close()

# End of code.
