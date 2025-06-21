# fho_parser_base.py

# Importa da biblioteca 'abc' (Abstract Base Classes) as ferramentas necessárias
# para criar uma classe abstrata. Uma classe abstrata é como um contrato ou
# um modelo que não pode ser usado diretamente, mas obriga outras classes
# que a "herdam" a implementar certos métodos.
from abc import ABC, abstractmethod

# Define a classe FHOParser. Ao herdar de 'ABC', ela se torna uma classe base abstrata.
class FHOParser(ABC):
    
    # O método __init__ é o construtor da classe. Ele é chamado sempre que
    # um novo objeto parser é criado e serve para inicializar seus atributos (variáveis internas).
    def __init__(self):
        # 'palavra' irá armazenar a string de código-fonte que será analisada. Começa vazia.
        self.palavra = ''
        
        # 'posicao' é um contador que marca em qual índice da string 'palavra' nós estamos. Começa em 0.
        self.posicao = 0
        
        # 'lookAhead' armazena o caractere atual que o parser está "olhando".
        # É a principal variável usada para tomar decisões de análise. Começa vazio.
        self.lookAhead = ''
        
    def inicializa(self, palavra_input):
        """
        Este método serve para carregar uma nova string de código no parser e
        reiniciar seu estado para o começo.
        """
        # A string de entrada é salva no atributo 'palavra' do objeto.
        self.palavra = palavra_input
        
        # A posição é resetada para 0, o início da string.
        self.posicao = 0
        
        # Verifica se a palavra não está vazia para evitar erros.
        if self.posicao < len(self.palavra):
            # O lookAhead é inicializado com o primeiro caractere da palavra.
            self.lookAhead = self.palavra[self.posicao]
        else:
            # Se a palavra for vazia, o lookAhead recebe um caractere especial '#'
            # que usaremos para marcar o fim da entrada (End of File).
            self.lookAhead = '#'
            
    def match(self, esperado):
        """
        Este método verifica se o caractere atual é o que esperamos. Se for,
        ele "consome" o caractere e avança para o próximo. Se não for, ele
        lança um erro de sintaxe.
        
        IMPORTANTE: Este match() funciona a nível de CARACTERE. No nosso interpretador SCL,
        criamos um 'match_token()' que funciona a um nível mais alto (de tokens).
        """
        # Compara o caractere atual ('lookAhead') com o caractere 'esperado'.
        if self.lookAhead == esperado:
            # Se forem iguais, avança a posição na palavra.
            self.posicao += 1
            
            # Atualiza o 'lookAhead' para o novo caractere da posição atual.
            if self.posicao < len(self.palavra):
                self.lookAhead = self.palavra[self.posicao]
            else:
                # Se chegamos ao fim da palavra, marca com '#'.
                self.lookAhead = '#'
        else:
            # Se não forem iguais, a sintaxe está incorreta.
            # Imprime uma mensagem de erro detalhada e encerra o programa.
            print(f"ERRO SINTATICO (FHOParser char-level): esperado: '{esperado}', lido: '{self.lookAhead}' na posicao {self.posicao}")
            exit(1) 
    
    # O decorador '@abstractmethod' define um método que NÃO tem implementação
    # nesta classe, mas que OBRIGATORIAMENTE deve ser implementado por qualquer
    # classe que herde de FHOParser (como a nossa SCLParser).
    @abstractmethod
    def parse(self):
        """
        Este é o método principal que iniciará o processo de análise (parsing).
        Cada parser específico (como o SCLParser) terá sua própria lógica de como
        começar a analisar a gramática.
        """
        # A palavra 'pass' significa que este método não faz nada aqui,
        # apenas cumpre a exigência de existir.
        pass