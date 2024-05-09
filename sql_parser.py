from flask import Flask, render_template, request
from ply import yacc

app = Flask(__name__)

# Define los tokens del lexer
tokens = (
    'CREATE', 'DATABASE', 'IF', 'NOT', 'EXISTS',
    'USE', 'TABLE', 'INT', 'VARCHAR', 'DECIMAL',
    'AUTO_INCREMENT', 'PRIMARY_KEY', 'FOREIGN_KEY', 'REFERENCES', 'COMMA', 'LPAREN', 'RPAREN', 'SEMICOLON',
    'ID', 'NUMBER', 'STRING', 'SELECT', 'FROM', 'INSERT', 'UPDATE', 'DELETE', 'AND_KEYWORD', 'OR_KEYWORD',
    'INTO', 'VALUES', 'SET', 'WHERE', "ASTERISK", "PRIMARY"
)

# Define las reglas de gramática para el parser

def p_statement(p):
    '''
    statement : create_db_statement
              | use_db_statement
              | create_table_statement
              | empty
              | insert_statement
              | update_statement
              | delete_statement
              | select_statement 

    '''
    pass

def p_create_db_statement(p):
    '''
    create_db_statement : CREATE DATABASE IF NOT EXISTS ID SEMICOLON
                        | CREATE DATABASE ID SEMICOLON
    '''
    pass

def p_use_db_statement(p):
    '''
    use_db_statement : USE ID SEMICOLON
    '''
    pass

def p_create_table_statement(p):
    '''
    create_table_statement : CREATE TABLE IF NOT EXISTS ID LPAREN column_definitions RPAREN SEMICOLON
                           | CREATE TABLE ID LPAREN column_definitions RPAREN SEMICOLON
    '''
    pass

def p_column_definitions(p):
    '''
    column_definitions : column_definition
                       | column_definitions COMMA column_definition
    '''
    pass

def p_column_definition(p):
    '''
    column_definition : ID data_type column_constraints
    '''
    pass

def p_data_type(p):
    '''
    data_type : INT
              | VARCHAR LPAREN NUMBER RPAREN
              | DECIMAL LPAREN NUMBER COMMA NUMBER RPAREN
    '''
    pass

def p_column_constraints(p):
    '''
    column_constraints : AUTO_INCREMENT
                       | PRIMARY_KEY
                       | FOREIGN_KEY LPAREN ID RPAREN REFERENCES ID LPAREN ID RPAREN
    '''
    pass

def p_empty(p):
    'empty :'
    pass
def p_select_statement(p):
    '''
    select_statement : SELECT ASTERISK FROM ID SEMICOLON
    '''
    print("Parsing SELECT statement...")
    pass




# Reglas para consultas INSERT, UPDATE y DELETE
def p_insert_statement(p):
    '''
    insert_statement : INSERT INTO backtick_id LPAREN id_list RPAREN VALUES LPAREN value_list RPAREN SEMICOLON
    '''
    pass

def p_backtick_id(p):
    '''
    backtick_id : BACKTICK ID BACKTICK
    '''
    p[0] = p[2]  # Retorna el identificador sin las comillas invertidas


def p_update_statement(p):
    '''
    update_statement : UPDATE ID SET assignment_list WHERE condition SEMICOLON
    '''
    pass

def p_delete_statement(p):
    '''
    delete_statement : DELETE FROM ID WHERE condition SEMICOLON
    '''
    pass

def p_id_list(p):
    '''
    id_list : backtick_id
            | id_list COMMA backtick_id
    '''
    pass

def p_value_list(p):
    '''
    value_list : value
               | value_list COMMA value
    '''
    pass


def p_value(p):
    '''
    value : NUMBER
          | STRING
    '''
    pass

def p_assignment_list(p):
    '''
    assignment_list : assignment
                    | assignment_list COMMA assignment
    '''
    pass

def p_assignment(p):
    '''
    assignment : ID '=' value
    '''
    pass

def p_condition(p):
    '''
    condition : ID '=' value
              | condition AND_KEYWORD condition
              | condition OR_KEYWORD condition
    '''
    pass

# Define una función de manejo de errores sintácticos
def p_error(p):
    raise Exception(f"Error sintáctico en la entrada cerca de '{p.value}' en la línea {p.lineno}, columna {p.lexpos}")

# Construir el parser
parser = yacc.yacc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse_sql', methods=['POST'])
def parse_sql():
    data = request.form['sql']
    try:
        result = parser.parse(data)
        return render_template('result.html', result=result)
    except Exception as e:
        error_message = f"Error de sintaxis: {str(e)}"
        return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
