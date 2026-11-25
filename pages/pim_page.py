"""Page Object do modulo PIM (cadastro de funcionarios e dados pessoais)."""
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, por_rotulo

TOAST = (By.CSS_SELECTOR, ".oxd-toast")


class PimPage(BasePage):
    PRIMEIRO_NOME = (By.NAME, "firstName")
    SOBRENOME = (By.NAME, "lastName")
    BOTAO_SALVAR = (By.CSS_SELECTOR, "button[type='submit']")
    # Na tela de dados pessoais ha varios botoes Save; o primeiro e o do formulario principal.
    SALVAR_DADOS_PESSOAIS = (By.XPATH, "(//button[@type='submit'])[1]")
    DATA_NASCIMENTO = por_rotulo("Date of Birth")

    # ---- cadastro de funcionario ----
    def abrir_cadastro(self):
        self.abrir_caminho("/web/index.php/pim/addEmployee")
        self.visivel(self.PRIMEIRO_NOME)
        self.esperar_carregamento()
        return self

    def preencher_nome(self, primeiro_nome, sobrenome=None):
        self.digitar(self.PRIMEIRO_NOME, primeiro_nome)
        if sobrenome:
            self.digitar(self.SOBRENOME, sobrenome)

    def salvar(self):
        self.clicar(self.BOTAO_SALVAR)

    def criar_funcionario(self, primeiro_nome, sobrenome):
        """Cadastra um funcionario ficticio. Ao salvar, o sistema abre os dados pessoais dele."""
        self.abrir_cadastro()
        self.preencher_nome(primeiro_nome, sobrenome)
        self.salvar()
        self.wait.until(EC.url_contains("viewPersonalDetails"))
        # espera o formulario carregar os dados (evita digitar antes de o site preencher os campos)
        self.wait.until(lambda d: d.find_element(*self.PRIMEIRO_NOME).get_attribute("value") == primeiro_nome)
        self.esperar_carregamento()

    # ---- dados pessoais ----
    def definir_data_nascimento(self, data):
        self.digitar_data(self.DATA_NASCIMENTO, data)

    def salvar_dados_pessoais(self):
        self.clicar(self.SALVAR_DADOS_PESSOAIS)

    def resultado_do_salvamento(self, tempo=10):
        """Devolve ('erro', [mensagens]) ou ('sucesso', textos) conforme o que aparecer primeiro."""
        limite = time.time() + tempo
        while time.time() < limite:
            erros = self.textos_de_erro(tempo=0.5)
            if erros:
                return "erro", erros
            avisos = [t.text for t in self.driver.find_elements(*TOAST) if t.text.strip()]
            if avisos:
                return "sucesso", avisos
        return "nada", []

    # ---- limpeza ----
    def excluir_funcionario(self, sobrenome):
        """Exclui o funcionario ficticio criado pelo teste (busca pelo sobrenome unico)."""
        self.abrir_caminho("/web/index.php/pim/viewEmployeeList")
        self.esperar_carregamento()
        self.digitar(por_rotulo("Employee Name"), sobrenome)
        self.clicar((By.XPATH, "//button[normalize-space()='Search']"))
        lixeira = (
            By.XPATH,
            f"//div[contains(@class,'oxd-table-card')][.//div[normalize-space()='{sobrenome}']]"
            "//button[.//i[contains(@class,'bi-trash')]]",
        )
        self.clicar(lixeira)
        self.clicar((By.XPATH, "//button[normalize-space()='Yes, Delete']"))
