# EcoPontos Cidadãos — Índice e reprodução

**Turma 2CCPY-2026 | Prompt and Artificial Intelligence | Frente C — descarte sustentável | Dupla**  
**Identificação a confirmar pelo grupo:** Arthur Traldi (RM 563477) e Vitor Paiva (RM 565303).

## Índice do ZIP
- `1_visao_produto.md` — personas, RF/RNF, aceite, riscos e rastreabilidade.
- `2_contrato_api.yaml` — contrato OpenAPI 3.0.3, 3 endpoints e schemas/erros.
- `3_arquitetura.md` — diagramas Mermaid, 3 ADRs, observabilidade e segurança.
- `4_slice/` — API Python FastAPI, domínio isolado, adaptadores, pytest, verificação de contrato e GitHub Actions.
- `5_evals_de_ia.md` — 8 casos, guardrails, métricas, regressão, rollout.
- `6_README.md` — este guia.
- `7_demo_video_url.txt` — endereço do vídeo **a completar pelo grupo**.
- `8_certificacao.txt` — identificação, links e resumo de decisões.
- `9_Chat_Log.txt` — relato do auxílio de IA.

## Requisitos e execução local
Python 3.11+ (testado no ambiente de elaboração com Python local). Na raiz do ZIP extraído:

```bash
cd 4_slice
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import yaml; from openapi_spec_validator import validate; validate(yaml.safe_load(open('../2_contrato_api.yaml', encoding='utf-8')))"
ruff check src tests
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
uvicorn src.api.app:app --reload
```

Abrir `http://127.0.0.1:8000/docs` e usar API; também funciona sem credenciais de terceiros, pois o adaptador de IA é fake por padrão.

## Exemplos de requisição reais reproduzíveis
```bash
curl -i 'http://127.0.0.1:8000/points?limit=2&offset=0'
curl -i 'http://127.0.0.1:8000/points/eco-001'
curl -i 'http://127.0.0.1:8000/points/eco-999'
curl -i -X POST 'http://127.0.0.1:8000/ask' -H 'Content-Type: application/json' -d '{"point_id":"eco-001","question":"Aceita papel?"}'
```

Respostas esperadas: 200 com dados fictícios, 200 com ponto, 404 com `NOT_FOUND`, 200 com `answered` e fonte de origem. Erro de parâmetro `limit=0` ⇒ 422 `VALIDATION_ERROR`.

## Teste de contrato automatizado e CI
`tests/test_contract.py` valida estrutura mínima da spec e confere respostas reais da API com schemas escritos no YAML; é evidência candidata ao bônus. O GitHub Actions em `4_slice/.github/workflows/ci.yml` faz validação da spec, lint, pytest e cobertura. **A execução do GitHub Actions depende de publicar o repositório e não foi realizada automaticamente neste documento.**

**Estrutura do repositório:** o workflow já está duplicado em `.github/workflows/ci.yml` na raiz do ZIP, para o GitHub detectá-lo após o push. A cópia em `4_slice/.github/workflows/ci.yml` preserva a estrutura indicada pelo briefing; ambas possuem conteúdo idêntico.

## Evidências verificáveis
- Execução local: `4_slice/evidence/local_validation.txt` (saída literal de ferramenta, produzida durante a preparação).
- CI verde: **não há print nem URL nesta versão; não inventar.** Ao executar no GitHub, capturar screenshot genuíno e preencher `4_slice/evidence/CI_LINK_A_PREENCHER.txt` ou incluir PNG real.
- Vídeo: completar `7_demo_video_url.txt` com URL não listada real de até 3 min, com ambos integrantes e demonstração de `pytest` e CI.

## Roteiro sugerido de vídeo (≤ 3 min)
1. 0:00–0:30: ambos os integrantes se identificam, persona/problema e escolha da frente C.
2. 0:30–1:10: mostrar YAML, GET de sucesso e 404 real.
3. 1:10–1:50: demonstrar `/ask` com fake e recusa fora do escopo.
4. 1:50–2:30: executar `pytest`, mostrar CI verde verdadeiro.
5. 2:30–3:00: explicar troca do LLM via porta, guardrails e bloqueios para produção.

## Limitações honestas
Catálogo e endereços fictícios. `FakeAnswerProvider` não é LLM real nem prova qualidade generativa. Não se coletaram métricas operacionais em produção. O caso EV-08 possui teste de recusa, mas o guardrail de resíduos especiais ainda precisa de validação ampla antes de rollout público. Nenhum token/chave é usado.

## Checklist antes de enviar
- [ ] Confirmar nomes/RMs e contribuições reais; [ ] adicionar link de vídeo válido; [ ] executar Actions e anexar print verdadeiro; [ ] revisar README, links e licença; [ ] conferir prazo de 19/11/2026 às 23h59; [ ] compactar com estrutura intacta.
