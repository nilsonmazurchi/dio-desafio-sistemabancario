import textwrap
import re

# Função para exibir o menu inicial
def menu_inicial():
    menu = """\n
    ================ MENU INICIAL ================
    [nu]\tNovo usuário
    [lu]\tListar usuários
    [lc]\tListar contas
    [uc]\tUsuário cadastrado
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para exibir o menu de conta
def menu_conta():
    menu = """\n
    ================ MENU CONTA ================
    [nc]\tNova conta
    [ce]\tConta existente
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para exibir o menu de operações
def menu_operacoes():
    menu = """\n
    ================ MENU OPERAÇÕES ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para depositar dinheiro em uma conta
def depositar(conta, valor):
    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return conta

# Função para sacar dinheiro de uma conta
def sacar(conta, valor, limite, limite_saques):
    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > limite
    excedeu_saques = conta["numero_saques"] >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return conta

# Função para exibir o extrato de uma conta
def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo:\t\tR$ {conta['saldo']:.2f}")
    print("==========================================")

# Função para validar o formato da data
def validar_data(data):
    return bool(re.match(r"\d{2}-\d{2}-\d{4}", data))

# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ")

    while True:
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        if validar_data(data_nascimento):
            break
        else:
            print("\n@@@ Data de nascimento inválida! Use o formato dd-mm-aaaa. @@@")

    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    usuarios.append(usuario)
    print("=== Usuário criado com sucesso! ===")

    return usuario

# Função para filtrar um usuário pelo CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta para um usuário
def criar_conta(agencia, numero_conta, usuarios, cpf, contas):
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario and not filtrar_conta(cpf, contas):
        conta = {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "numero_saques": 0}
        print("\n=== Conta criada com sucesso! ===")
        return conta

    if usuario:
        print("\n@@@ Usuário já possui uma conta, criação de nova conta não permitida! @@@")
    else:
        print("\n@@@ Usuário não encontrado! @@@")
    
    return None

# Função para filtrar uma conta pelo CPF do titular
def filtrar_conta(cpf, contas):
    contas_filtradas = [conta for conta in contas if conta['usuario']['cpf'] == cpf]
    return contas_filtradas[0] if contas_filtradas else None

# Função para listar todas as contas cadastradas
def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada! @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função para listar todos os usuários cadastrados
def listar_usuarios(usuarios):
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado! @@@")
        return

    for usuario in usuarios:
        linha = f"""\
            Nome:\t\t{usuario['nome']}
            CPF:\t\t{usuario['cpf']}
            Data Nasc.:\t{usuario['data_nascimento']}
            Endereço:\t{usuario['endereco']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função para realizar operações bancárias em uma conta
def realizar_operacoes(conta, limite, limite_saques):
    while True:
        opcao = menu_operacoes()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta = depositar(conta, valor)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta = sacar(conta, valor, limite, limite_saques)

        elif opcao == "e":
            exibir_extrato(conta)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
    return conta

# Função principal para executar o sistema bancário
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []

    while True:
        opcao = menu_inicial()

        if opcao == "nu":
            usuario = criar_usuario(usuarios)

            if usuario:
                cpf = usuario['cpf']
                while True:
                    opcao_conta = menu_conta()

                    if opcao_conta == "nc":
                        numero_conta = len(contas) + 1
                        conta = criar_conta(AGENCIA, numero_conta, usuarios, cpf, contas)

                        if conta:
                            contas.append(conta)
                            conta = realizar_operacoes(conta, limite=500, limite_saques=LIMITE_SAQUES)
                            break

                    elif opcao_conta == "ce":
                        conta = filtrar_conta(cpf, contas)

                        if conta:
                            conta = realizar_operacoes(conta, limite=500, limite_saques=LIMITE_SAQUES)
                            break
                        else:
                            print("\n@@@ Nenhuma conta encontrada para este usuário! @@@")

                    elif opcao_conta == "q":
                        break

                    else:
                        print("Operação inválida, por favor selecione novamente a operação desejada.")

        elif opcao == "lu":
            listar_usuarios(usuarios)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "uc":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)

            if usuario:
                while True:
                    opcao_conta = menu_conta()

                    if opcao_conta == "nc":
                        numero_conta = len(contas) + 1
                        conta = criar_conta(AGENCIA, numero_conta, usuarios, cpf, contas)

                        if conta:
                            contas.append(conta)
                            conta = realizar_operacoes(conta, limite=500, limite_saques=LIMITE_SAQUES)
                            break

                    elif opcao_conta == "ce":
                        conta = filtrar_conta(cpf, contas)

                        if conta:
                            conta = realizar_operacoes(conta, limite=500, limite_saques=LIMITE_SAQUES)
                            break
                        else:
                            print("\n@@@ Nenhuma conta encontrada para este usuário! @@@")

                    elif opcao_conta == "q":
                        break

                    else:
                        print("Operação inválida, por favor selecione novamente a operação desejada.")
            else:
                print("\n@@@ Usuário não encontrado! @@@")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
