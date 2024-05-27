from database import conectar

def resumo_viagens(motorista_id, data_inicio, data_fim):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT m.nome, v.data, v.valor_apresentado, v.valor_deferido
    FROM motoristas m
    JOIN viagens v ON m.id = v.motorista_id
    WHERE m.id = ? AND v.data BETWEEN ? AND ?
    ''', (motorista_id, data_inicio, data_fim))
    
    viagens = cursor.fetchall()
    conn.close()
    
    total_valor_apresentado = sum(v[2] for v in viagens)
    total_valor_deferido = sum(v[3] for v in viagens)
    
    resumo = {
        "motorista": viagens[0][0] if viagens else None,
        "viagens": viagens,
        "total_valor_apresentado": total_valor_apresentado,
        "total_valor_deferido": total_valor_deferido,
    }
    
    return resumo
