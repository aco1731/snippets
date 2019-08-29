import requests
import bs4 
from datetime import datetime

url = "https://localbitcoins.com"

html = requests.get(url)

soup = bs4.BeautifulSoup(html.text, 'html.parser')

tabela = soup.find("table")

tabela = [item for item in tabela.findAll('tr')]

tabela.pop(0)

print("Lista de Vendedores - Local Bitcoin -", datetime.now().strftime('%Y-%m-%d - %H:%M'),'\n')

vendedores = []

for linha in tabela:
    colunas = linha.find_all('td')
    print ("Vendedor:", colunas[0].a.get_text())
    #print ("Tempo de Resposta:", colunas[0].span['title'])  
    print ("Metodos de Pagamento:", " ".join(colunas[1].text.split()[4:]))
    print ("Preço\BTC:", colunas[2].get_text().strip())
    print ("Limites:", colunas[3].get_text().strip())
    print("Link:", url + colunas[4].a['href'])
    print("\n")
    vendedores.append({'Vendedor':colunas[0].a.get_text(), 'Preço':colunas[2].get_text().strip()})


for vendedor in vendedores:
    if float(vendedor['Preço'].split()[0].replace(",", "")) < 15130:
       print (vendedor)

# listdesc = []
           

# for th in tabela.find_all('th'):
#     #print(type(th))
#     item = th.get_text().strip()
#     #Remove itens vazios.
#     if item:
#         listDesc.append(item)
