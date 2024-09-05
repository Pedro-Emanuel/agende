import os
import json
import time
import getch
import threading
import locale
from datetime import datetime, timedelta
from enum import Enum, auto

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

class TipoRefeicao(Enum):
    ALMOCO = auto()
    JANTAR = auto()

    def __str__(self):
        return self.name.capitalize()

    @property
    def valor(self):
        return '2' if self == TipoRefeicao.ALMOCO else '3'

class AgendadorRU:
    def __init__(self):
        self.usuario, self.senha = self.obter_credenciais()
        self.driver = self._configurar_webdriver()

    def getPass(self):
        print("Senha: ", end='', flush=True)
        passwor = ''
        while True:
            x = getch.getch()
            # x = msvcrt.getch().decode("utf-8")
            if x == '\r' or x == '\n':
                break
            print('*', end='', flush=True)
            passwor +=x
        print('')
        return passwor

    def obter_credenciais(self):
        arquivo = '.credenciais_agende'
        if os.path.exists(arquivo):
            with open(arquivo, 'r') as f:
                cred = json.load(f)
                return cred['usuario'], cred['senha']
        else:
            print("Configuração inicial de credenciais")
            usuario = input("Usuário: ")
            senha = self.getPass()
            with open(arquivo, 'w') as f:
                json.dump({'usuario': usuario, 'senha': senha}, f)
            print("Credenciais salvas")
            return usuario, senha

    def _configurar_webdriver(self):
        print("Configurando navegador...")
        opcoes = webdriver.ChromeOptions()
        opcoes.add_argument("--no-sandbox")
        opcoes.add_argument("--disable-dev-shm-usage")
        opcoes.add_argument("--headless")
        opcoes.add_argument("--disable-gpu")
        opcoes.add_argument("--window-size=1920x1080")

        servico = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=servico, options=opcoes)

    def esperar_elemento(self, tipo, elemento, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((tipo, elemento))
        )

    def fazer_login(self):
        print("Realizando login...")
        self.driver.get('https://si3.ufc.br/sigaa/verTelaLogin.do')
        self.esperar_elemento(By.NAME, 'user.login').send_keys(self.usuario)
        self.esperar_elemento(By.NAME, 'user.senha').send_keys(self.senha)
        self.esperar_elemento(By.NAME, 'entrar').click()
        print("Login realizado")

    def lidar_com_aviso_login(self):
        print("Verificando avisos...")
        while self.driver.current_url == 'https://si3.ufc.br/sigaa/telaAvisoLogon.jsf':
            self.esperar_elemento(By.CSS_SELECTOR, 'input[type="submit"]').click()
        while self.driver.current_url != 'https://si3.ufc.br/sigaa/paginaInicial.do':
            time.sleep(1)
        print("Navegação concluída")

    def ir_para_menu_estudante(self):
        self.esperar_elemento(By.CSS_SELECTOR, 'li.menus').find_element(By.TAG_NAME, "a").click()

    def navegar_para_agendamento(self):
        print("Acessando agendamento...")
        self.lidar_com_aviso_login()
        print("Acessando menu do estudante...")
        self.ir_para_menu_estudante()
        menu = self.esperar_elemento(By.ID, "cmAction-96")
        ActionChains(self.driver).move_to_element(menu).perform()
        self.esperar_elemento(By.ID, "cmAction-97").click()

    def preencher_formulario(self, data, tipo_refeicao):
        datafmt = datetime.strptime(data, "%d%m%Y").strftime("%d-%m-%Y")
        print(f"Agendando: {tipo_refeicao} para {datafmt} ({datetime.strptime(data, '%d%m%Y').strftime('%A')})")
        self.esperar_elemento(By.ID, "formulario:tipo_refeicao")
        self.esperar_elemento(By.ID, "formulario:data_agendamento").send_keys(data)
        Select(self.esperar_elemento(By.ID, "formulario:tipo_refeicao")).select_by_value(tipo_refeicao.valor)

        opcoes = [0]
        while len(opcoes) == 1:
            try:
                sel_horario = Select(self.esperar_elemento(By.ID, "formulario:horario_agendado"))
                opcoes = [o.get_attribute('value') for o in sel_horario.options]
            except StaleElementReferenceException:
                pass

        valor_horario = '53' if tipo_refeicao == TipoRefeicao.ALMOCO else '54'
        if valor_horario in opcoes:
            sel_horario.select_by_value(valor_horario)
        else:
            print("Nenhum horário válido")
            return False, "Horário inválido"

        self.esperar_elemento(By.ID, "formulario:cadastrar_agendamento_bt").click()
        return self.verificar_mensagens()

    def verificar_mensagens(self):
        erros, info = [], []
        evento = threading.Event()

        def encontrar_erros():
            nonlocal erros
            try:
                erros = self.driver.find_elements(By.CSS_SELECTOR, "ul.erros li")
                if erros: evento.set()
            except Exception as e:
                print(f"Erro ao buscar erros: {e.__class__.__name__}")

        def encontrar_info():
            nonlocal info
            try:
                info = self.driver.find_elements(By.CSS_SELECTOR, "ul.info li")
                if info: evento.set()
            except Exception as e:
                print(f"Erro ao buscar info: {e.__class__.__name__}")

        threading.Thread(target=encontrar_erros).start()
        threading.Thread(target=encontrar_info).start()

        evento.wait(timeout=10)

        if erros:
            print(f"Erro: {erros[0].text}")
            return False, erros[0].text
        elif info:
            print(f"Sucesso: {info[0].text}")
            return True, info[0].text
        else:
            print("Nenhuma mensagem encontrada")
            return False, "Sem mensagem"

    def obter_proximo_dia_util(self, data):
        proximo = data + timedelta(days=1)
        while proximo.weekday() >= 5:
            proximo += timedelta(days=1)
        return proximo

    def agendar_refeicoes_automaticas(self):
        print("________________________________")
        print("Iniciando agendamento automático")
        data_atual = datetime.now().date()
        dias_agendar = []
        limite_dias = 3

        while len(dias_agendar) < limite_dias:
            proximo = self.obter_proximo_dia_util(data_atual)
            if (proximo - datetime.now().date()).days <= limite_dias:
                dias_agendar.append(proximo)
                data_atual = proximo
            else:
                break

        print(f"Agendando para {len(dias_agendar)} dias")
        print('')
        
        for data in dias_agendar:
            data_fmt = data.strftime("%d%m%Y")

            for tipo in TipoRefeicao:
                try:
                    sucesso, msg = self.preencher_formulario(data_fmt, tipo)
                    if not sucesso and "Existe agendamento" in msg:
                        print(f"{tipo} já agendado")
                    elif not sucesso:
                        print(f"Erro ao agendar {tipo}: {msg}")
                    
                    self.ir_para_menu_estudante()
                    menu = self.esperar_elemento(By.ID, "cmAction-96")
                    ActionChains(self.driver).move_to_element(menu).perform()
                    self.esperar_elemento(By.ID, "cmAction-97").click()
                except Exception as e:
                    print(f"Erro inesperado: {e.__class__.__name__}")
                finally:
                    print("")

        print("Agendamento concluído")
        print("________________________________")

    def encerrar(self):
        self.driver.quit()
        print("Sessão encerrada")

def main():
    print("Agendador Automático do RU")
    agendador = AgendadorRU()
    
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        
    try:
        agendador.fazer_login()
        agendador.navegar_para_agendamento()
        agendador.agendar_refeicoes_automaticas()
    except Exception as e:
        print(f"Erro crítico: {e.__class__.__name__}")
        print("Tente novamente mais tarde ou verifique suas credenciais")
    finally:
        agendador.encerrar()

if __name__ == "__main__":
    main()