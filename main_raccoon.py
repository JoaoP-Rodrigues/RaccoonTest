import json
from functions import *
import pandas as pd
import requests

# Open
file_shows = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows')
file_ingressos = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos')

#file_shows = open("psel_de_shows.json")
#file_ingressos = open("psel_de_ingressos.json")
file_compras = open("psel_de_compras.txt")
shows = json.loads(file_shows.content)
tickets = json.loads(file_ingressos.content)

df_tickets = pd.DataFrame(tickets)

# Transform the file with purchases datas.
list_purchases = file_compras.read()
all_purchases = getListPurchases(list_purchases)

# Answer the First Question:
# What the spending average of clients from Amazing Tickets
getGastosPista(tickets, all_purchases, shows)

# Answer the Second Question: 
# Which customers didn't go to the show
getNotPresents(tickets, all_purchases, shows)

# Answer the Third Question:
# Which customers bought tickets with others companies
getPurchasesCompetitors(tickets, all_purchases, shows)

# Answer the Fouth Question:
# What the show day with biggest spending
getBiggestSpending(all_purchases, shows)

#file_shows.close()
#file_ingressos.close()
file_compras.close()
