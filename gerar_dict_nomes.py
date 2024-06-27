import json

dict_nomes = {'70998' : 'Letícia(F)',
              '67370' : 'Oziel',
              '70995' : 'Vanilzo',
              '27097' : 'Dondley(F)',
              '72673' : 'Sandra',
              '72763' : 'Vitor',
              '36405' : 'Vinícius Farisi(F)',
              '36624' : 'Vinícius Gregório(F)',
              '69861' : 'Rodrigo',
              '' : 'Ana Cristina',
              '20207' : 'Alexandre(F)',
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
              '36624' : 0.5, #'Vinícius Gregório(F)'
              '69861' : 0.5, #'Rodrigo'
              '' : 0.5, #'Ana Cristina'
              '20207' : 0.5, #'Alexandre(F)'
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

dict_repasse_p2 = {'70998' : 0.3, #'Letícia(F)'
              '67370' : 0.3, #'Oziel'
              '70995' : 0.3, #'Vanilzo'
              '27097' : 0.3, #'Dondley(F)'
              '72673' : 0.3, #'Sandra'
              '72763' : 0.3, #'Vitor'
              '36405' : 0.3, #'Vinícius Farisi(F)'
              '36624' : 0.3, #'Vinícius Gregório(F)'
              '69861' : 0.3, #'Rodrigo'
              '' : 0.3, #'Ana Cristina'
              '20207' : 0.3, #'Alexandre(F)'
              '47187' : 0.3, #'Andre'
              '72495' : 0.3, #'Flavia'
              '22579' : 0.3, #'Priscila'
              '31408' : 0.3, #'Thamires'
              '74912' : 0.3, #'Daniella'
              '45879' : 0.3, #'Marcos'
              '46342' : 0.3, #'Ana Paula'
              '71475' : 0.3, #'Guilherme'
              '72389' : 0.3, #'Milton'
              '31503' : 0.3, #'Giovanna'
              '35408' : 0.3, #'Alberto'
              '71382' : 0.3, #'Marília(F)'
              '69594' : 0.3, #'Eduardo Chagas'
              
              }

with open('dict_nomes.json', 'w') as f:
    json.dump(dict_nomes, f)

with open('dict_repasse.json', 'w') as f:
    json.dump(dict_repasse, f)

with open('dict_repasse_p2.json', 'w') as f:
    json.dump(dict_repasse_p2, f)


# Código para importar o json:

#import json

# with open('dict_nomes.json', 'r') as f:
#     dict_nomes = json.load(f)