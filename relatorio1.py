opcao = input("Digite a opção desejada. 1- Cria Aluno, 2- Alunos Disponiveis, 3- Atualizar aluno, 4- Excluir Aluno, 5- Sair: ")
alunos = []

def criar_aluno():
    nome = input("Digite o nome do aluno: ")
    idade = int(input("Digite a idade do aluno: "))
    curso = input("Digite o curso do aluno (GES, GEC, GET, GEP e etc): ")
    matricula = input("Digite a matrícula do aluno: ")
    aluno = {"nome": nome, "idade": idade, "matricula": curso+matricula}
    alunos.append(aluno)
    print("Aluno criado com sucesso!")

def listar_alunos():
    if not alunos:
        print("Nenhum aluno disponível.")
    else:
        for index, aluno in enumerate(alunos):
            print(f"{index + 1}. Nome: {aluno['nome']}, Idade: {aluno['idade']}, Matrícula: {aluno['matricula']}")

def atualizar_aluno():
    listar_alunos()
    if alunos:
        index = int(input("Digite o número do aluno que deseja atualizar: ")) - 1
        if 0 <= index < len(alunos):
            nome = input("Digite o novo nome do aluno: ")
            idade = int(input("Digite a nova idade do aluno: "))
            curso = input("Digite o novo curso do aluno (GES, GEC, GET, GEP e etc): ")
            matricula = input("Digite a nova matrícula do aluno: ")
            alunos[index] = {"nome": nome, "idade": idade, "matricula": curso+matricula}
            print("Aluno atualizado com sucesso!")
        else:
            print("Número de aluno inválido.")

def excluir_aluno():
    listar_alunos()
    if alunos:
        index = int(input("Digite o número do aluno que deseja excluir: ")) - 1
        if 0 <= index < len(alunos):
            alunos.pop(index)
            print("Aluno excluído com sucesso!")
        else:
            print("Número de aluno inválido.")

while opcao != "5":
    if opcao == "1":
        criar_aluno()
    elif opcao == "2":
        listar_alunos()
    elif opcao == "3":
        atualizar_aluno()
    elif opcao == "4":
        excluir_aluno()
    else:
        print("Opção inválida. Por favor, tente novamente.")
    
    opcao = input("Digite a opção desejada. 1- Cria Aluno, 2- Alunos Disponiveis, 3- Atualizar aluno, 4- Excluir Aluno, 5- Sair: ")