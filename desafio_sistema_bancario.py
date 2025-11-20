menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[lc] Listar contas
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
usuarios = []
contas_correntes = []
AGENCIA = "0001"

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def cadastrar_usuario(usuarios):
    cpf = input("Informe o CPF do usuário: ")
    cpf_normalizado = cpf.replace(".", "").replace("-", "")
    
    if usuario_cadastrado(cpf_normalizado, usuarios):
        print("Já existe usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo do usuário: ")
    data_nascimento = input("Informe a data de nascimento do usuário (DD-MM-AAAA): ")
    endereco = input("Informe o endereço do usuário (logradouro, número - bairro - cidade/sigla estado): ")
    
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf_normalizado,
        "endereco": endereco
    }
    
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    
def usuario_cadastrado(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def cadastrar_conta_bancaria(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário para abertura da conta: ")
    cpf_normalizado = cpf.replace(".", "").replace("-", "")
    usuario = usuario_cadastrado(cpf_normalizado, usuarios)
    
    if usuario:
        print("Usuário encontrado, criando conta bancária...")
        conta = {
            "agencia": "0001",
            "numero_conta": len(usuarios) + 1,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "limite_saques": LIMITE_SAQUES
        }
        return conta
    else:
        print("Usuário não encontrado, cadastro de conta não realizado.")
        
def listar_contas(contas):
    print(contas)

while True:

    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))
        
        saldo, extrato = depositar(saldo, valor, extrato)

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = saque(
            saldo=saldo,
            valor=valor,
            extrato=extrato,
            limite=limite,
            numero_saques=numero_saques,
            limite_saques=LIMITE_SAQUES,
        )

    elif opcao == "e":
        exibir_extrato(saldo, extrato=extrato)
    
    elif opcao == "nu":
        cadastrar_usuario(usuarios)
        
    elif opcao == "nc":
        numero_conta = len(contas_correntes) + 1
        conta = cadastrar_conta_bancaria(AGENCIA, numero_conta, usuarios)
        
        if conta:
            contas_correntes.append(conta)
            print("Conta criada com sucesso!")
            
    elif opcao == "lc":
        listar_contas(contas_correntes)
        
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
