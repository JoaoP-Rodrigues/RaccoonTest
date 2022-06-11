import pandas as pd

def getListPurchases(list_compras):

    # This function have a only target: transform the file with purchases datas of clients (format less) in a Python List
    # I decided to put the datas of link in a file, to facilitate your manipulation, because of your lack of format

    compras = list_compras.split(",")

    i = 0
    cont = 0
    sublist_purchases = [] # main list, to store all sublist
    temp_list = [] # this is a sublist, to store datas of each client's purchases from each show

    # Loop While to navigate in file datas
    while i < len(compras):

        # First conditional to add the header in the list
        if i < 2:
            temp_list.append(compras[i])
            i +=1
            cont += 1
            continue

        # This second conditional exist only to get the first line of datas
        # this was necessary beacause in next lines, the count of elements will be different
        if cont == 2 and i == 2:
            temp_i = compras[i].replace(" ", "-", 1)
            new_i = temp_i.split("-")
            temp_list.append(new_i[0])

            # variable to store the Name of client for next iteration of loop
            # this was necessary because of the lack of format of file
            element_2 = new_i[1] 

            sublist_purchases.append(temp_list)
            temp_list = []
            cont = 0
            i +=1
            continue

        # This conditional will add the first (element_2 from above/below conditional) and the second elements of file in the sublist
        if cont == 0:
            temp_list.append(element_2)
            temp_list.append(compras[i])
            i += 1
            cont += 1
            continue

        # This conditional, similar to second, will break the second element to separate the Value of previous client and the Name of next Client.
        if cont == 1:
            temp_i = compras[i].replace(" ", "-", 1)
            new_i = temp_i.split("-")
            temp_list.append(new_i[0])

            # this internal conditional exist to, in final of file, don't try get the name's client, that not exist.
            if i < len(compras)-1:
                element_2 = new_i[1]

            sublist_purchases.append(temp_list)

            # Right after the temp_list be add in the sublist_purchases, it is reset to receive new datas
            temp_list = []
            cont = 0
            i += 1
            continue

    return sublist_purchases


def getGastosPista(ingressos, purchases, shows):

    # -----------
    # This function will answer the First Question.
    # -----------

    # For this, in your first loop it will get all Tickes with Status = Concluido and Tipo = Pista

    # pista_tickets will be a big list, with sub_lists in your content (nested lists)
    pista_tickets = []

    for ticket in ingressos:

        temp_list = [] # temp_list will store datas of clients that bought tickets from 'Pista' type

        if ticket['tipo'] == "Pista" and ticket['status'] == "Concluido":
            temp_list.append(ticket['nome'])
            temp_list.append(ticket['dia'])
            
            temp_list.append(0.0) # this is a field to increment the spending values of clients
            pista_tickets.append(temp_list)

    # In this second loop, the function will get the spending values of each client only in the day of show with "Pista" ticket
    for p in purchases:
        i = 0
        while i < len(pista_tickets):

            # Here was necessary get show datas to compare the day of show of files (in the first one are the name of show, and in the second one are the number of day)
            if p[0] == pista_tickets[i][0] and (shows.get(p[1]).get('dia') == pista_tickets[i][1]):
                pista_tickets[i][2] += float(p[2])

            i += 1

    # In the last loop, the function will sum of spending values bigger than zero (values equal zero are not presents clients in the show)
    sum_spending = 0
    count_present = 0
    for c in pista_tickets: 
        if c[2] > 0:
            sum_spending += c[2]
            count_present += 1

    # Print the datas in the console
    print("\n-- Gastos dos clientes da Amazing Tickets --")
    print("---------- Ingressos do tipo Pista ---------")
    print("-" * 44)
    print("Clientes Pista presentes: ", count_present)
    print("Total de gasto da Pista: ", sum_spending)
    print("Média de gastos dos Clientes: ", round(sum_spending / count_present, 2))
    print("-" * 44)

    # End of Function


def getNotPresents(ingressos, purchases, shows):

    # -----------
    # This is the function to answer the Second Question.
    # -----------
    # Similar way of the function above, it will get all clients with Status = Concluido

    ingressos_AT = []
    for ticket_AT in ingressos:
        temp_ticket = []
        if ticket_AT['status'] == "Concluido":
            temp_ticket.append(ticket_AT['nome'])
            temp_ticket.append(ticket_AT['dia'])
            temp_ticket.append(0.0)
            ingressos_AT.append(temp_ticket)

    # Here, it will test if the client have some spending value in the day of show bought
    # For answer this question, is necessary get only clients that bought tickets with AT, and did not go to the show
    for p in purchases:
        i = 0
        while i < len(ingressos_AT):

            # if the client have any spending, your datas are removed from list
            if p[0] == ingressos_AT[i][0] and (shows.get(p[1]).get('dia') == ingressos_AT[i][1]):
                ingressos_AT.remove(ingressos_AT[i])
            i += 1

    # Print Datas on the console
    print("\n-- Clientes que não foram aos shows --")
    print("-" * 40)
    for client in ingressos_AT:
        print(f"Nome: {client[0]} | Dia do show: {client[1]}")
        print("-" * 40)


def getPurchasesCompetitors(tickets, compras, eventos):
    # -----------
    # This is the function to answer the Third Question.
    # -----------

    # This function depends on another function (getCompetitors (Description of it in body of it))
    tickets_competitors = getCompetitors(tickets, compras, eventos)

    # Print Datas of Clients that not bought tickets with th AT and bought with competitors
    print("\n-- Clientes que compraram Ingressos com concorrentes --")
    print("-" * 50)
    for k, v in tickets_competitors.items():
        print(f"Nome: {k} | Dia(s) do show: {v}")
        print("-" * 40)


def getCompetitors(ingressos, purchases, shows):

    # -----------
    # This function will get datas of clients that try buy tickets with AT, but for some problem they didn't complete the purchase
    # -----------

    # In this first loop, it will get all clients with Status different of Concluido, and that not bought posteriorly to the same day
    nao_finalizados = {}
    for ticket_comp in ingressos:
        
        if ticket_comp['status'] != "Concluido":

            # Test if the name of client are in the dictionary, if not, create.
            if ticket_comp['nome'] not in nao_finalizados:
                nao_finalizados[ticket_comp['nome']] = []

            # Test if the day of show that client try buy it are in list of your name, if not, add.
            if ticket_comp['dia'] not in nao_finalizados[ticket_comp['nome']]:
                nao_finalizados[ticket_comp['nome']].append(ticket_comp['dia'])

        # If the client was able to buy later the ticket for the same day, this day will be removed from list
        if ticket_comp['status'] == "Concluido":
            if ticket_comp['nome'] in nao_finalizados and ticket_comp['dia'] in nao_finalizados[ticket_comp['nome']]:    
                nao_finalizados[ticket_comp['nome']].remove(ticket_comp['dia'])


    tickets_with_competitors = {}

    # Now, the function will get all clients that didn't complete the purchase with the AT, but had expenses on the show on same day
    i = 0
    for p in purchases:

        # This conditional exist to jump the first iteration of loop, because of the first element of list (is a header)
        if i == 0:
            i += 1
            continue
        
        # This internal loop will check if the client had any expenses.
        # If Yes, means he bought the ticket with another company

        for nome, dias in nao_finalizados.items():

            dia_gastos = shows.get(p[1]).get('dia')
            if p[0] == nome and dia_gastos in dias:
                if nome not in tickets_with_competitors:
                    tickets_with_competitors[nome] = []

                if dia_gastos not in tickets_with_competitors[nome]:
                    tickets_with_competitors[nome].append(dia_gastos)

    # Returns the dictionary with clients datas
    return tickets_with_competitors


def getBiggestSpending(compras, shows):

    # -----------
    # This function will answer the Forth question
    # -----------
    # This is the only function that uses Pandas Library, because it is a heavy Library, and the data is small to uses only it in the others functions
    
    # Creates a DataFrame with expenses datas of clients
    df_compras = pd.DataFrame(compras[1:], columns=compras[0])
    df_compras['gastos'] = df_compras['gastos'].astype("float")

    # This loop exist to convert the json file with datas of shows to a Python list, and sum the expenses of each show
    list_shows = []
    for show, datas in shows.items():
        show_temp = []
        show_temp.append(show)
        show_temp.append(str(datas['dia']))
        gastos_dia = df_compras.loc[df_compras['show'] == show, 'gastos'].sum()
        show_temp.append(gastos_dia)
        list_shows.append(show_temp)

    # Sort the dataframe leaving the highest values in first, and reset your index
    colunas = ['Nome_Show', 'Dia_Show', 'Total_de_Gastos']
    df_total_compras = pd.DataFrame(list_shows, columns=colunas).sort_values(by=['Total_de_Gastos'], ascending=False).reset_index(drop=True)

    # Get Only first row of DataFrame (with the highest spending day)
    dia_maior_gastos = df_total_compras.iloc[0]

    # Print Datas on the console 
    print('\n-------- Dia de Maior gastos --------')
    print('-' * 40)
    print('Dia: ', dia_maior_gastos[1])
    print('Show: ', dia_maior_gastos[0])
    print('Total Gasto: ', dia_maior_gastos[2])
    print('-' * 40)


def getJsonGiveUp(ingressos, gastos, eventos):
    # -----------
    # This function will answer the Fifth question
    # -----------

    # Uses the getCompetitors function do get all clients that didn't bought tickets with the AT
    ticket_competitors = getCompetitors(ingressos, gastos, eventos)

    spending_not_clients = {}
    i = 0
    for g in gastos:

        # This conditional exist to jump the first iteration of loop, because of the first element of list (is a header)
        if i == 0:
            i += 1
            continue
        # In this loop, the function will get all expenses of each client that didn't bought your tickets with the AT
        for nome, dia in ticket_competitors.items():

            dia_gasto = eventos.get(g[1]).get('dia')
            if g[0] == nome and dia_gasto in dia:
                if nome not in spending_not_clients:
                    spending_not_clients[nome] = [0.0, []]

                if g[1] not in spending_not_clients[nome][1]:
                    spending_not_clients[nome][1].append(g[1])

                # The value of expenses and the name of show is stored in a dictionary
                spending_not_clients[nome][0] += float(g[2])

    not_clients = []
    for x, y in spending_not_clients.items():

        # Print Datas on the console
        print(f"Nome: {x} | Total Gasto: {y[0]} | Dia(s) não comprado com AT: {y[1]}")

        # Store datas in list format, to create a Json file after.
        temp_dict_not_clients = {}
        temp_dict_not_clients['nome'] = x
        temp_dict_not_clients['gastos'] = round(y[0], 2)
        temp_dict_not_clients['shows'] = y[1]

        not_clients.append(temp_dict_not_clients)

    return not_clients
                