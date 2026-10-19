import json


def calculo_risco(carteira: list) -> float:
    """
    Calcula a média ponderada da carteira e retorna o valor bruto.
    """
    risco = 0
    valor = 0

    if not carteira:
        return 0.0

    for ativo in carteira:
        risco += ativo["valor_investido"] * ativo["risco"]
        valor += ativo["valor_investido"]

    if valor == 0:
        return 0.0
    return risco / valor


FATOR_ALERTA = 0.10
FATOR_SEVERO = 0.20


def classificar_risco(risco: float, score_max: float) -> str:
    """Estado de risco da carteira frente ao perfil."""
    if risco <= score_max * (1 + FATOR_ALERTA):
        return "Enquadrada"

    if risco <= score_max * (1 + FATOR_SEVERO):
        return "Desenquadramento leve"

    return "Desenquadramento severo"


DECISAO_POR_ESTADO = {
    "Enquadrada": "Aprovado",
    "Desenquadramento leve": "Alerta",
    "Desenquadramento severo": "Rejeitado",
}


def validar_suitability(perfil: dict, carteira: list, ordem: dict) -> dict:
    """Classifica uma ordem com base no risco projetado da carteira e no perfil do cliente"""
    nova_ordem = {
        "ativo": ordem["ativo"],
        "risco": ordem["risco"],
        "valor_investido": ordem["valor_ordem"],
    }

    carteira_projetada = carteira + [nova_ordem]
    risco_projetado = calculo_risco(carteira_projetada)
    estado = classificar_risco(risco_projetado, perfil["score_max_risco"])

    limite_alerta = round(perfil["score_max_risco"] * (1 + FATOR_ALERTA), 2)
    mensagens = {
        "Aprovado": "Ordem executada. Carteira em conformidade.",
        "Alerta": f"Atenção: O risco da carteira ultrapassará o limite de {limite_alerta}. É necessário termo de ciência.",
        "Rejeitado": "Risco excessivo. A operação viola a política de Suitability.",
    }

    status = DECISAO_POR_ESTADO[estado]

    return {
        "status": status,
        "risco_projetado": round(risco_projetado, 2),
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
