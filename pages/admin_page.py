"""Page Object do modulo Admin > User Management (usuarios do sistema)."""
from pages.base_page import BasePage, por_rotulo


class AdminPage(BasePage):
    CAMPO_SENHA = por_rotulo("Password")
    CAMPO_CONFIRMAR_SENHA = por_rotulo("Confirm Password")

    def abrir_cadastro_de_usuario(self):
        self.abrir_caminho("/web/index.php/admin/saveSystemUser")
        self.visivel(self.CAMPO_SENHA)
        self.esperar_carregamento()
        return self

    def preencher_senhas(self, senha, confirmacao):
        self.digitar(self.CAMPO_SENHA, senha)
        self.digitar(self.CAMPO_CONFIRMAR_SENHA, confirmacao)
        self.sair_do_campo()
