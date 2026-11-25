"""Page Object do modulo Leave > Leave List (lista de licencas)."""
from selenium.webdriver.common.by import By

from pages.base_page import BasePage, por_rotulo


class LeavePage(BasePage):
    DATA_INICIAL = por_rotulo("From Date")
    DATA_FINAL = por_rotulo("To Date")
    BOTAO_BUSCAR = (By.XPATH, "//button[normalize-space()='Search']")

    def abrir_lista_de_licencas(self):
        self.abrir_caminho("/web/index.php/leave/viewLeaveList")
        self.visivel(self.DATA_INICIAL)
        self.esperar_carregamento()
        return self

    def preencher_periodo(self, inicio, fim):
        self.digitar_data(self.DATA_INICIAL, inicio)
        self.digitar_data(self.DATA_FINAL, fim)

    def buscar(self):
        self.clicar(self.BOTAO_BUSCAR)
