"""
Fluxo 1: LOGIN E LOGOUT

CT01 - Login valido abre o Dashboard e o logout volta a tela de login
Criterio: CA01 | Tecnica: PE (classe valida)
"""
from pages.login_page import LoginPage, SENHA_ADMIN, USUARIO_ADMIN


def test_ct01_login_valido_e_logout(driver, base_url, tirar_print):
    # Dado que estou na tela de login
    pagina = LoginPage(driver, base_url).abrir()
    # Quando entro com usuario e senha validos
    pagina.entrar(USUARIO_ADMIN, SENHA_ADMIN)
    # Entao vejo o Dashboard
    assert pagina.dashboard_visivel(), "O login valido deveria abrir o Dashboard"
    tirar_print("dashboard")

    # Quando saio do sistema
    pagina.sair()
    # Entao volto para a tela de login
    assert pagina.tela_de_login_visivel(), "Depois do logout deveria voltar a tela de login"
