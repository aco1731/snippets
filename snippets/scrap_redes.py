import requests
import bs4 


html = requests.get("https://localbitcoins.com/")
soup = bs4.BeautifulSoup(html.text, 'html.parser')


tabela = soup.find("table")

linhas = [ item for item in tabela.findAll('tr') ]

headers = linhas[0]
linhas = linhas[1:]

for linha in linhas:

  colunas = linha.find_all('td')
  print ("Vendedor:", colunas[0].a.get_text())
  print ("Tempo de Resposta:", colunas[0].span['title'])
  pagamento = colunas[1].text.split()
  print ("Pagamento:",pagamento[4:])
  print("/n")

#print ("Metodo de Pagamento:", pagamento)


#for linha in linhas:
#print( [ item for item in linhas[0].contents ] )

  #for  col in linha.find_all('td'):
   # print(col)

#for tr in tabela.findAll(tr):
 #   print(type(tr))
  #  for td in tr.findAll(td):
    #    print(td)

# listDesc = []

# for th in tabela.find_all('th'):
#     #print(type(th))
#     item = th.get_text().strip()
#     #Remove itens vazios.
#     if item:
#         listDesc.append(item)
