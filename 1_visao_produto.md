# EcoPontos Cidadãos — Visão de produto

**Global Solution 2026.2 — CitizenTech | Frente C: descarte e sustentabilidade**  
**Curso/turma:** Engenharia de Software — 2CCPY-2026  
**Disciplina:** Prompt and Artificial Intelligence | **Modalidade:** dupla  
**Grupo (confirmar dados antes de enviar):** Arthur Traldi — RM 563477; Vitor Paiva — RM 565303.

## Problema e oportunidade
**Problema em uma frase:** moradores que precisam descartar materiais recicláveis não encontram facilmente pontos de coleta adequados nem orientações verificáveis de descarte.

## Personas
- **Primária — Marina, moradora de 34 anos:** reside em bairro com coleta seletiva irregular; usa smartphone básico; precisa saber se um ponto recebe determinado material e como prepará-lo; **não é** funcionária de triagem, nem especialista em reciclagem.
- **Secundária — Lucas, operador de cooperativa:** precisa consultar o cadastro e sinalizar à prefeitura dados desatualizados; **não é** responsável por atualizar automaticamente o cadastro por esta API.

## Proposta e limites de confiança
API demonstrativa que consulta cadastro estruturado de ecopontos e explica o descarte com um adaptador de IA substituível. **O catálogo do slice é inteiramente fictício e não deve ser utilizado como guia de endereços reais.** O campo `updated_at` indica atualização do cadastro de demonstração, não verificação de disponibilidade em tempo real. O modelo só pode reescrever fatos presentes no cadastro, jamais inventar horários, elegibilidade ou localização.

## Requisitos funcionais (RF)
| ID | Requisito | Evidência |
|---|---|---|
| RF-01 | Listar pontos com `limit` e `offset` | `GET /points`, teste de paginação |
| RF-02 | Filtrar pontos pelo material aceito | `GET /points?material=papel`, teste de filtro |
| RF-03 | Consultar detalhe por identificador | `GET /points/{id}`, teste de sucesso |
| RF-04 | Responder com erro padronizado para identificador inexistente | 404 `ErrorResponse`, teste |
| RF-05 | Responder pergunta sobre descarte usando contexto de um ponto cadastrado | `POST /ask`, fake do adaptador |
| RF-06 | Recusar perguntas fora da finalidade e não responder sem evidência | `POST /ask`, `status=refused` |
| RF-07 | Detectar provedor indisponível e retornar erro padronizado | `POST /ask`, 503 e teste |

## Requisitos não funcionais (RNF)
| ID | Meta mensurável | Como aferir |
|---|---|---|
| RNF-01 | Latência p95 de GETs abaixo de 400 ms com 30 RPS por 5 min no ambiente de homologação | teste de carga; meta ainda não verificada em produção |
| RNF-02 | Cobertura de linhas do slice ≥ 80% | `pytest --cov=src --cov-report=term-missing` na CI |
| RNF-03 | Disponibilidade mensal ≥ 99,5% em horário de atendimento previsto | monitoramento de uptime externo após implantação |
| RNF-04 | 0 segredos versionados e 0 chamadas externas nos testes unitários | revisão e testes com fake |
| RNF-05 | 100% das respostas de IA contendo status `answered` baseadas exclusivamente em dados da fonte | avaliação de grounding em suíte de 30 casos |

## Critérios de aceite (Dado / Quando / Então)
1. **CA-01:** Dado um catálogo com três pontos, quando solicito `GET /points?limit=2&offset=0`, então recebo 200 com dois itens e `total=3`.
2. **CA-02:** Dado um material `papel`, quando filtro pontos por esse material, então cada ponto retornado aceita `papel`.
3. **CA-03:** Dado um identificador válido, quando consulto `GET /points/{id}`, então recebo 200 e campos conforme schema `Point`.
4. **CA-04:** Dado um identificador inexistente, quando consulto seu detalhe, então recebo 404 com `error.code=NOT_FOUND`.
5. **CA-05:** Dada uma dúvida sobre material aceito em ponto existente, quando envio `POST /ask`, então recebo `answered` e resposta restrita ao cadastro.
6. **CA-06:** Dada pergunta sobre tema alheio a descarte, quando envio `POST /ask`, então recebo `refused`, sem orientação inventada.
7. **CA-07:** Dado provedor de IA indisponível, quando envio `POST /ask`, então recebo 503 com código `AI_UNAVAILABLE`.
8. **CA-08:** Dado `limit=0`, quando consulto listagem, então recebo 422 e corpo de erro padronizado.

## Fora do escopo
- Não criar agendamentos, rotas de transporte, rastrear caminhões ou garantir funcionamento em tempo real.
- Não usar endereço/catálogo como dado oficial ou georreferenciado da prefeitura; não atualizar o cadastro por esta API.
- Não tratar informações pessoais identificáveis nem fazer recomendações de descarte de materiais perigosos.

## Riscos e mitigação
| Risco | Impacto | Mitigação | Risco residual |
|---|---|---|---|
| LLM inventar materiais ou condições | Informação incorreta ao cidadão | factualidade validada por cadastro e guardrail; recusa sem contexto; suíte de regressão | fake não substitui homologação real |
| Cadastro desatualizado | Deslocamento desnecessário | `updated_at`, advertência explícita, rotina de conferência operacional | base de demonstração não certificada |
| Prompt injection | desvio da finalidade | classificação do escopo antes do provedor, sem acesso do modelo a credenciais; saída limitada | avaliação adicional antes do público |
| Dependência do provedor | falha de atendimento | porta de IA, timeout/fallback, 503 rastreável | precisa monitorar serviço real |

## Rastreabilidade
RF-01/02 → `/points` → `test_list.py`; RF-03/04 → `/points/{id}` → `test_detail.py`; RF-05/06/07 → `/ask` → `test_ask.py`; CA-08 → `test_errors.py`. Contrato detalhado em `2_contrato_api.yaml` e decisões em `3_arquitetura.md`.
