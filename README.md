# Motor de Validação de Suitability de Carteira (CVM 30)

Implementação do **Case I: Motor de Validação de Suitability de Carteira** para o processo seletivo do Programa de Estágio de Férias da Genial Investimentos (Jan/2027).

---

## Como Executar

O projeto utiliza exclusivamente a biblioteca padrão do Python

### 1. Executar a validação do exemplo do PDF

Executa o motor com os dados de exemplo fornecidos na especificação (CDB XPTO + Ação ABC com nova ordem de FII YYY):

```bash
python3 suitability.py
```

**Saída esperada no terminal (JSON):**

```json
{
  "status": "Aprovado",
  "risco_projetado": 1.81,
  "mensagem": "Ordem executada. Carteira em conformidade."
}
```

---

### 2. Executar os Testes Unitários e Edge Cases

Executa os testes automatizados cobrindo os cenários nominais do PDF (Aprovado, Alerta, Rejeitado) e os casos de borda (carteira vazia, fronteiras exatas de decisão e proteção contra divisão por zero):

```bash
python3 test_suitability.py
```
