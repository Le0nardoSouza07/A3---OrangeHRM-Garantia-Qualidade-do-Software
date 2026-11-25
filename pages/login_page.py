"""Page Object da tela de login e do menu de logout do OrangeHRM (demo)."""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

# Credenciais publicas do demo (aparecem na propria tela de login).
USUARIO_ADMIN = "Admin"
SENHA_ADMIN = "admin123"


class LoginPage(BasePage):
    CAMPO_USUARIO = (By.NAME, "username")
    CAMPO_SENHA = (By.NAME, "password")
    BOTAO_LOGIN = (By.CSS_SELECTOR, "button[type='submit']")
    TITULO_DASHBOARD = (By.XPATH, "//h6[normalize-space()='Dashboard']")
    MENU_USUARIO = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
    LINK_LOGOUT = (By.XPATH, "//a[normalize-space()='Logout']")

    def abrir(self):
        self.abrir_caminho("/web/index.php/auth/login")
        self.visivel(self.CAMPO_USUARIO)
        return self

    def entrar(self, usuario, senha):
        self.digitar(self.CAMPO_USUARIO, usuario)
        self.digitar(self.CAMPO_SENHA, senha)
        self.clicar(self.BOTAO_LOGIN)

    def dashboard_visivel(self):
        try:
            self.visivel(self.TITULO_DASHBOARD)
            return "/dashboard" in self.driver.current_url
        except TimeoutException:
            return False

    def sair(self):
        self.clicar(self.MENU_USUARIO)
        self.clicar(self.LINK_LOGOUT)

    def tela_de_login_visivel(self):
        try:
            self.visivel(self.CAMPO_USUARIO)
            return "/auth/login" in self.driver.current_url
        except TimeoutException:
            return False
