from paises import Sulamericanos
from paises import Europeus
from paises import Asiaticos
from paises import pesquisa_rede
from paises import traduz_hostname
from paises import phpIPAM


 
def main(args):

    print(args)
    sul = Sulamericanos()
    sul.print_paises()
 
    eu = Europeus()
    eu.print_paises()

    asia_ = Asiaticos()
    asia_.print_paises()

    dict_redes = 'nada'

    print(pesquisa_rede(\
        traduz_hostname('v121p300'))\
        ['Dados'])
 
    print(dict_redes)

    return
 
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))