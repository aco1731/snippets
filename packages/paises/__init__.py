import yaml
import re

ed = ['Portugal','Espanha','França', 'Alemanha','Inglaterra']
sd = ['Argentina','Uruguai','Brasil', 'Chile','Peru']
asia = ['Japaão','China','Coreia do Sul']
 

from .phpIPAM import phpIPAM
from .sulamericanos import Sulamericanos
from .europeus import Europeus


TABELA_NORMAS = "./tabelas/tabelas_normatizacao.yml"
TABELA_REDES = "./tabelas/tabela_redes_sgtr.yml"


def pesquisa_rede(dict_host,dict_alvo=None):
    '''
    Pesquisa no dict_alvo a rede desejada conforme os criterios 
    do dic_host( cliente, ambiente, regiao e finalidade).
    '''
    
    if dict_alvo is None:
        dict_alvo = dict_redes


    if type(dict_host) is dict:
        #Presume que foi passado o dicionario dict_host da funcao traduz_hostname. 
        #Utiliza ós 4 primeiras chaves para localizar a rede(cliente,amb, regiao e finalidade).
        criterios = [dict_host[item][0:4] for item in dict_host][0:4]
    else:
        #Caso não, não faz nenhum tratamento. Aceita os criterios como estão.
        criterios = dict_host
        
    try:
        
        if type(dict_alvo) is dict:
            #Se o dicionario alvo tem as chaves rede e backup, a rede foi encontrada.
            if 'Dados' in dict_alvo and 'Backup' in dict_alvo:
                return dict_alvo
            
            #Varre o dicionario até encontrar a chave correspondente ao criterio atual.
            #Após identificar a chave, faz uma nova chamada a funcao passando o dicionario da chave e o prox. criterio
            criterio = criterios.pop(0)
            dict_next = next(value for key,value in dict_alvo.items() if criterio in key)
            return pesquisa_rede(criterios,dict_next)
        else:
            #Se dict_redes não é mais um dicionario, a rede foi localizada. Retorna o valor.
            return dict_alvo
    except IndexError:
        print('Não foi possível identificar a rede. Necessita de mais criterios?'\
              f'\ncriterio = {criterios} \ndict_alvo = {dict_alvo}')
        return None
    except StopIteration:
        print(f'Não foi possível identificar a rede. O criterio informado existe no dict de rede?'\
              f'\ncriterio = {criterios} \ndict_alvo = {dict_alvo}')
        return None


def traduz_hostname(hostname):
    '''
        Retorna um dicionario detalhando o hostname conforme as definições da tabela de normatização.
    '''

    regex = re.search("(?P<host>(?:v|f|p))(?P<uf>[1-3])(?P<finalidade>[1-5])(?P<os>[1-3])(?P<ambiente>(?:p|h|d|t|r))(?P<id>\w+)($|(\.(?P<sufixo>([a-z])+(\.[a-z]+)*))$)", hostname, re.I)
    
    if (regex):
        host = regex.group('host').lower()
        uf = regex.group('uf').lower()
        finalidade = regex.group('finalidade').lower()
        ambiente = regex.group('ambiente').lower()
        sufixo = regex.group('sufixo')
    else:
        #print("ERRO: Nome fora do padrão.")
        return None
    
    cliente = 'Legado'
    backup = False
    
    #Identifica a região baseado no dict REGIAO
    regiao = next(chave for chave,valor in REGIAO.items() if finalidade in valor)
    
    if sufixo is not None:
        lista_sufixo = sufixo.lower().split('.')
        dict_clientes = {'inss':'INSS','mte':'MTE','rfb':'RFB'}
        for sufixo in lista_sufixo:
            if sufixo in dict_clientes: cliente = dict_clientes[sufixo]
            if sufixo in 'dmz': regiao = 'RIE'
         #   if sufixo in 'bkp': backup = True
  
    #    print('Cliente: ' + cliente + '\nRegião: ' + regiao + '\nAmbiente: ' +  \
    #    AMBIENTE[ambiente] + '\nFinalidade: ' + FINALIDADE[finalidade] + \
    #   '\nBackup: ' + ['Não', 'Sim'][backup])
    
    dict_info_rede = {'cliente':cliente,'ambiente':AMBIENTE[ambiente],'regiao':regiao
                    ,'finalidade':FINALIDADE[finalidade],'backup':['Não', 'Sim'][backup],'uf':UF[uf],'host':HOST[host]}

    return dict_info_rede
  

def carrega_tabelas_yaml():
    #Carrega arquivo yaml de normatização 
    with open(TABELA_NORMAS, 'r') as normas_yml:
        try:
            dict_normas = yaml.safe_load(normas_yml)
        except yaml.YAMLError as exc:
            raise yaml.YAMLError('YAML: Não foi possível ler o arquivo com as tabelas de normatização.',exc)

    #Carrega yaml com as redes mapeadas por cliente, regiao e finalidade.
    with open(TABELA_REDES, 'r') as redes_yaml:
        try:
            dict_redes = yaml.safe_load(redes_yaml)
        except yaml.YAMLError as exc:
              raise yaml.YAMLError('YAML: Não foi possível ler o arquivo com a tabela de redes.')
        
    return [dict_normas, dict_redes]


dict_normas,dict_redes = carrega_tabelas_yaml()
(dict_normas and dict_redes) and print('Tabelas YAML carregadas com sucesso.')


#Carrega os arrays c\ as variaveis de normatização. HOST, UF, FINALIDADE, OS, AMBIENTE, REGIAO
try:
    
    #HOST = {'v': 'Virtual', 'f': 'Fisico','p':'Particao'}
    HOST = dict_normas['HOST']
    
    #UF = {'1': 'RJ','2':'DF','3':'SP'}
    UF = dict_normas['UF']
    
    #FINALIDADE = {'0':'Hospedeiro','1':'Banco de Dados','2':'Aplicação','3':'Apresentação','4':'Operacional','5':'Gerenciamento'}
    FINALIDADE = dict_normas['FINALIDADE']
    
    #OS = {'0':'Windows','1':'Linux','2':'AIX','3':'HP-UX','4':'ESX','5':'SCO','6':'Novell','7':'Solaris'}
    OS = dict_normas['OS']
    
    #AMBIENTE = {'p':'Produção','h':'Homologação','t':'Teste','d':'Desenvolvimento','r':'Treinamento'}
    AMBIENTE = dict_normas['AMBIENTE']
    
    #REGIAO = {'RI':['1'],'RII':['2','3','4','5']}
    REGIAO = dict_normas['REGIAO']

    #Buscar clientes no arq. de redes yaml??
    #  dict_clientes_redes_yaml = [key.lower() for key in dict_redes.keys()][1:] 
    CLIENTES = {'inss':'INSS','mte':'MTE','rfb':'RFB'}

except KeyError as exc:
    raise KeyError(f'TABELA_NORMAS não possui a chave {exc}. O arquivo YAML está correto?')


class Asiaticos():
     
    def __init__(self):
        ''' Construtor'''
        self.members = asia
  
  
    def print_paises(self):
        print('Mostrando alguns paises sulamericanos')
        for member in self.members:
            print('\t%s ' % member)