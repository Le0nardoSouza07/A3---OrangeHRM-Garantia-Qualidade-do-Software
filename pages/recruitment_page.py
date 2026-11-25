"""Page Object do modulo Recruitment > Candidates (candidatos)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage, por_rotulo


class RecruitmentPage(BasePage):
    PRIMEIRO_NOME = (By.NAME, "firstName")
    SOBRENOME = (By.NAME, "lastName")
    EMAIL = por_rotulo("Email")
    BOTAO_SALVAR = (By.CSS_SELECTOR, "button[type='submit']")

    def abrir_cadastro_de_candidato(self):
        self.abrir_caminho("/web/index.php/recruitment/addCandidate")
        self.visivel(self.PRIMEIRO_NOME)
        self.esperar_carregamento()
        return self

    def preencher_candidato(self, primeiro_nome, sobrenome, email):
        self.digitar(self.PRIMEIRO_NOME, primeiro_nome)
        self.digitar(self.SOBRENOME, sobrenome)
        self.digitar(self.EMAIL, email)

    def salvar(self):
        self.clicar(self.BOTAO_SALVAR)
