from models import Motorista, Viagem
from utils import resumo_viagens
from database import conectar
import sqlite3

def cadastrar_motorista():
    nome = input("Nome do Motorista: ")
    banco = input("Banco: ")
    agencia = input("Agência: ")
    op = input("Operação: ")
    conta = input("Conta: ")
    adiantamento = float(input("Adiantamento (padrão 2500): ") or 2500.0)
    
    motorista = Motorista(nome, banco, agencia, op, conta, adiantamento)
    motorista.salvar()
    print("Motorista cadastrado com sucesso!")

def registrar_viagem():
    motorista_id = int(input("ID do Motorista: "))
    conn = sqlite3.connect('controle.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM motoristas WHERE id = ?', (motorista_id,))
    nome_motorista = cursor.fetchone()
    
    if nome_motorista:
        nome_motorista = nome_motorista[0]
        data = input("Data da Viagem (YYYY-MM-DD): ")
        valor_apresentado = float(input("Valor Apresentado: "))
        valor_deferido = float(input("Valor Deferido: "))
        
        viagem = Viagem(motorista_id, nome_motorista, data, valor_apresentado, valor_deferido)
        viagem.salvar()
        print("Viagem registrada com sucesso!")
    else:
        print("Motorista não encontrado.")
    conn.close()

def exibir_resumo():
    try:
        motorista_id = int(input("ID do Motorista: "))
        data_inicio = input("Data de Início (YYYY-MM-DD): ")
        data_fim = input("Data de Término (YYYY-MM-DD): ")
        resumo = resumo_viagens(motorista_id, data_inicio, data_fim)
        
        if resumo['motorista']:
            print(f"Motorista: {resumo['motorista']}")
            for viagem in resumo["viagens"]:
                print(f"Data: {viagem[1]}, Valor Apresentado: {viagem[2]}, Valor Deferido: {viagem[3]}")
            print(f"Total Valor Apresentado: {resumo['total_valor_apresentado']}")
            print(f"Total Valor Deferido: {resumo['total_valor_deferido']}")
            print(f"Saldo: {resumo['total_valor_deferido'] - resumo['total_valor_apresentado']}")
        else:
            print("Nenhuma viagem encontrada para o motorista.")
    except ValueError as e:
        print(f"Erro ao exibir resumo: {e}")

def main():
    while True:
        print("\n--- Menu ---")
        print("1. Cadastrar Motorista")
        print("2. Registrar Viagem")
        print("3. Exibir Resumo de Viagens")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_motorista()
        elif opcao == '2':
            registrar_viagem()
        elif opcao == '3':
            exibir_resumo()
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    conectar()
    main()
