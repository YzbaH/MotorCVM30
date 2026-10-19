from suitability import validar_suitability, calculo_risco

perfil = {"perfil": "Moderado", "score_max_risco": 2.5}

carteira_base = [
    {"ativo": "CDB XPTO", "risco": 1.2, "valor_investido": 50000},
    {"ativo": "Ação ABC", "risco": 4.0, "valor_investido": 10000},
]

# Caso base do case
r1 = validar_suitability(
    perfil,
    carteira_base,
    {"ativo": "FII YYY", "risco": 3.5, "valor_ordem": 5000},
)
assert r1["status"] == "Aprovado"
assert r1["risco_projetado"] == 1.81
assert r1["mensagem"] == "Ordem executada. Carteira em conformidade."

# Caso Alerta
r2 = validar_suitability(
    perfil,
    carteira_base,
    {"ativo": "Ação Volátil", "risco": 4.5, "valor_ordem": 41000},
)
assert r2["status"] == "Alerta"
assert 2.75 < r2["risco_projetado"] <= 3.00
assert "Atenção: O risco da carteira ultrapassará o limite de 2.75" in r2["mensagem"]

# Caso Rejeitado
r3 = validar_suitability(
    perfil,
    carteira_base,
    {"ativo": "Cripto / Derivativos", "risco": 5.0, "valor_ordem": 100000},
)
assert r3["status"] == "Rejeitado"
assert r3["risco_projetado"] > 3.00
assert r3["mensagem"] == "Risco excessivo. A operação viola a política de Suitability."

# Edge case Carteira vazia
r4 = validar_suitability(
    perfil,
    [],
    {"ativo": "Tesouro Selic", "risco": 1.0, "valor_ordem": 5000},
)
assert r4["status"] == "Aprovado"
assert r4["risco_projetado"] == 1.0

# Edge case fronteira exata no limiar de Alerta (2.75)
# regra é <= 2.75
r5 = validar_suitability(
    perfil,
    [],
    {"ativo": "Ativo Limite Alerta", "risco": 2.75, "valor_ordem": 10000},
)
assert r5["status"] == "Aprovado"
assert r5["risco_projetado"] == 2.75

# Edge case fronteira exata no limiar de Rejeição
# 3.00 "Alerta" (<= 3.00); 3.01 "Rejeitado" (> 3.00)
r6_alerta = validar_suitability(
    perfil,
    [],
    {"ativo": "Ativo Limite Severo", "risco": 3.00, "valor_ordem": 10000},
)
assert r6_alerta["status"] == "Alerta"
assert r6_alerta["risco_projetado"] == 3.00

r6_rejeitado = validar_suitability(
    perfil,
    [],
    {"ativo": "Ativo Ultrapassa Severo", "risco": 3.01, "valor_ordem": 10000},
)
assert r6_rejeitado["status"] == "Rejeitado"
assert r6_rejeitado["risco_projetado"] == 3.01

# edge case divisão por zero
r7 = calculo_risco([{"ativo": "Ativo Sem Saldo", "risco": 2.0, "valor_investido": 0}])
assert r7 == 0.0

print("Todos os testes passaram")
