# scl_parser.py (Versão Interpretador)

# Importa as classes de definição de Token e Tipo de Token do arquivo vizinho.
from token_definitions import TokenType, Token

# A classe SCLParser é o nosso interpretador. Ela não herda de nenhuma outra classe,
# sendo completamente autossuficiente.
class SCLParser:
    # O método __init__ é o construtor, responsável por inicializar o estado interno do interpretador.
    def __init__(self):
        # --- Atributos de Estado do Analisador Léxico (Lexer) ---
        self.palavra = ''          # Armazena a string completa do código-fonte.
        self.posicao = 0           # A posição (índice) atual do caractere que estamos lendo.
        self.lookAhead = ''        # O caractere exato na 'posicao' atual.
        self.lineno = 1            # O número da linha atual, para mensagens de erro.
        
        # --- Atributos de Estado do Analisador Sintático (Parser) ---
        self.current_token = None  # O objeto Token atual que foi produzido pelo lexer.

        # --- Atributos do Interpretador ---
        self.symbol_table = {}     # A Tabela de Símbolos, que armazena as variáveis (tipo e valor).
        
        # Um dicionário que mapeia as strings das palavras-chave para seus tipos de token.
        # Facilita a identificação de palavras reservadas.
        self.keywords = {
            "INT": TokenType.TYPE_INT, "REAL": TokenType.TYPE_REAL, "BOOL": TokenType.TYPE_BOOL,
            "IF": TokenType.IF, "THEN": TokenType.THEN, "ELSE": TokenType.ELSE, "END_IF": TokenType.END_IF,
            "WHILE": TokenType.WHILE, "DO": TokenType.DO, "END_WHILE": TokenType.END_WHILE,
            "FOR": TokenType.FOR, "TO": TokenType.TO, "END_FOR": TokenType.END_FOR,
            "PRINT": TokenType.PRINT,
            "OR": TokenType.OR, "AND": TokenType.AND, "NOT": TokenType.NOT,
            "TRUE": TokenType.BOOLEAN_LITERAL, "FALSE": TokenType.BOOLEAN_LITERAL
        }

    # --- Métodos de Configuração e Utilitários ---
    
    def inicializa(self, palavra_input):
        """Prepara o parser para analisar uma nova string de entrada."""
        self.palavra = palavra_input
        self.posicao = 0
        self.lineno = 1
        self.lookAhead = self.palavra[self.posicao] if self.palavra else '#'
        # Pega o primeiro token para iniciar a análise.
        self.current_token = self._get_next_token()
        
    def _parser_error(self, message):
        """Lança um erro formatado e encerra a execução."""
        print(f"\nERRO (linha {self.current_token.lineno if self.current_token else self.lineno}): {message}")
        if self.current_token: print(f"  Token atual: {self.current_token}")
        exit(1)

    # --- Métodos do Analisador Léxico (Lexer) ---

    def _lexer_advance_char(self):
        """Avança um caractere na string de entrada e atualiza o lookAhead."""
        if self.lookAhead == '\n': self.lineno += 1
        self.posicao += 1
        self.lookAhead = self.palavra[self.posicao] if self.posicao < len(self.palavra) else '#'

    def _peek(self):
        """Espia o próximo caractere sem consumi-lo, útil para operadores de 2 caracteres."""
        peek_pos = self.posicao + 1
        return self.palavra[peek_pos] if peek_pos < len(self.palavra) else '#'

    def _get_next_token(self):
        """Lê a string de entrada caractere por caractere e a transforma em uma sequência de tokens."""
        while self.lookAhead != '#':
            # Pula caracteres de espaço em branco e comentários de linha (//).
            if self.lookAhead.isspace(): self._lexer_advance_char(); continue
            if self.lookAhead == '/' and self._peek() == '/':
                while self.lookAhead != '\n' and self.lookAhead != '#': self._lexer_advance_char()
                continue

            start_pos, current_lineno = self.posicao, self.lineno

            # 1. Reconhecimento de Identificadores e Palavras-chave
            if self.lookAhead.isalpha():
                ident_str = ""
                while self.lookAhead.isalnum() or self.lookAhead == '_': ident_str += self.lookAhead; self._lexer_advance_char()
                upper_ident = ident_str.upper()
                token_type = self.keywords.get(upper_ident)
                if token_type: # Se a string é uma palavra-chave...
                    if token_type == TokenType.BOOLEAN_LITERAL: return Token(token_type, True if upper_ident == "TRUE" else False, start_pos, current_lineno)
                    return Token(token_type, upper_ident, start_pos, current_lineno)
                return Token(TokenType.ID, ident_str, start_pos, current_lineno) # Senão, é um ID.

            # 2. Reconhecimento de Literais Numéricos (INT e REAL)
            elif self.lookAhead.isdigit():
                num_str = ""
                while self.lookAhead.isdigit(): num_str += self.lookAhead; self._lexer_advance_char()
                if self.lookAhead == '.': # Verifica se é um número REAL
                    num_str += '.'; self._lexer_advance_char()
                    while self.lookAhead.isdigit(): num_str += self.lookAhead; self._lexer_advance_char()
                    return Token(TokenType.NUMBER_LITERAL, float(num_str), start_pos, current_lineno)
                return Token(TokenType.NUMBER_LITERAL, int(num_str), start_pos, current_lineno) # Senão, é INT.
            
            # 3. Reconhecimento de Operadores (2 caracteres primeiro, para evitar ambiguidades)
            elif self.lookAhead == ':' and self._peek() == '=': self._lexer_advance_char(); self._lexer_advance_char(); return Token(TokenType.ASSIGN, ':=', start_pos, current_lineno)
            elif self.lookAhead == '<' and self._peek() == '>': self._lexer_advance_char(); self._lexer_advance_char(); return Token(TokenType.NEQ, '<>', start_pos, current_lineno)
            elif self.lookAhead == '<' and self._peek() == '=': self._lexer_advance_char(); self._lexer_advance_char(); return Token(TokenType.LTE, '<=', start_pos, current_lineno)
            elif self.lookAhead == '>' and self._peek() == '=': self._lexer_advance_char(); self._lexer_advance_char(); return Token(TokenType.GTE, '>=', start_pos, current_lineno)

            # 4. Reconhecimento de Operadores e Pontuação (1 caractere)
            else:
                single_char_map = {'=': TokenType.EQ, '+': TokenType.PLUS, '-': TokenType.MINUS, '*': TokenType.MUL, '/': TokenType.DIV, '(': TokenType.LPAREN, ')': TokenType.RPAREN, ';': TokenType.SEMICOLON, '<': TokenType.LT, '>': TokenType.GT}
                char = self.lookAhead
                if char in single_char_map:
                    self._lexer_advance_char()
                    return Token(single_char_map[char], char, start_pos, current_lineno)
                else: # Se o caractere não for reconhecido, é um erro léxico.
                    self._parser_error(f"Erro Léxico: Caractere inesperado '{self.lookAhead}'")
        return Token(TokenType.EOF, '#', self.posicao, self.lineno) # Retorna o token de Fim de Arquivo.

    # --- Métodos do Analisador Sintático e Interpretador ---

    def match_token(self, expected_type):
        """Verifica se o token atual é do tipo esperado. Se for, avança para o próximo. Senão, lança um erro."""
        if self.current_token.type == expected_type: self.current_token = self._get_next_token()
        else: self._parser_error(f"Sintaxe inválida. Esperado '{expected_type}', mas foi encontrado '{self.current_token.type}'")

    # Os métodos abaixo implementam as regras da gramática da linguagem SCL.
    # Cada método é responsável por analisar e EXECUTAR uma parte do código.

    def parse(self):
        """Ponto de entrada da análise e interpretação."""
        self.program()
        self.match_token(TokenType.EOF)

    def program(self): # Regra: program -> statement_list
        self.statement_list()

    def statement_list(self): # Regra: statement_list -> (statement ";")*
        """Processa uma lista de comandos, um após o outro, até não encontrar mais comandos válidos."""
        statement_starters = [TokenType.ID, TokenType.IF, TokenType.WHILE, TokenType.FOR, TokenType.PRINT, TokenType.TYPE_INT, TokenType.TYPE_REAL, TokenType.TYPE_BOOL]
        while self.current_token.type in statement_starters:
            self.statement()
            self.match_token(TokenType.SEMICOLON) # Cada comando deve terminar com ';'

    def statement(self): # Regra: statement -> assignment | if_statement | ...
        """Verifica qual tipo de comando é o atual e chama o método apropriado para processá-lo."""
        token_type = self.current_token.type
        if token_type == TokenType.ID: self.assignment()
        elif token_type == TokenType.IF: self.if_statement()
        elif token_type == TokenType.WHILE: self.while_statement()
        elif token_type == TokenType.FOR: self.for_statement()
        elif token_type == TokenType.PRINT: self.print_statement()
        elif token_type in [TokenType.TYPE_INT, TokenType.TYPE_REAL, TokenType.TYPE_BOOL]: self.declaration()
        else: self._parser_error("Comando inválido.")

    def declaration(self): # Regra: declaration -> TYPE IDENTIFIER
        """Processa uma declaração de variável, adicionando-a à tabela de símbolos."""
        var_type = self.current_token.type
        self.match_token(var_type)
        var_name = self.current_token.value
        if var_name in self.symbol_table: self._parser_error(f"Erro Semântico: Variável '{var_name}' já declarada.")
        self.symbol_table[var_name] = {'type': var_type, 'value': None} # Adiciona à tabela com valor inicial nulo
        self.match_token(TokenType.ID)
        
    def assignment(self): # Regra: assignment -> ID := expression
        """Executa uma atribuição: avalia a expressão e atualiza o valor da variável na tabela de símbolos."""
        var_name = self.current_token.value
        if var_name not in self.symbol_table: self._parser_error(f"Erro Semântico: Variável '{var_name}' não declarada.")
        self.match_token(TokenType.ID)
        self.match_token(TokenType.ASSIGN)
        value = self.expression() # O método expression retorna o VALOR calculado
        self.symbol_table[var_name]['value'] = value
    
    def print_statement(self): # Regra: print_statement -> PRINT expression
        """Executa o comando PRINT: avalia a expressão e imprime o resultado no console."""
        self.match_token(TokenType.PRINT)
        value = self.expression()
        print(f"[SAÍDA SCL] {value}")

    # --- Métodos de Controle de Fluxo (a parte mais complexa do interpretador) ---
    # Estes métodos precisam não só analisar a sintaxe, mas também controlar o fluxo de execução,
    # decidindo quais blocos de código executar ou pular.

    def if_statement(self): # Regra: IF expression THEN statement_list (ELSE statement_list)? END_IF
        self.match_token(TokenType.IF)
        condition = self.expression() # Avalia a condição, que retorna True ou False
        self.match_token(TokenType.THEN)
        then_block_start = self.current_token, self.posicao, self.lineno, self.lookAhead
        if condition: # Se a condição for VERDADEIRA...
            self.statement_list() # ...executa o bloco THEN.
        else: # Se for FALSA...
            # ...pula o bloco THEN. Usamos um "skipper" para avançar os tokens sem executar.
            skipper = SCLParser(); skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead = then_block_start; skipper.palavra, skipper.symbol_table = self.palavra, self.symbol_table; skipper.statement_list()
            self.current_token, self.posicao, self.lineno, self.lookAhead = skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead
        
        if self.current_token.type == TokenType.ELSE:
            self.match_token(TokenType.ELSE)
            if not condition: # Se a condição original era FALSA...
                self.statement_list() # ...executa o bloco ELSE.
            else: # Se era VERDADEIRA...
                # ...pula o bloco ELSE.
                skipper = SCLParser(); skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead = self.current_token, self.posicao, self.lineno, self.lookAhead; skipper.palavra, skipper.symbol_table = self.palavra, self.symbol_table; skipper.statement_list()
                self.current_token, self.posicao, self.lineno, self.lookAhead = skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead
        self.match_token(TokenType.END_IF)

    def while_statement(self): # Regra: WHILE expression DO statement_list END_WHILE
        self.match_token(TokenType.WHILE)
        condition_start = self.current_token, self.posicao, self.lineno, self.lookAhead
        while True:
            self.current_token, self.posicao, self.lineno, self.lookAhead = condition_start # "Rebobina" para a condição
            condition_value = self.expression()
            self.match_token(TokenType.DO)
            if not condition_value: # Se a condição for FALSA...
                # ...pula o corpo do laço e sai.
                skipper = SCLParser(); skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead = self.current_token, self.posicao, self.lineno, self.lookAhead; skipper.palavra, skipper.symbol_table = self.palavra, self.symbol_table; skipper.statement_list()
                self.current_token, self.posicao, self.lineno, self.lookAhead = skipper.current_token, skipper.posicao, skipper.lineno, skipper.lookAhead
                break
            self.statement_list() # Se for VERDADEIRA, executa o corpo.
        self.match_token(TokenType.END_WHILE)

    def for_statement(self): # Regra: FOR ID := expr TO expr DO statement_list END_FOR
        self.match_token(TokenType.FOR); var_name = self.current_token.value
        if var_name not in self.symbol_table: self._parser_error(f"Erro Semântico: Variável '{var_name}' não declarada.")
        self.match_token(TokenType.ID); self.match_token(TokenType.ASSIGN)
        start_val = self.expression(); self.match_token(TokenType.TO); end_val = self.expression(); self.match_token(TokenType.DO)
        
        body_start = self.current_token, self.posicao, self.lineno, self.lookAhead
        for i in range(start_val, end_val + 1):
            self.symbol_table[var_name]['value'] = i # Atualiza a variável de controle.
            self.current_token, self.posicao, self.lineno, self.lookAhead = body_start # "Rebobina" para o início do corpo.
            self.statement_list() # Executa o corpo.
        self.match_token(TokenType.END_FOR)

    # --- Métodos de Avaliação de Expressões ---
    # A sequência de chamadas a seguir (expression -> logic_expr -> ... -> factor)
    # implementa a ordem de precedência dos operadores.

    def expression(self): return self.logic_expr() # Ponto de entrada para qualquer expressão.
    
    def logic_expr(self): # Lida com o operador OR (menor precedência).
        result = self.logic_term()
        while self.current_token.type == TokenType.OR: self.match_token(TokenType.OR); result = result or self.logic_term()
        return result

    def logic_term(self): # Lida com o operador AND.
        result = self.logic_factor()
        while self.current_token.type == TokenType.AND: self.match_token(TokenType.AND); result = result and self.logic_factor()
        return result

    def logic_factor(self): # Lida com o operador NOT.
        if self.current_token.type == TokenType.NOT: self.match_token(TokenType.NOT); return not self.logic_factor()
        return self.comparison()

    def comparison(self): # Lida com operadores de comparação (>, <, =, etc.).
        left = self.arith_expr()
        op_type = self.current_token.type
        if op_type in [TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE]:
            self.match_token(op_type); right = self.arith_expr()
            if op_type == TokenType.EQ: return left == right
            if op_type == TokenType.NEQ: return left != right
            if op_type == TokenType.LT: return left < right
            if op_type == TokenType.LTE: return left <= right
            if op_type == TokenType.GT: return left > right
            if op_type == TokenType.GTE: return left >= right
        return left

    def arith_expr(self): # Lida com Adição e Subtração.
        result = self.term()
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op_type = self.current_token.type; self.match_token(op_type)
            if op_type == TokenType.PLUS: result += self.term()
            else: result -= self.term()
        return result

    def term(self): # Lida com Multiplicação e Divisão (maior precedência aritmética).
        result = self.factor()
        while self.current_token.type in [TokenType.MUL, TokenType.DIV]:
            op_type = self.current_token.type; self.match_token(op_type)
            if op_type == TokenType.MUL: result *= self.factor()
            else: result /= self.factor()
        return result

    def factor(self): # É a base da recursão das expressões. Lida com os valores "atômicos".
        token_type = self.current_token.type
        if token_type == TokenType.NUMBER_LITERAL: value = self.current_token.value; self.match_token(TokenType.NUMBER_LITERAL); return value
        elif token_type == TokenType.BOOLEAN_LITERAL: value = self.current_token.value; self.match_token(TokenType.BOOLEAN_LITERAL); return value
        elif token_type == TokenType.ID: # Se for uma variável...
            var_name = self.current_token.value
            if var_name not in self.symbol_table: self._parser_error(f"Erro Semântico: Variável '{var_name}' não declarada.")
            value = self.symbol_table[var_name]['value'] # ...busca seu valor na tabela de símbolos.
            if value is None: self._parser_error(f"Erro de Execução: Variável '{var_name}' usada antes de ser inicializada.")
            self.match_token(TokenType.ID); return value
        elif token_type == TokenType.LPAREN: # Lida com expressões entre parênteses.
            self.match_token(TokenType.LPAREN); result = self.expression(); self.match_token(TokenType.RPAREN); return result
        else: self._parser_error("Fator inválido na expressão.")