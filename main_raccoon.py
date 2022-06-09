import json
from functions import *
#import pandas as pd
#import requests

# Open
#file_shows = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_shows')
#file_ingressos = requests.get('https://us-central1-raccoon-bi.cloudfunctions.net/psel_de_ingressos')

file_shows = open("psel_de_shows.json")
file_ingressos = open("psel_de_ingressos.json")
file_compras = open("psel_de_compras.txt")

shows = json.load(file_shows)
tickets = json.load(file_ingressos)

# Transform the file with purchases datas.
list_purchases = file_compras.read()
compras = getListPurchases(list_purchases)

# Answer the First Question: 
# What the spending average of clients from Amazing Tickets
getGastosPista(tickets, compras, shows)

# Answer the Second Question: 
# Which customers didn't go to the show
getNotPresents(tickets, compras, shows)

# Answer the Third Question:
# Which customers bought tickets with others companies
getPurchasesCompetitors(tickets, compras, shows)

file_shows.close()
file_ingressos.close()
file_compras.close()
