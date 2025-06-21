# Importa a classe principal do nosso interpretador, que contém toda a lógica
# de análise léxica, sintática e de execução.
from scl_parser import SCLParser 

# Importa a biblioteca JSON. Usaremos ela apenas no final, para imprimir
# a tabela de símbolos (um dicionário Python) de uma forma bonita e legível.
import json

# Este é o bloco de execução principal do Python. O código aqui dentro só roda
# quando executamos este arquivo diretamente (ex: python main.py).
if __name__ == '__main__':
    
    # Aqui definimos o código-fonte da nossa linguagem SCL em uma string de múltiplas linhas.
    # Este é o "programa" que nosso interpretador irá ler e executar.
    scl_code = """
    // --- Bloco de Declarações ---
    // O interpretador irá ler estas linhas primeiro e adicionar as variáveis
    // 'a', 'b', 'c', 'resultado_final' e 'i' à sua tabela de símbolos,
    // inicializando seus valores como nulos (None).
    REAL a;
    REAL b;
    REAL c;
    BOOL resultado_final;
    INT i;

    // --- Bloco de Atribuições Iniciais ---
    // O interpretador executa cada linha, calculando o valor à direita do ':='
    // e atualizando a tabela de símbolos com os novos valores.
    a := 10.0;
    b := 20.0;
    c := 5.0;
    resultado_final := FALSE;

    // --- Execução e Saída ---
    // O comando PRINT foi adicionado à nossa linguagem para exibir valores.
    // O interpretador deve imprimir o valor atual da variável 'a'.
    PRINT a; // Saída esperada: [SAÍDA SCL] 10.0

    // O interpretador avalia a condição do IF. A expressão aritmética e lógica
    // será calculada passo a passo:
    // 1. b * 2.0  ->  20.0 * 2.0  ->  40.0
    // 2. a + 40.0 ->  10.0 + 40.0 ->  50.0
    // 3. 50.0 > 40.0 -> TRUE
    // 4. a <> b   ->  10.0 <> 20.0 -> TRUE
    // 5. TRUE AND TRUE -> TRUE
    // Como a condição é verdadeira, o bloco THEN será executado.
    IF (a + b * 2.0 > 40.0) AND (a <> b) THEN
        resultado_final := TRUE;
    END_IF;

    // Imprime o valor de 'resultado_final' após o IF.
    PRINT resultado_final; // Saída esperada: [SAÍDA SCL] True
    
    // O interpretador inicia o laço FOR. A variável 'i' irá de 1 até 3.
    FOR i := 1 TO 3 DO
        // Dentro do laço, a cada iteração, 'c' é atualizado e seu novo valor é impresso.
        // Iteração 1: i=1, c = 5.0 + 1 -> 6.0. Imprime 6.0
        // Iteração 2: i=2, c = 6.0 + 2 -> 8.0. Imprime 8.0
        // Iteração 3: i=3, c = 8.0 + 3 -> 11.0. Imprime 11.0
        c := c + i;
        PRINT c;
    END_FOR;
    
    // Imprime o valor final de 'c' após o término do laço.
    PRINT c; // Saída esperada: [SAÍDA SCL] 11.0
    """

    # --- Início da Execução do Interpretador ---
    
    print("--- Iniciando Análise e Execução do Código SCL ---")
    
    # 1. CRIAÇÃO: Criamos uma instância (um objeto) do nosso interpretador.
    # Neste momento, ele está "vazio", pronto para receber o código.
    parser = SCLParser()
    
    # 2. INICIALIZAÇÃO: Carregamos a string scl_code para dentro do objeto parser.
    # O método `inicializa` prepara o interpretador para começar a análise,
    # lendo o primeiro caractere e o primeiro token do código.
    parser.inicializa(scl_code)
    
    # Usamos um bloco try...except para executar o interpretador. Isso permite
    # capturar qualquer erro que aconteça durante a análise e mostrar uma
    # mensagem amigável, em vez de o programa quebrar inesperadamente.
    try:
        # 3. EXECUÇÃO: Este é o comando que dispara todo o processo.
        # O método `parse` começa a percorrer o código token por token,
        # validando a sintaxe, executando os comandos e atualizando os valores
        # na tabela de símbolos.
        parser.parse()
        
        # 4. SUCESSO: Se o método `parse()` terminar sem lançar nenhum erro,
        # significa que todo o código SCL foi analisado e executado com sucesso.
        print("\nAnálise e execução concluídas com sucesso!")
        
        # Imprimimos o estado final da tabela de símbolos para verificar os valores
        # finais de todas as variáveis. O json.dumps formata o dicionário para
        # uma visualização mais clara.
        print("\n--- Tabela de Símbolos Final (com valores) ---")
        print(json.dumps(parser.symbol_table, indent=4))
        
    # Este bloco captura os erros que nós mesmos programamos no parser
    # (com a chamada `exit(1)`).
    except SystemExit as e:
        if e.code == 1:
            print("\n--- Análise falhou ---")
            
    # Este bloco captura quaisquer outros erros inesperados do Python que
    # possam ter ocorrido, ajudando na depuração.
    except Exception as e:
        print(f"\nUm erro geral inesperado ocorreu: {e}")