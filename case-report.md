# Relatório de Negócio e Compliance - Motor de Suitability CVM 30


## 1. Regulação vs. Negócio

Para viabilizar essa operação de forma segura para o negócio e auditável para o regulador, a Genial deve atuar da seguinte forma:

1. **Clareza Visual da Interface:** O alerta no aplicativo deve ser claro, mostrando números da operação (ex: *"Sua carteira passará de 1.67 para 2.82, ultrapassando seu limite de 2.75"*). Para assegurar que o usuário leu o aviso, a caixa de confirmação deve iniciar desmarcada e o botão de compra permanecer desabilitado, sendo liberado apenas após o clique do cliente e a confirmação biométrica.

2. **Armazenamento do Documento:** O documento do termo legal em si (PDF ou texto padrão) fica armazenado em um serviço de arquivos, evitando sobrecarregar o banco de dados com arquivos pesados.

3. **Registro no Banco de Dados**: A tabela de ordens no banco de dados armazena apenas os metadados da operação:
   - Identificador do cliente, da ordem e carimbo de data/hora do aceite;
   - Link/caminho da versão do documento no storage;
   - Hash (SHA-256) do termo aceito: garante a integridade do documento;
   - Valores de risco calculados no momento (risco atual, projetado e limite).

4. **Logs de Auditoria:** O sistema deve gerar logs técnicos imutáveis como tabela append-only ou storage com object lock. Registrando endereço de IP, identificador de dispositivo, token de sessão do cliente e confirmação de validação biométrica (FaceID ou TouchID), comprovando que realmente o usuário efetuou a operação. 


## 2. Desenquadramento Passivo

### Como o motor é reaproveitado

O motor foi dividido em duas camadas para possibilitar esse uso:
- `calculo_risco`: calcula o risco da carteira atual;
- `classificar_risco`: compara esse risco com o perfil e devolve o estado da carteira (Enquadrada, Desenquadramento leve ou Desenquadramento severo).

Portanto o processo não usa a função `validar_suitability`, porque "Aprovado/Rejeitado" são decisões sobre uma ordem. Para o monitoramento de carteira, avalia-se apenas o estado atual.
Então, após o fechamento do pregão da B3 e a consolidação das cotações diárias, uma rotina automatizada executa esse cálculo para as carteiras de clientes.

### Canais de comunicação

A escolha do canal depende da severidade. Quando a carteira está Enquadrada, nenhum aviso é necessário. No desenquadramento leve, o push e o banner no app são suficientes, pois é o canal mais rápido para o investidor de varejo e permite oferecer o rebalanceamento na própria tela. 
No desenquadramento severo, combinam-se push, e-mail e alerta ao assessor: o push dá velocidade, o e-mail serve como registro formal, com o extrato do cálculo, e o assessor faz o contato ativo para ajudar o cliente a ajustar a carteira.
Se o desenquadramento persistir por certo tempo (10 dias por exemplo), o caso é encaminhado ao assessor e ao Compliance, pois, se o cliente não agiu, a instituição precisa de acompanhamento humano e documentado.

## 3. Premissas e decisões de design

### Limiar de corte para rejeição severa

O enunciado do case estabelece que o alerta dispara quando o risco ultrapassa 10% do score do
cliente, mas não define a fronteira exata para a rejeição (trazendo apenas o exemplo com risco 
3.5). Desta forma para montar o motor assumi uma tolerância de 20% acima do score máximo como limite para o desenquadramento leve.
Ou seja, entre 10% e 20% acima do teto, a ordem ainda pode ser liberada mediante termo de ciência. Acima dos 20%, o risco se torna excessivo e o motor rejeita a operação sumariamente.

### Separação entre estado da carteira e decisão da ordem

A lógica foi dividida em duas funções com propósitos distintos. A função `classificar_risco` avalia apenas o risco da carteira do cliente (retornando se a carteira está em conformidade, em desenquadramento leve ou severo). Já a função `validar_suitability` usa essa classificação para tomar uma decisão sobre a compra (Aprovado, Alerta ou Rejeitado). Essa separação permite que a rotina noturna utilize a mesma função de enquadramento da carteira.
