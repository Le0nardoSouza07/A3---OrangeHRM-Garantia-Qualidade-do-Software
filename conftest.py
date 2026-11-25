"""
Configuracao compartilhada pelos testes (o pytest carrega este arquivo sozinho).

- Cria e fecha o navegador para cada teste (fixture "driver").
- Faz login como administrador quando o teste pede a fixture "logado".
- Tira um print da tela quando um teste falha (pasta "evidencias").
- Fixture "tirar_print": salva um print em qualquer momento (evidencia de que passou).

Variaveis de ambiente opcionais:
  BASE_URL  endereco do sistema (padrao: https://opensource-demo.orangehrmlive.com)
  HEADLESS  use HEADLESS=1 para rodar sem abrir a janela do navegador
"""
import os
from datetime import datetime

import pytest
from selenium import webdriver

from pages.login_page import LoginPage, SENHA_ADMIN, USUARIO_ADMIN

# ALTERADO PARA O CASE DO GRUPO 8: OrangeHRM (demonstracao)
BASE_URL = os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com").rstrip("/")
PASTA_EVIDENCIAS = os.path.join(os.path.dirname(__file__), "evidencias")


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def driver():
    opcoes = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":
        opcoes.add_argument("--headless=new")
    if os.getenv("CI") == "1":  # servidores/containers (ex.: GitHub Actions)
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1280,900")
    opcoes.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    if os.getenv("CHROME_BINARY"):
        opcoes.binary_location = os.getenv("CHROME_BINARY")

    # O Selenium Manager baixa sozinho o driver compativel com o Chrome instalado.
    navegador = webdriver.Chrome(options=opcoes)
    # O OrangeHRM e lento e carrega por partes: usamos esperas explicitas
    # (WebDriverWait) nas paginas, entao a espera implicita fica desligada.
    navegador.implicitly_wait(0)
    yield navegador
    navegador.quit()


@pytest.fixture
def logado(driver, base_url):
    """Abre o sistema e entra como administrador (pre-condicao da maioria dos testes)."""
    pagina = LoginPage(driver, base_url).abrir()
    pagina.entrar(USUARIO_ADMIN, SENHA_ADMIN)
    assert pagina.dashboard_visivel(), "Pre-condicao falhou: o login nao abriu o Dashboard"
    return driver


@pytest.fixture
def tirar_print(driver, request):
    """Devolve uma funcao que salva um print com uma etiqueta (evidencia da execucao)."""

    def _tirar(etiqueta):
        os.makedirs(PASTA_EVIDENCIAS, exist_ok=True)
        nome = "".join(c if c.isalnum() else "_" for c in request.node.name)
        driver.save_screenshot(os.path.join(PASTA_EVIDENCIAS, f"{nome}_{etiqueta}.png"))

    return _tirar


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Quando um teste falha, salva um print da tela como evidencia do defeito."""
    resultado = yield
    relatorio = resultado.get_result()
    if relatorio.when == "call" and relatorio.failed:
        navegador = item.funcargs.get("driver")
        if navegador:
            os.makedirs(PASTA_EVIDENCIAS, exist_ok=True)
            momento = datetime.now().strftime("%Y%m%d-%H%M%S")
            nome = "".join(c if c.isalnum() else "_" for c in item.name)
            navegador.save_screenshot(os.path.join(PASTA_EVIDENCIAS, f"{momento}_{nome}_FALHOU.png"))
