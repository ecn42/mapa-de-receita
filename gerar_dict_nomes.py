import json

dict_nomes = {'70998' : 'Letícia(F)',
              '67370' : 'Oziel',
              '70995' : 'Vanilzo',
              '27097' : 'Dondley(F)',
              '72673' : 'Sandra',
              '72763' : 'Vitor',
              '36405' : 'Vinícius Farisi(F)',
              '36624' : 'Vinícius Gregório',
              '69861' : 'Rodrigo',
              '' : 'Ana Cristina',
              '20207' : 'Alexandre',
              '47187' : 'Andre',
              '72495' : 'Flavia',
              '22579' : 'Priscila',
              '31408' : 'Thamires',
              '74912' : 'Daniella',
              '45879' : 'Marcos',
              '46342' : 'Ana Paula',
              '71475' : 'Guilherme',
              '72389' : 'Milton',
              '31503' : 'Giovanna',
              '35408' : 'Alberto',
              '71382' : 'Marília(F)',
              
              }

with open('dict_nomes.json', 'w') as f:
    json.dump(dict_nomes, f)

# Código para importar o json:

#import json

# with open('dict_nomes.json', 'r') as f:
#     dict_nomes = json.load(f)