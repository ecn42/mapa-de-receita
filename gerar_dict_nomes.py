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
              '69594' : 'Eduardo Chagas'
              
              }


dict_repasse = {'70998' : 0.5, #'Letícia(F)'
              '67370' : 0.5, #'Oziel'
              '70995' : 0.5, #'Vanilzo'
              '27097' : 0.5, #'Dondley(F)'
              '72673' : 0.5, #'Sandra'
              '72763' : 0.5, #'Vitor'
              '36405' : 0.5, #'Vinícius Farisi(F)'
              '36624' : 0.5, #'Vinícius Gregório'
              '69861' : 0.5, #'Rodrigo'
              '' : 0.5, #'Ana Cristina'
              '20207' : 0.5, #'Alexandre'
              '47187' : 0.5, #'Andre'
              '72495' : 0.5, #'Flavia'
              '22579' : 0.5, #'Priscila'
              '31408' : 0.5, #'Thamires'
              '74912' : 0.5, #'Daniella'
              '45879' : 0.5, #'Marcos'
              '46342' : 0.5, #'Ana Paula'
              '71475' : 0.5, #'Guilherme'
              '72389' : 0.5, #'Milton'
              '31503' : 0.5, #'Giovanna'
              '35408' : 0.5, #'Alberto'
              '71382' : 0.5, #'Marília(F)'
              '69594' : 0.5, #'Eduardo Chagas'
              
              }

with open('dict_nomes.json', 'w') as f:
    json.dump(dict_nomes, f)

with open('dict_repasse.json', 'w') as f:
    json.dump(dict_repasse, f)

# Código para importar o json:

#import json

# with open('dict_nomes.json', 'r') as f:
#     dict_nomes = json.load(f)