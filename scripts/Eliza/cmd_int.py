from eliza_clss import Asistente
import cmdint_idiomas as idiomas
import time
'''
    interface de comandos
'''
def tiempo():
    año, mes, dia, horas, minutos, segundos, dia_semana, dia_año, dia_dest = time.localtime()
    return horas, minutos, segundos

def command_interface(nombre, idioma):
    h, m, s = tiempo()
    current_time = int((h * 3600) + (m * 60) + s)
    saludos = {
        0 : ['Buenos días', 'Buenas tardes', 'Buenas noches'],
        1 : ['Good morning', 'Good afternon', 'Good evening'],
        2 : ['Buenos días / Morning', 'Buenas tardes / Afternoon', 'Buenas noches / Evening']
    }
    welcome_q = ['¿Cómo puedo ayudarte?', 'How can I help you?', 'Bienvenido / Welcome']
    asistente_name = ['Asistente', 'Assistant', 'Asist']
    
    if idioma == 0: idiomas.espanol()
    if idioma == 1: idiomas.ingles()
    if idioma == 2: idiomas.traductor()

    print('='*72)

    if (25200 <= current_time < 43200):
        print(f'{saludos[idioma][0]} {nombre} {welcome_q[idioma]}')
        
    elif (43200 <= current_time  < 68400):
         print(f'{saludos[idioma][1]} {nombre} {welcome_q[idioma]}')

    else:
        print(f'{saludos[idioma][2]} {nombre} {welcome_q[idioma]}')

    s = ''
    asistente = Asistente(idioma= idioma)
    while (s.lower() != 'quit'):
        try:
            s = input(f'{nombre} > ')
            if (s.lower() == 'salir' or s.lower() == 'bye' or s.lower() == 'close' or s.lower() == 'cerrar'):
                s = 'quit'
        except EOFError:
            s = 'quit'
        
        while s[-1] in '!.':
            s = s[:-1]
        print(f'{asistente_name[idioma]} > {asistente.respuesta(s, idioma)}')
