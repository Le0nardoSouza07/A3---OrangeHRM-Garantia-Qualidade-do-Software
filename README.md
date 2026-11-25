# Testes automatizados do OrangeHRM (demo) - Grupo 8

Garantia da Qualidade de Software - USJT 2026/2 - Prof. Leandro Negreiros

Projeto montado a partir do **kit inicial do professor** (Python + Selenium + pytest, padrao Page Object),
adaptado para o case **OrangeHRM (demonstracao)**: https://opensource-demo.orangehrmlive.com
Somente dados ficticios.

## Casos automatizados

| ID | Caso | Fluxo | Criterio | Arquivo |
|---|---|---|---|---|
| CT01 | Login valido abre o Dashboard e o logout volta ao login | 1. Login e logout | CA01 | tests/test_login.py |
| CT02 | Cadastro de funcionario sem sobrenome | 2. PIM | CA02 | tests/test_pim.py |
| CT03 | Data de nascimento no futuro | 3. Dados pessoais | CA03 | tests/test_dados_pessoais.py |
| CT04 | Senha e confirmacao de senha diferentes | 4. Usuarios do sistema | CA02 | tests/test_usuarios.py |
| CT05 | Candidato com e-mail em formato invalido | 5. Candidatos | CA02 | tests/test_candidatos.py |
| CT06 | Data inicial depois da data final | 6. Lista de licencas | CA03 | tests/test_licencas.py |

## Como rodar (Windows)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python verificar_ambiente.py
pytest
```

| Comando | Para que |
| --- | --- |
| `pytest` | roda todos os testes |
| `pytest tests/test_login.py` | roda um arquivo (um fluxo) |
| `pytest -k ct03` | roda so o teste cujo nome contem "ct03" |
| `pytest --html=relatorio.html --self-contained-html` | gera o relatorio com os resultados |
| `set HEADLESS=1` e depois `pytest` | roda sem abrir a janela do navegador |

## Evidencias

- Teste que **falha** salva um print automatico em `evidencias/` (nome termina em `_FALHOU.png`).
- Cada teste tambem salva prints de apoio (por exemplo `..._mensagem_de_erro.png`).

## Estrutura

```
conftest.py        navegador, login (fixture "logado") e prints
pages/             Page Objects (um por modulo do site)
tests/             um arquivo de teste por fluxo
evidencias/        prints da execucao
verificar_ambiente.py   script do kit que confere o computador
```

## Observacoes

- O demo e compartilhado e lento: as paginas usam `WebDriverWait`.
- Campos sao localizados pelo rotulo (label), porque nao tem id estavel.
- O formato de data e lido do placeholder do campo antes de digitar.
- Teste que falha **fica no relatorio**: pode ser defeito do site.
- Nunca alterar a senha ou o perfil do usuario Admin.
