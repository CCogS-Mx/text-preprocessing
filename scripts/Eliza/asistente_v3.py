#Se importa el archivo cmd_int.py, que contiene la interface principal.
import cmd_int

'''
    Página principal de eliza, contiene el código para correr el algoritmo,
    ya que se está ejecutando directamente en consola. Decidí hacerlo por 
    bloques para reducir la información contenida en el archivo principal.

    El código original se tomó de la siguiete fuente:
    http://www.le-grenier-informatique.fr/pages/les-documents-du-grenier/le-chatbot-eliza.html

    Se implementaron dos idiomas ("En", "Es") y un traductor entre estos idiomas

    Las modificaciones fueron realizadas por: Cesar Macias Sanchez

    Se optó por separarlo en bloques de código dada la longitud del código completo.
'''

if __name__ == "__main__":
    '''
        Se pide el nombre del usuario, para utilizarlo durante la conversación
    '''
    nombre = str(input('Introduce tu nombre / Type your name:\n>'))
    idioma = int(input('lenguage / language [0: Español, 1: English, 2: Transalte]:\n>')) 
    
    '''
        Ya que decidí manejar dos idiomas, recurrí al siguiente condicional
        para cambiar el idioma.
    '''
    if (idioma == 0 or idioma == 1 or idioma == 2):
        cmd_int.command_interface(nombre.capitalize(), idioma)
    else:
        print('Error, no se reconoce el comando, bye bye')
        print('Error, unrecognized command, bye bye')
        
        