from database import conectar

class Motorista:
    def __init__(self, nome, banco, agencia, op, conta, adiantamento=2500.0):
        self.nome = nome
        self.banco = banco
        self.agencia = agencia
        self.op = op
        self.conta = conta
        self.adiantamento = adiantamento
    
    def validar(self):
        if not self.nome:
            raise ValueError("O nome do motorista é obrigatório.")
        if not self.banco:
            raise ValueError("O banco é obrigatório.")
        if not self.agencia or not self.agencia.isdigit():
            raise ValueError("A agência é obrigatória e deve conter apenas números.")
        if not self.op or not self.op.isdigit():
            raise ValueError("A operação é obrigatória e deve conter apenas números.")
        if not self.conta:
            raise ValueError("A conta é obrigatória.")
        if not isinstance(self.adiantamento, (int, float)) or self.adiantamento < 0:
            raise ValueError("O adiantamento deve ser um número positivo")

    def salvar(self):
        self.validar()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO motoristas (nome, banco, agencia, op, conta, adiantamento) 
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.nome, self.banco, self.agencia, self.op, self.conta, self.adiantamento))
        conn.commit()
        conn.close()

class Viagem:
    def __init__(self, motorista_id, nome_motorista, data, valor_apresentado, valor_deferido):
        if not isinstance(valor_apresentado, (int, float)) or not isinstance(valor_deferido, (int, float)) or valor_apresentado < 0 or valor_deferido < 0:
            raise ValueError("Valores apresentados e deferidos devem ser números.")
        self.motorista_id = motorista_id
        self.nome = nome_motorista
        self.data = data
        self.valor_apresentado = valor_apresentado
        self.valor_deferido = valor_deferido

    def salvar(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO viagens (motorista_id, nome, data, valor_apresentado, valor_deferido) 
        VALUES (?, ?, ?, ?, ?)
        ''', (self.motorista_id, self.nome, self.data, self.valor_apresentado, self.valor_deferido))
        conn.commit()
        self.atualizar_motorista(conn)
        conn.close()

    def atualizar_motorista(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        SELECT SUM(valor_apresentado), SUM(valor_deferido) FROM viagens WHERE motorista_id = ?
        ''', (self.motorista_id,))
        totais = cursor.fetchone()
        total_valor_apresentado = totais[0] if totais[0] else 0.0
        total_valor_deferido = totais[1] if totais[1] else 0.0

        # Calcular resultado
        cursor.execute('''
        SELECT adiantamento FROM motoristas WHERE id = ?
        ''', (self.motorista_id,))
        adiantamento = cursor.fetchone()[0]
        resultado = adiantamento - total_valor_deferido

        # Atualizar status
        status = "Sobrou com o Motorista" if resultado >= 0 else "Depositar ao Motorista"

        cursor.execute('''
        UPDATE motoristas
        SET quantidade_viagens = quantidade_viagens + 1,
            valor_apresentado = ?,
            valor_deferido = ?,
            resultado = ?,
            status = ?
        WHERE id = ?
        ''', (total_valor_apresentado, total_valor_deferido, resultado, status, self.motorista_id))
        conn.commit()
