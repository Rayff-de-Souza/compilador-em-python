import sys
from MemoriaCache import MemoriaCache


CPU_DEBUG = True

registradores = {
    "1": {"valor": 0x00, "nome": "CP"},
    "2": {"valor": 0x00, "nome": "AX"},
    "3": {"valor": 0x00, "nome": "BX"},
    "4": {"valor": 0x00, "nome": "CX"},
    "5": {"valor": 0x00, "nome": "DX"},
    "flag_zero": {"valor": 0x00, "nome": "FLAG ZERO"}
}

#memoria = MemoriaCache('C:\\Users\\rayff\\Documents\\PUCPR\\PERFORMANCE_EM_SISTEMAS_CIBERFISICOS\\AULA_02\\ATIVIDADE_01\\ProjetoArq_1\\arquivos_memoria\\mov_mov_add.bin')
#memoria = MemoriaCache('C:\\Users\\rayff\\Documents\\PUCPR\\PERFORMANCE_EM_SISTEMAS_CIBERFISICOS\\AULA_02\\ATIVIDADE_01\\ProjetoArq_1\\arquivos_memoria\\inc_dec.bin')
#memoria = MemoriaCache('C:\\Users\\rayff\\Documents\\PUCPR\\PERFORMANCE_EM_SISTEMAS_CIBERFISICOS\\AULA_02\\ATIVIDADE_01\\ProjetoArq_1\\arquivos_memoria\\todas_instrucoes.bin')
#memoria = MemoriaCache('C:\\Users\\rayff\\Documents\\PUCPR\\PERFORMANCE_EM_SISTEMAS_CIBERFISICOS\\AULA_02\\ATIVIDADE_01\\ProjetoArq_1\\arquivos_memoria\\programa_simples.bin')
memoria = MemoriaCache('C:\\Users\\rayff\\Documents\\PUCPR\\PERFORMANCE_EM_SISTEMAS_CIBERFISICOS\\AULA_02\\ATIVIDADE_01\\ProjetoArq_1\\arquivos_memoria\\fibonacci_10.bin')


def buscarEDecodificarInstrucao() -> None:

    """
    Lê o byte na memória marcado pelo registrador_cp e retorna o ID da próxima instrução.

    Argumentos:
        None
    
    Retorno:
        O ID da próxima instrução.
    """

    # VARIÁVEIS GLOBAIS
    global registradores
    global memoria


    instrucao = memoria.getValorMemoria(registradores["1"]["valor"])
    
    if instrucao == 0x40:
        print("buscarEDecodificarInstrucao: instrução MOV REG, BYTE")
        return 6
    
    if instrucao == 0x41:
        print("buscarEDecodificarInstrucao: instrução MOV REG, REG")
        return 7
    
    elif instrucao == 0x01:
        print("buscarEDecodificarInstrucao: instrução ADD REG, REG")
        return 1

    elif instrucao == 0x10:
        print("buscarEDecodificarInstrucao: instrução INC REG")
        return 2
    
    elif instrucao == 0x20:
        print("buscarEDecodificarInstrucao: instrução DEC REG")
        return 3
    
    elif instrucao == 0x00:
        print("buscarEDecodificarInstrucao: instrução ADD REG, BYTE")
        return 0
    
    elif instrucao == 0x30:
        print("buscarEDecodificarInstrucao: instrução SUB REG, BYTE")
        return 4
    
    elif instrucao == 0x31:
        print("buscarEDecodificarInstrucao: instrução SUB REG, REG")
        return 5

    elif instrucao == 0x50:
        print("buscarEDecodificarInstrucao: instrução JMP BYTE")
        return 8
    
    elif instrucao == 0x60:
        print("buscarEDecodificarInstrucao: instrução CMP REG BYTE")
        return 9
    
    elif instrucao == 0x70:
        print("buscarEDecodificarInstrucao: instrução JZ BYTE")
        return 11


    return -1


def lerOperadoresExecutarInstrucao(idInstrucao: int, registrador_cp: int) -> None:

    """
    Lê os operadores e chama a função correspondente para executá-lo.

    Argumentos:
        - idInstrucao: OPCODE da instrução a ser executada;
        - registrador_cp: ponteiro para a próxima instrução.

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores
    global memoria


    try:
        operante_01 = memoria.getValorMemoria(registradores["1"]["valor"] + 1)
        operante_02 = memoria.getValorMemoria(registradores["1"]["valor"] + 2)
    except:
        operante_01 = memoria.getValorMemoria(registradores["1"]["valor"] + 1)


    if idInstrucao == 6:
        movRegByte(operante_01, operante_02)

    elif idInstrucao == 7:
        movRegReg(operante_01, operante_02)

    elif idInstrucao == 8:
        jmpByte(operante_01)

    elif idInstrucao == 9:
        cmpRegByte(operante_01, operante_02)

    elif idInstrucao == 11:
        jzByte(operante_01)

    elif idInstrucao == 1:
        addRegReg(operante_01, operante_02)

    elif idInstrucao == 2:
        incReg(operante_01)

    elif idInstrucao == 3:
        decReg(operante_01)

    elif idInstrucao == 0:
        addRegByte(operante_01, operante_02)

    elif idInstrucao == 4:
        subRegByte(operante_01, operante_02)
    
    elif idInstrucao == 5:
        subRegReg(operante_01, operante_02)
    
        
def calcularProximaInstrucao(idInstrucao: int) -> None:
    
    """
    Calcula o byte da próxima instrução incrementando ou decrementando o valor de registrador_cp.

    Argumentos:
        - idInstrução: OPCODE da instrução a ser executada;

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    if idInstrucao in [6, 1, 0, 4, 5, 7, 9]:
        registradores["1"]["valor"] += 0x03
        print("calcularProximaInstrucao: mudando CP para {}".format(registradores["1"]["valor"]))

    elif idInstrucao in [2, 3]:
        registradores["1"]["valor"] += 0x02
        print("calcularProximaInstrucao: mudando CP para {}".format(registradores["1"]["valor"]))

    # JUMP
    elif idInstrucao == 8:
        print("calcularProximaInstrucao: mudando CP para {}".format(registradores["1"]["valor"]))

    elif idInstrucao == 11 and registradores["flag_zero"]["valor"] == 0:
        registradores["1"]["valor"] += 0x02
        print("calcularProximaInstrucao: mudando CP para {}".format(registradores["1"]["valor"]))


def dumpRegistradores():

    # VARIÁVEIS GLOBAIS
    global registradores
    
    
    if CPU_DEBUG:

        print("=======================================================")
        print("{}[{}]".format(registradores["1"]["nome"], registradores["1"]["valor"]), end="  ")
        print("{}[{}]".format(registradores["2"]["nome"], registradores["2"]["valor"]), end="  ")
        print("{}[{}]".format(registradores["3"]["nome"], registradores["3"]["valor"]), end="  ")
        print("{}[{}]".format(registradores["4"]["nome"], registradores["4"]["valor"]), end="  ")
        print("{}[{}]".format(registradores["5"]["nome"], registradores["5"]["valor"]), end="  ")
        print("{}[{}]".format(registradores["flag_zero"]["nome"], registradores["flag_zero"]["valor"]), end="\n")
        print("=======================================================")


def cmpRegByte(idRegistrador: int, valor: int) -> None:

    """
    Compara valor do registrador IDReg1 com Byte. Flag Zero ZF é definida como 1 caso os valores sejam iguais
    
    Argumentos:
        - idRegistrador: id do registrador a ter seu valor comparado;
        - byte: valor a ter seu valor comparado com o registrador.

    Retorno:
        booleano (True or False)
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("lerOperadoresExecutarInstrucao: comparando o {} com {}".format(registradores[str(idRegistrador)]["nome"], valor))
    if registradores[str(idRegistrador)]["valor"] == valor:
        registradores["flag_zero"]["valor"] = 1
    
    else:
        registradores["flag_zero"]["valor"] = 0


def jzByte(byte: int) -> None:

    """
    Salta execução da CPU para o endereço Byte.
     
    Argumentos:
        - byte: o novo valor de memória do registrador_cp.

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores
    

    if registradores["flag_zero"]["valor"] == 1:
        registradores["1"]["valor"] = byte
        print(f"lerOperadoresExecutarInstrucao: JZ para o Byte {byte}")

    else:
        print(f"lerOperadoresExecutarInstrucao: JZ não executado")


def jmpByte(byte: int) -> None:

    """
    Salta execução da CPU para o endereço Byte.

    Argumentos:
        - byte: o novo valor de memória do registrador_cp.

    Retorno: 
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores
    

    print(f"lerOperadoresExecutarInstrucao: JUMP para o Byte {byte}")
    registradores["1"]["valor"] = byte


def movRegByte(idRegistrador, valor):

    # VARIÁVEIS GLOBAIS
    global registradores

    
    print("lerOperadoresExecutarInstrucao: atribuindo {} em {}".format(valor, registradores[str(idRegistrador)]["nome"]))
    registradores[str(idRegistrador)]["valor"] = valor


def movRegReg(idRegistrador_01: int, idRegistrador_02: int) -> None:

    """
    Essa função move o valor do idRegistrador_02 para o registrador idRegistrador_01.

    Argumentos:
        - idRegistrador_01: id do registrador a receber o valor movido;
        - idRegistrador_02: id do registrador a ter o valor movido.
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("lerOperadoresExecutarInstrucao: movendo o valor de {} em {}".format(registradores[str(idRegistrador_02)]["nome"], registradores[str(idRegistrador_01)]["nome"]))
    registradores[str(idRegistrador_01)]["valor"] = registradores[str(idRegistrador_02)]["valor"]


def addRegReg(idRegistrador_01: int, idRegistrador_02: int) -> None:

    """
    Adiciona o valor de um registrador para outro.

    Argumentos:
        - idRegistrador_01: OPCODE do primeiro registrador;
        - idRegistrador_02: OPCODE do segundo registrador;

    Retorno:
        None

    """

    # VARIÁVEIS GLOBAIS
    global registradores


    registradores[str(idRegistrador_01)]["valor"] += registradores[str(idRegistrador_02)]["valor"]
    print("lerOperadoresExecutarInstrucao: adicionando o valor de {} em {}".format(registradores[str(idRegistrador_02)]["nome"], registradores[str(idRegistrador_01)]["nome"]))


def addRegByte(idRegistrador: int, byte: int) -> None:

    """
    Essa função adicionará o byte ao registrador específicado.

    Argumentos:
        - byte: valor decimal a ser incrementado no registrador;
        - idRegistrador: registrador que se deseja incrementar.
    
    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    registradores[str(idRegistrador)]["valor"] += byte
    print("lerOperadoresExecutarInstrucao: adicionando {} em {}".format(registradores[str(idRegistrador)]["valor"], registradores[str(idRegistrador)]["nome"]))


def incReg(operante_01: int) -> None:

    """
    Incrementa o valor de um registrador.

    Argumentos:
        operante_01: o OPCODE do registrador a ser incrementado.

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("buscarEDecodificarInstrucao: instrução INC REG")
    print("lerOperadoresExecutarInstrucao: incrementando 1 em {}".format(registradores[str(operante_01)]["nome"]))
    registradores[str(operante_01)]["valor"] += 0x01    


def decReg(operante_01: int) -> None:

    """
    Decrementa o valor de um registrador.

    Argumentos:
        operante_01: o OPCODE do registrador a ser decrementado.

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("lerOperadoresExecutarInstrucao: decrementando 1 em {}".format(registradores[str(operante_01)]["nome"]))
    registradores[str(operante_01)]["valor"] -= 0x01    


def subRegByte(idRegistrador: int, byte: int) -> None:

    """
    Essa função irá subtrair o valor do registrador pelo byte.

    Argumentos:
        - idRegistrador: id do registrador a ser subtraído;
        - byte: valor a ser subtraído do registrador.
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("lerOperadoresExecutarInstrucao: subtraindo {} em {}".format(byte, registradores[str(idRegistrador)]["nome"]))
    registradores[str(idRegistrador)]["valor"] -= byte


def subRegReg(idRegistrador_01: int, idRegistrador_02: int) -> None:

    """
    Essa função irá subtrair o valor do idRegistrador_01 pelo idRegistrador_02.

    Argumentos:
        - idRegistrador_01: id do registrador a ser subtraído;
        - idRegistrador_02: id do registrador com o valor a subtrair.

    Retorno:
        None
    """

    # VARIÁVEIS GLOBAIS
    global registradores


    print("lerOperadoresExecutarInstrucao: subtraindo o valor de {} em {}".format(registradores[str(idRegistrador_02)]["nome"], registradores[str(idRegistrador_01)]["nome"]))
    registradores[str(idRegistrador_01)]["valor"] -= registradores[str(idRegistrador_02)]["valor"]



if __name__ == '__main__':

    while (registradores["1"]["valor"] < memoria.getTamanhoMemoria()):

        # UNIDADE DE CONTROLE
        idInstrucao = buscarEDecodificarInstrucao()

        # ULA
        lerOperadoresExecutarInstrucao(idInstrucao, registradores["1"]["valor"])

        dumpRegistradores() 

        # UNIDADE DE CONTROLE
        calcularProximaInstrucao(idInstrucao)

        input("PRESS ENTER TO CONTINUE")