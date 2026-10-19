import json


def calculo_risco(carteira: list):
    risco = 0
    valor = 0
    if not carteira:
        return 0
    for ativo in carteira:
        risco += ativo["valor_investido"] * ativo["risco"]
        valor += ativo["valor_investido"]
    if valor == 0:
        return 0.0
    return round(risco / valor, 2)


def validar_suitability(perfil: dict, carteira: list, ordem: dict):
    nova_ordem = {
        "ativo": ordem["ativo"],
        "risco": ordem["risco"],
        "valor_investido": ordem["valor_ordem"],
    }

    carteira_projetada = carteira + [nova_ordem]
    risco_projetado = calculo_risco(carteira_projetada)

    limite_alerta = round(perfil["score_max_risco"] * 1.1, 2)
    limite_severo = round(perfil["score_max_risco"] * 1.2, 2)

    if risco_projetado <= limite_alerta:
        status = "Aprovado"
    elif risco_projetado <= limite_severo:
        status = "Alerta"
    else:
        status = "Rejeitado"

    mensagens = {
        "Aprovado": "Ordem executada. Carteira em conformidade.",
        "Alerta": f"Atenção: O risco da carteira ultrapassará o limite de {limite_alerta}. É necessário termo de ciência.",
        "Rejeitado": "Risco excessivo. A operação viola a política de Suitability.",
    }

    return {
        "status": status,
        "risco_projetado": risco_projetado,
        "mensagem": mensagens[status],
    }


if __name__ == "__main__":
    perfil_exemplo = {"perfil": "Moderado", "score_max_risco": 2.5}

    carteira_exemplo = [
        {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
        {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000},
    ]

    ordem_exemplo = {"ativo": "FII YYY", "risco": 3.5, "valor_ordem": 5000}

    resultado = validar_suitability(perfil_exemplo, carteira_exemplo, ordem_exemplo)

    print(json.dumps(resultado, indent=2, ensure_ascii=False))
