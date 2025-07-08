import string
import re
import random
import time
import e_g_r
import c_g

class Asistente:
    def __init__(self, idioma):
        if (idioma == 0):
            self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE),
                                 e_g_r.estructuras_generales_de_respuesta))
            self.values = list(
                map(lambda x: x[1], e_g_r.estructuras_generales_de_respuesta))
        elif (idioma == 1):
            self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE),
                                 e_g_r.general_structures))
            self.values = list(
                map(lambda x: x[1], e_g_r.general_structures))
        else:
            self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE),
                                 e_g_r.translate_structures))
            self.values = list(
                map(lambda x: x[1], e_g_r.translate_structures))

    '''
        traducir: toma una cadena, reemplaza cualquier palabra
        encontrada en dict.keys() con el valor correspóndiente de dict.values()
    '''

    def translate(self, str, dict):
        palabras = str.lower().split()
        keys = dict.keys()
        for i in range(0, len(palabras)):
            if palabras[i] in keys:
                palabras[i] = dict[palabras[i]]
        return ' '.join(palabras)

    '''
        respuesta: toma una cadena, un conjunto de expresiones regulares,
        y su correspondiente conjunto de listas de respuestas; encuentra un
        emparejamiento, y regresa una respuesta seleccionada de manera
        aleatoria de la lista correspondiente
    '''

    def respuesta(self, str, idioma):
        # encuentra un emparejamiento entre las llaves
        for i in range(0, len(self.keys)):
            match = self.keys[i].match(str)
            if match:

                '''
                     encontró una pareja ... lo rellena con el valor correspondiente
                     seleccionado de manera aleatoria de entre las opciones disponibles
                '''

                resp = random.choice(self.values[i])
                # obtuvo una respuesta... rellena el texto respuesta en donde se indica
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos+1:pos+2])
                    if (idioma == 0):
                        resp = resp[:pos] + \
                            self.translate(match.group(num), c_g.conversiones_generales) + \
                            resp[pos+2:]
                    elif (idioma == 1):
                        resp = resp[:pos] + \
                            self.translate(match.group(num), c_g.general_conversions) + \
                            resp[pos+2:]
                    else:
                        resp = resp[:pos] + \
                            self.translate(match.group(num), c_g.translate_converions) + \
                            resp[pos+2:]
                    pos = resp.find('%')
                # modificar la puntuación
                if resp[-2:] == '?.':
                    resp = resp[:-2] + '.'
                if resp[-2:] == '??':
                    resp = resp[:-2] + '?'
                return resp