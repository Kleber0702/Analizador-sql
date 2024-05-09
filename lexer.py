import ply.lex as lex
import difflib

class Lexer:
    tokens = [
        'DELIMITADOR',
        'OPERADOR',
        'PALABRA_RESERVADA',
        'ENTERO',
        'IDENTIFICADOR',
        'PUNTO',  # Token para el punto "."
        'PALABRA_RESERVADA_MAL_ESCRITA',
        'IDENTIFICADOR_ERRONEO',
    ]

    t_ignore = ' \t'
    contador_lineas = 1
    token_count = {}  # Diccionario para contar los tokens
    error_list = []   # Lista para almacenar mensajes de error

    reserved = {
        'varchar': 'VARCHAR',
        'int': 'INT',
        'select': 'SELECT',
        'insert': 'INSERT',
        'update': 'UPDATE',
        'delete': 'DELETE',
        'from': 'FROM',
        'where': 'WHERE',
        'order': 'ORDER',
        'by': 'BY',
        'group': 'GROUP',
        'having': 'HAVING',
        'join': 'JOIN',
        'left': 'LEFT',
        'right': 'RIGHT',
        'inner': 'INNER',
        'outer': 'OUTER',
        'on': 'ON',
        'as': 'AS',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'in': 'IN',
        'exists': 'EXISTS',
        'all': 'ALL',
        'any': 'ANY',
        'distinct': 'DISTINCT',
        'count': 'COUNT',
        'sum': 'SUM',
        'avg': 'AVG',
        'min': 'MIN',
        'max': 'MAX',
        'case': 'CASE',
        'when': 'WHEN',
        'then': 'THEN',
        'else': 'ELSE',
        'end': 'END',
        'null': 'NULL',
        'true': 'TRUE',
        'false': 'FALSE',
        'create': 'CREATE',
        'table': 'TABLE',
        'database': 'DATABASE',
        'if': 'IF',
        'into': 'INTO',
    }

    tokens += reserved.values()

    @staticmethod
    def t_DELIMITADOR(t):
        r'[{}();]'
        return t

    @staticmethod
    def t_OPERADOR(t):
        r'[-+*/=<>]'
        return t

    @staticmethod
    def t_ENTERO(t):
        r'-?\b\d+\b'
        return t

    @staticmethod
    def t_IDENTIFICADOR(t):
        r'[a-zA-Z0-9_]+'

        # Si la palabra coincide exactamente con una palabra reservada, es una palabra reservada
        if t.value.lower() in Lexer.reserved:
            t.type = Lexer.reserved[t.value.lower()]
        # Si la palabra es similar a una palabra reservada pero con una ortografía incorrecta, la tratamos como mal escrita
        elif difflib.get_close_matches(t.value.lower(), Lexer.reserved.keys(), n=1, cutoff=0.7):
            t.type = 'PALABRA_RESERVADA_MAL_ESCRITA'
            error_message = f"Error léxico: Palabra reservada mal escrita '{t.value}' en la línea {Lexer.contador_lineas}"
            Lexer.error_list.append((error_message, t.value))
        elif t.value[0].isdigit():
            t.type = 'IDENTIFICADOR_ERRONEO'
            error_message = f"Error léxico: Palabra reservada mal escrita '{t.value}' en la línea {Lexer.contador_lineas}"
            Lexer.error_list.append((error_message, t.value))
        else:
            t.type = 'IDENTIFICADOR'

        return t  # Devolvemos el token creado

    @staticmethod
    def t_PALABRA_RESERVADA(t):
        r'(select|varchar|insert|update|delete|from|where|order|by|group|having|join|left|right|inner|outer|on|as|and|or|not|in|exists|all|any|distinct|count|sum|avg|min|max|case|when|then|else|end|null|true|false|create|table|database|if|int|into)'
        t.type = Lexer.reserved.get(t.value.lower(), 'PALABRA_RESERVADA')
        return t

    @staticmethod
    def t_PUNTO(t):
        r'\.'
        return t

    @staticmethod
    def t_newline(t):
        r'\n+'
        Lexer.contador_lineas += t.value.count('\n')
        t.lexer.lineno += t.value.count('\n')

    @staticmethod
    def t_eof(t):
        t.lexer.lineno += t.value.count('\n')
        return None

    @staticmethod
    def t_error(t):
        error_message = f"Error léxico: Carácter inesperado '{t.value[0]}' en la línea {Lexer.contador_lineas}"
        Lexer.error_list.append(error_message)
        t.lexer.skip(1)

    def build():
        return lex.lex(module=Lexer())

lexer = Lexer.build()
