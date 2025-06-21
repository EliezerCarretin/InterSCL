# token_definitions.py

# A classe TokenType funciona como um "catálogo" ou "enumeração". 
# Ela centraliza todos os nomes dos tipos de tokens que nossa linguagem possui.
# Usar constantes (variáveis com nomes em maiúsculas) em vez de strings literais
# no resto do código (ex: "IF") ajuda a evitar erros de digitação.
class TokenType:
    # --- Seção de Palavras-Chave (Keywords) ---
    
    # Palavras-chave para declaração de tipos de variáveis
    TYPE_INT = "INT"
    TYPE_REAL = "REAL"
    TYPE_BOOL = "BOOL"
    
    # Palavras-chave para estruturas de controle de fluxo
    IF = "IF"
    THEN = "THEN"
    ELSE = "ELSE"
    END_IF = "END_IF"
    WHILE = "WHILE"
    DO = "DO"
    END_WHILE = "END_WHILE"
    FOR = "FOR"
    TO = "TO"
    END_FOR = "END_FOR"
    PRINT = "PRINT" # Comando para saída de dados
    
    # Palavras-chave para operadores lógicos
    OR = "OR"
    AND = "AND"
    NOT = "NOT"

    # --- Seção de Tokens Variáveis ---

    # Identificadores (nomes de variáveis)
    ID = "ID"
    
    # Literais (valores fixos no código)
    NUMBER_LITERAL = "NUMBER_LITERAL"   # ex: 123, 45.6
    BOOLEAN_LITERAL = "BOOLEAN_LITERAL" # ex: TRUE, FALSE

    # --- Seção de Operadores e Pontuação ---

    # Operadores de atribuição e aritméticos
    ASSIGN = ":="
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    
    # Operadores de Comparação
    EQ = "="    # Igual
    NEQ = "<>"  # Diferente
    LT = "<"    # Menor que
    LTE = "<="  # Menor ou igual a
    GT = ">"    # Maior que
    GTE = ">="  # Maior ou igual a

    # Símbolos de Pontuação
    SEMICOLON = ";" # Fim de um comando
    LPAREN = "("    # Abre parênteses
    RPAREN = ")"    # Fecha parênteses
    
    # Token especial para marcar o Fim do Arquivo (End Of File)
    EOF = "EOF"

# A classe Token define a estrutura de um único token.
# Cada vez que o analisador léxico reconhece uma parte do código (como um número,
# uma palavra-chave ou um operador), ele cria um objeto desta classe
# para armazenar todas as informações sobre o que foi encontrado.
class Token:
    # O método __init__ é o construtor do objeto Token.
    def __init__(self, type, value, position=0, lineno=1):
        # self.type armazena o TIPO do token. Será uma das constantes da classe TokenType.
        # Ex: TokenType.NUMBER_LITERAL
        self.type = type
        
        # self.value armazena o VALOR real que foi lido do código.
        # Ex: para um token NUMBER_LITERAL, o valor poderia ser o número 123.
        # Para um ID, poderia ser a string "minha_variavel".
        self.value = value
        
        # self.position guarda o índice do caractere onde o token começou.
        # É útil para depuração e para apontar erros com mais precisão.
        self.position = position
        
        # self.lineno guarda o número da linha onde o token foi encontrado.
        # Essencial para fornecer mensagens de erro claras ao usuário.
        self.lineno = lineno

    # O método especial __str__ define como o objeto Token será exibido
    # quando tentarmos "imprimi-lo" (com o comando print).
    # Isso é extremamente útil para depurar o analisador, pois podemos ver
    # facilmente a sequência de tokens que está sendo gerada.
    def __str__(self):
        return f"Token(type={self.type}, value='{self.value}', pos={self.position}, line={self.lineno})"