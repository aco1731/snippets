import requests
import bs4 

headers = {'User-Agent': 'Mozilla/5.0'}
payload = {'SelDia':'7','SelMes':'7'}
html = requests.post  \
 ('http://www-pessoas-tst/dtpnet/aniversariantes/aniversariantes.asp',  headers=headers,data=payload)


print(html.text)


soup = bs4.BeautifulSoup(html.text, 'html.parser')

tabela = soup.find("table")
tabela = [item for item in tabela.findAll('tr')]

tabela = tabela[2:]


for linha in tabela:
    colunas = linha.find_all('td')
    print ("Aniversariante:", colunas[1].get_text())
