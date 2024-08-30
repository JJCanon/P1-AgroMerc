import pandas as pd
import json

df = pd.read_excel('frutas.xlsx')

df.to_json('Frutas.json', orient='records')

with open('Frutas.json','r') as file:
    frutas = json.load(file)
    
for i in range (100):
    fruta = frutas[i]
    print(fruta)
    break