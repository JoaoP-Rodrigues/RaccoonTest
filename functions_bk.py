
def getListPurchases(list_compras):

    # This function have a only target: transform the file with purchases datas of clients (format less) in a Python List
    # I decided to put the datas of link in a file, to facilitate while I work in the development

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
            temp_list = []
            cont = 0
            i += 1
            continue

    return sublist_purchases


def getGastosPista(ingressos, purchases, shows):

    pista_tickets = []
    for ticket in ingressos:
        temp_list = []
        if ticket['tipo'] == "Pista" and ticket['status'] == "Concluido":
            temp_list.append(ticket['nome'])
            temp_list.append(ticket['dia'])
            temp_list.append(0.0)
            pista_tickets.append(temp_list)

    for p in purchases:
        i = 0
        while i < len(pista_tickets):
            if p[0] == pista_tickets[i][0] and (shows.get(p[1]).get('dia') == pista_tickets[i][1]):
                pista_tickets[i][2] += float(p[2])

            i += 1

    sum_spending = 0
    count_present = 0
    for c in pista_tickets: 
        if c[2] > 0:
            sum_spending += c[2]
            count_present += 1

    print("\n-- Gastos dos clientes da Amazing Tickets --")
    print("---------- Ingressos do tipo Pista ---------")
    print("-" * 44)
    print("Clientes Pista presentes: ", count_present)
    print("Total de gasto da Pista: ", sum_spending)
    print("Média de gastos dos Clientes: ", round(sum_spending / count_present, 2))
    print("-" * 44)


def getNotPresents(ingressos, purchases, shows):

    ingressos_AT = []
    for ticket_AT in ingressos:
        temp_ticket = []
        if ticket_AT['status'] == "Concluido":
            temp_ticket.append(ticket_AT['nome'])
            temp_ticket.append(ticket_AT['dia'])
            temp_ticket.append(0.0)
            ingressos_AT.append(temp_ticket)


    for p in purchases:
        i = 0
        while i < len(ingressos_AT):
            if p[0] == ingressos_AT[i][0] and (shows.get(p[1]).get('dia') == ingressos_AT[i][1]):
                ingressos_AT[i][2] += float(p[2])

            i += 1

    print("\n-- Clientes que não foram aos shows --")
    print("-" * 40)
    for client in ingressos_AT:
        if client[2] == 0.0:
            print(f"Nome: {client[0]} | Dia do show: {client[1]}")
            print("-" * 40)

def getPurchasesCompetitors(ingressos, purchases, shows):

    não_finalizados = {}
    for ticket_comp in ingressos:
        
        if ticket_comp['status'] != "Concluido":

            if ticket_comp['nome'] not in não_finalizados:
                não_finalizados[ticket_comp['nome']] = []

            if ticket_comp['dia'] not in não_finalizados[ticket_comp['nome']]:
                não_finalizados[ticket_comp['nome']].append(ticket_comp['dia'])

        if ticket_comp['status'] == "Concluido":
            if ticket_comp['nome'] in não_finalizados and ticket_comp['dia'] in não_finalizados[ticket_comp['nome']]:    
                não_finalizados[ticket_comp['nome']].remove(ticket_comp['dia'])


    tickets_with_competitors = {}
    i = 0
    for p in purchases:

        teste = shows.get(p[1])
        print(type(teste))
        if i == 1:
            break

        i += 1
        print(type(teste))
        '''for nome, dias in não_finalizados.items():

            dia_gastos = shows.get(p[1]) #.get('dia')

            if p[0] == nome and dia_gastos in dias:
                if nome not in tickets_with_competitors:
                    tickets_with_competitors[nome] = []

                if dia_gastos not in tickets_with_competitors[nome]:
                    tickets_with_competitors[nome].append(dia_gastos)
        
           
    
    print("\n-- Clientes que compraram Ingressos com concorrentes --")
    print("-" * 50)
    for k, v in tickets_with_competitors.items():
        print(f"Nome: {k} | Dia do show: {v}")
        print("-" * 40)
'''
'''
            temp_ticket = []
            i = 0
            while i < len(não_comprados):
                if nc['nome'] == não_comprados[i][0] and nc['dia'] == não_comprados[i][1]:
                    
                    temp_nc.append(não_comprados[i][0])
                    temp_nc.append(não_comprados[i][1])
                    not_bought.append(temp_nc)
                i += 1

    tickets_with_competitors = {}
    for p in purchases:
        i = 0
        while i < len(not_bought):
            if p[0] == not_bought[i][0] and (shows.get(p[1]).get('dia') == not_bought[i][1]):
                if not_bought[i][0] not in tickets_with_competitors:
                    tickets_with_competitors[not_bought[i][0]] = []

                if not_bought[i][1] not in tickets_with_competitors[not_bought[i][0]]:
                    tickets_with_competitors[not_bought[i][0]].append(not_bought[i][1])

            i += 1




    
    '''