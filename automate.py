from seleniumwire import webdriver  # Importar seleniumwire ao invés de selenium diretamente
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

# Caminho para o ChromeDriver no mesmo nível do script
driver_path = './chromedriver.exe'

# Configurar o serviço do ChromeDriver
service = Service(executable_path=driver_path)

# Configurar as opções do ChromeDriver
chrome_options = webdriver.ChromeOptions()

# Lista de credenciais
credentials = [
    {"email": "escritoriopesquisa03@outlook.com", "password": "rus6h07seQl"},
    {"email": "conta.pessoalrs@outlook.com", "password": "1PrB977TqsA"},
    {"email": "conta.pess@outlook.com", "password": "1PrB977T25"},
    {"email": "c.pessoalrs@outlook.com", "password": "tI8aatvBCpu"},
    {"email": "contapessrs@outlook.com", "password": "HLHOrrl"},
    {"email": "c.pess@outlook.com", "password": "CUCHff"},
    {"email": "minha.contars@outlook.com", "password": "GNhKZExE"},
    {"email": "minhapessoalrs@outlook.com", "password": "mmJ9uku7un"},
    {"email": "cta.pessoal@outlook.com", "password": "RDuVy5cx"},
    {"email": "cta.pess@outlook.com", "password": "thIVnc3U30"},
    {"email": "contapessoal10rs@outlook.com", "password": "0xZ9Yc"}
]

# Função para realizar login e pesquisa
def login_and_search(email, password):
    # Iniciar o WebDriver com o serviço configurado
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Acessar diretamente a página de login
        driver.get("https://portalimendes.com.br/login")
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Encontrar os campos de e-mail e senha e preencher com as credenciais
        email_field = driver.find_element(By.ID, "email-login")
        password_field = driver.find_element(By.ID, "senha-login")
        
        email_field.send_keys(email)
        password_field.send_keys(password)
        
        # Encontrar e clicar no botão de login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Entrar')]")
        login_button.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Clicar no botão "Acessar"
        acessar_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Acessar')]")
        acessar_button.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Clicar no botão "editar perfil"
        editar_perfil = driver.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/a[1]")
        editar_perfil.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Clicar em "UF"
        uf_perfil = driver.find_element(By.XPATH, "//*[@id='selectUf']")
        uf_perfil.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        
        # Clicar em "Atividade"
        atividade_perfil = driver.find_element(By.XPATH, "//*[@id='selectCnae']")
        atividade_perfil.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        
        # Clicar em "Atividade"
        regime_perfil = driver.find_element(By.XPATH, "//*[@id='selectCtrib']")
        regime_perfil.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        
        # Clicar em "Atividade"
        salvar_perfil = driver.find_element(By.XPATH, "//*[@id='appProfilePoc']/div/button")
        salvar_perfil.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        
        # Selecionar "NCM" no dropdown
        select_criterio = driver.find_element(By.ID, "selectCriterio")
        select_criterio.click()
        
        ncm_option = driver.find_element(By.XPATH, "//select[@id='selectCriterio']/option[contains(text(), 'NCM')]")
        ncm_option.click()
        
        # Esperar a página carregar
        time.sleep(5)
        
        # Encontrar o campo de pesquisa, digitar o NCM e enviar
        search_field = driver.find_element(By.XPATH, "//input[@id='valor' and @placeholder='Informe a NCM']")
        search_field.send_keys("22021000")
        search_field.send_keys(Keys.RETURN)
        
        # Esperar os resultados carregarem
        time.sleep(5)
        
        # Capturar os dados do "Preview" na aba "Network" do DevTools
        for request in driver.requests:
            if request.response and 'portal_imendes/v1/public/Consult' in request.url:
                try:
                    data = json.loads(request.response.body.decode('utf-8'))
                    print(f"Console Output for {email}:")
                    print(json.dumps(data, indent=2))
                    with open(f'output_{email}.json', 'w') as f:
                        f.write(json.dumps(data, indent=2))
                except Exception as e:
                    print(f"Error processing request for {email}: {e}")
    
    finally:
        # Fechar o navegador
        driver.quit()

# Selecionar a primeira credencial disponível
if credentials:
    email, password = credentials.pop(0).values()
    login_and_search(email, password)
else:
    print("No credentials available.")
