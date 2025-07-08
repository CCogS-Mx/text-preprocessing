'''
        En esta sección, se definieron los menús de bienvenida para cada
        idoma contemplado
'''

def ingles():
    print('Assistant')
    print('='*72 + '\n')
    print('*'*29 +' Instructions ' + '*'*29)
    print('You can type in plain English, using normal upper-' +
            '\nand lower case letters and punctuation' +
            '\nType "help" to show some suggestions' +
            '\nType "quit" to finish.\n'
    )

def espanol():
    print('Asistente')
    print('='*72 + '\n' )
    print('*'*28 + ' Instrucciones  ' + '*'*28)
    print('Puedes hablar conmigo utilizando lenguaje español común, con letras' +
            '\nmayúsculas y minúsculas, y su puntuación.' +
            '\nEscribe "ayuda" para conocer qué puedo hacer' +
            '\nEscribe "salir" para terminar.\n'
    )

def traductor():
    print('Traductor / Translator')
    print('='*72 + '\n' )
    print('*'*21 + ' Instrucciones / Instructions ' + '*'*21)
    print('Excribe "Traduce" y la palabra a traducir' +
            '\nPor el momento, solo traduce palabras' +
            '\nSi es un verbo introdúcelo en infinitivo' +
            '\nEscribe "ayuda" para sugerencias' +
            '\nEscribe "salir" para terminar.\n'
    )
    print('Type "Translate" plus the word to translate' +
            '\nAt the moment it only translates single words' +
            '\nIf it is a verb, type the infintive form'
            '\nType "help" to see suggestions' +
            '\nType "quit" to finish.\n'
    )