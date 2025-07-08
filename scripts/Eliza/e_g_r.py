import time

'''
    estructuras_generales_de_respuesta, contiene la lista general de respuestas,
    cada elemento de la lista es una lista de dos listas, la primera lista es
    la expresión regular que el algoritmo utiliza para comparar las cadenas de
    entrada del usuario, contra las expresiones regulares definidas, la segunda
    es la lista de posibles respuestas
'''

estructuras_generales_de_respuesta = [
    #=================================================================
    # Saludos
    #=================================================================
    [r'Hol(a*|i*|s*)',
        [
            'Hola hola',
            'Hola, teclea algo diferente para continuar',
            'Holis',
            '¿Qué tal?',
        ]
    ],
    #=================================================================
    # Fecha y hora
    #=================================================================

    [r'Dame la hora|Dame la hora (.*)|\¿?Qu(é|e) hora es\??',
        [
            f"La hora actual es: {time.strftime('%H:%M:%S', time.localtime())}",
            f"Son las: {time.strftime('%H:%M:%S', time.localtime())}"
        ]
    ],

    [r'Dame la fecha|Dame la fecha (.*)|\¿?Qu(é|e) d(i|í)a es hoy\??',
        [
            f"Hoy es: {time.strftime('%d / %m / 20%y', time.localtime())}"
        ]
    ],

    #=================================================================
    # Bromas
    #=================================================================

    [r'Cuentame un chiste',
        [
            '¿Sabes por qué un koala no puede ser oso?\nPorqué no está koalificado.',
            '¿Qué se necesita para encender una vela?\nQue esté apagada.'
        ]
    ],

    [r'Cuentame (un|una) (.*)',
        [
            'No tengo %2' + 's disponibles por el momento'
        ]
    ],

    [r'\¿?C(ó|o)mo te llamas\??',
        [
            'No lo sé, no me han dado nombre, pero puedes llamarme asistente',
            'No tengo registrado un nombre, solo sé que me llaman asistente'
        ]
    ],

    [r'\¿?C(ó|o)mo est(á|a)s\??|\¿?C(ó|o)mo est(á|a)s (.*)\??',
        [
            'Bastante bien de hecho',
            'Muy bien, gracias por preguntar ¿Tú cómo estás?'
        ]
    ],

    #=================================================================
    # Respuestas generales
    #=================================================================

    [r'Creo que (.*)',
        [
            '¿Por qué dices que %1?',
            "¿Estas seguro de lo que dices?",
        ]
    ],

    [r'Me siento (.*)',
        [
            '¿Por qué te sientes %1?',
            '¿A qué te refieres con %1?',
            '¿Puedo ayudar con eso?'
        ]
    ],

    [r'Me (gusta|gustan) (el|la|los|las) (.*)',
        [
            'A mi también me gusta: %3',
            'Creo que tenemos cosas en común',
            'Baia baia ;)'
        ]
    ],

    [r'Necesito (.*)',
        [
            '¿Por qué necesitas %1?',
            '¿Realmente lograrás obtener %1?',
            '¿Seguro que necesitas %1?'
        ]
    ],

    [r'Si|Si (.*)|Perfecto|Perfecto (.*)|Ok|Ok (.*)|Bien (.*)',
        [
            'Perfecto',
            'Vaya, que bien',
            'Ya lo esperaba',
            'Que bien',
            'Genial'
        ]
    ],

    [r'No|No (.*)',
        [
            'Tal vez en otra ocasión',
            'Que mal',
            'No lo esperaba'
            '¿Por qué %1?'
        ]
    ],

    #=================================================================
    # Comandos
    #=================================================================

    [r'ayuda|\¿?Qu(e|é) puedes hacer\??',
        [
            'Puedes pedirme cosas cómo:' +
            '\n- "Dame la hora"' +
            '\n- "¿Qué día es hoy?"' +
            '\n- "Cuentame un chiste"' +
            '\n- "Dame la fecha"' +
            '\n- "¿Cómo te llamas?"' +
            '\n- "Necesito ..."' +
            '\n- etc.' +
            '\n\n y recuerda, no te preocupes por la puntuación y la acentuación'
        ]
    ],

    [r'salir|quit',
        [
            'Hasta luego ',
            'Bye bye',
            'Un placer',
        ]
    ],

    #=================================================================
    # Expresiones regulares no contempladas
    #=================================================================

    [r'(.*)',
        [
            'Cuentame más.',
            'Lo sienteo, mi creador no me dió la capacidad de entender eso ja ja',
            '...',
            'Deberías intentar con el comando "ayuda"',
            '%1 se encuentra fuerna de mi entendimiento',
            'Interesante',
            'Al parecer %1 no se encuentra en mis archivos jaja',
            'Intentalo de nuevo',
            'Intenta preguntando "¿Cómo estás?"',
            'Perfecto',
            'Si pudiera ser otra cosa, definitivamente no sería un asistente ja ja ja',
        ]
    ],
]

general_structures = [
    #=================================================================
    # Regards
    #=================================================================
    [r'Hi|Hello',
        [
            'Hi',
            'Hello, type something different to continue',
            'Hiii',
            'Welcome'
        ]
    ],
    #=================================================================
    # Time
    #=================================================================

    [r'Time|Time (.*)|What time is it\??',
        [
            f"The current time is: {time.strftime('%H:%M:%S', time.localtime())}",
            f"Local time: {time.strftime('%H:%M:%S', time.localtime())}",
        ]
    ],

    [r'Date|Date (.*)|What day is it\?|What day is today\?',
        [
            f"Current date: {time.strftime('%m / %d / 20%y', time.localtime())}"
        ]
    ],

    #=================================================================
    # Jokes
    #=================================================================

    [r'Tell me a joke',
        [
            "What does the zero say to the eight?\nNice belt!!",
            "What did 2 say to 4 after 2 beat him in a race?\n2 fast 4 you",
            "I put my root beer in a square glass.\nNow it's just a beer",
            "Why do mathematicians like parks?\nBecause of all the natural logs",
        ]
    ],

    [r'Tell me (a|an) (.*)',
        [
            "By the time %2" + "s are not available "
        ]
    ],

    [r'What\'?s your name\??|What is your name\??',
        [
            "I don't know my name, but you can call me assistant",
            "Not sure about that, type something else"
        ]
    ],

    [r'How are you\??',
        [
            "I'm fine thanks",
            "That's kind from you, I'm very fine",
            "Really? I'm a machine, I don't have feelings, but lets say Im fine"
        ]
    ],

    #=================================================================
    # General answers
    #=================================================================

    [r'I think (.*)',
        [
            'Why you say %1?',
            "Are you sure?",
        ]
    ],

    [r'(I feel (.*))|(I\'?m (.*))|(I am (.*))',
        [
            "Why are you %2 ?",
            "Can I help with that?",
            "Are you really %2 ?"
        ]   
    ],

    [r'I (like|love) the (.*)|I (like|love) (.*)',
        [
            'Give me 5, i like that too',
            'Nice',
            'I feel lucky today'
        ]
    ],

    [r'I need (.*)',
        [
            'Why do you need %1?',
            'Would you really get %1?',
            'Are you sure you need %1?'
        ]
    ],

    [r'Yes|Yes (.*)|Ok',
        [
            'Ok',
            "Well, that's fine",
            "I was hopping so",
            'Fine',
            'Great'
        ]
    ],

    [r'No|No (.*)',
        [
            'Maybe next time',
            'Oh no',
            "I didn't expect that",
            'Why not?'
        ]
    ],

    #=================================================================
    # Commands
    #=================================================================

    [r'help|What can you do\??',
        [
            'Try typing "What time is it?"'
        ]
    ],

    [r'quit',
        [
            'Bye bye',
            'Good bye.',
            'Have a nice day',
            'See you'
        ]
    ],

    #=================================================================
    # Undefined regular expressions
    #=================================================================

    [r'(.*)',
        [
            'Please tell me more.',
            "Sorry %1 is not amongst my files",
            'You should try typing "help"',
            'Why do you say that %1?',
            'I see.',
            'Very interesting.',
            'Try again',
            'If I could be anything else, surely I would not be an assistant',
            '...',
            'Ok'
        ]
    ],
]

translate_structures = [
    [r'Traduce (.*)',
        [
            '%1'
        ]
    ],

    [r'Translate (.*)',
        [
            '%1'
        ]
    ],

    [r'Ayuda',
        [
            'Intenta escribiendo "Traduce mirar"'
        ]
    ],

    [r'Help',
        [
            'Try typing "Translate feel"'
        ]
    ],

    [r'salir|quit',
        [
            'Bye bye',
            'Adios',
            ":'("
        ]
    ],

    [r'(.*)',
        [
            '%1 command not valid / %1 comando no válido',
            
        ]
    ]

]