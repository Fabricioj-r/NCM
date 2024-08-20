#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template_string
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import random

app = Flask(__name__)

# Caminho para o ChromeDriver
caminho_driver = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')

# Configurar o serviço do ChromeDriver
servico = Service(executable_path=caminho_driver)

# Configurar as opções do ChromeDriver
opcoes_chrome = webdriver.ChromeOptions()
opcoes_chrome.add_argument("--disable-gpu")
opcoes_chrome.add_argument("--no-sandbox")
opcoes_chrome.add_argument("--disable-dev-shm-usage")
opcoes_chrome.add_argument("--window-size=1920,1080")
opcoes_chrome.add_argument("--headless")  # Adiciona o modo headless

# Lista de credenciais
credenciais = [
    {"email": "escritoriopesquisa03@outlook.com", "senha": "rus6h07seQl"},
    {"email": "conta.pessoalrs@outlook.com", "senha": "1PrB977TqsA"},
    {"email": "conta.pess@outlook.com", "senha": "1PrB977T25"},
    {"email": "c.pessoalrs@outlook.com", "senha": "tI8aatvBCpu"},
    {"email": "contapessrs@outlook.com", "senha": "HLHOrrl"},
    {"email": "c.pess@outlook.com", "senha": "CUCHff"},
    {"email": "minha.contars@outlook.com", "senha": "GNhKZExE"},
    {"email": "minhapessoalrs@outlook.com", "senha": "mmJ9uku7un"},
    {"email": "cta.pessoal@outlook.com", "senha": "RDuVy5cx"},
    {"email": "cta.pess@outlook.com", "senha": "thIVnc3U30"},
    {"email": "contapessoal10rs@outlook.com", "senha": "0xZ9Yc"}
]

# Função para limpar os arquivos de saída
def limpar_arquivos_saida():
    for arquivo in os.listdir():
        if arquivo.startswith('output_') and arquivo.endswith('.json'):
            os.remove(arquivo)

# Função para realizar login e pesquisa
def realizar_login_e_pesquisa(email, senha, atividade, regime, uf, ncm):
    limpar_arquivos_saida()
    navegador = webdriver.Chrome(service=servico, options=opcoes_chrome)
    
    try:
        print(f"Iniciando login com {email}")
        
        # Navega até a página de login do portal
        navegador.get("https://portalimendes.com.br/login")
        time.sleep(5)
        
        # Aguarda até que o campo de email esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "email-login")))
        
        # Insere o email no campo de login
        navegador.find_element(By.ID, "email-login").send_keys(email)
        
        # Insere a senha no campo de login
        navegador.find_element(By.ID, "senha-login").send_keys(senha)
        
        # Clica no botão de entrar
        navegador.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Entrar')]").click()
        
        # Aguarda até que o botão 'Acessar' esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Acessar')]")))
        time.sleep(1)
        
        # Clica no botão 'Acessar'
        navegador.find_element(By.XPATH, "//button[contains(text(), 'Acessar')]").click()
        time.sleep(1)
        
        # Aguarda até que o link para editar perfil esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/a[1]")))
        time.sleep(2)
        
        # Clica no link para editar perfil
        navegador.find_element(By.XPATH, "//*[@id='app']/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/a[1]").click()
        time.sleep(1)
        
        # Aguarda até que o campo de seleção de UF esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='selectUf']")))      
        # Seleciona a UF correspondente
        navegador.find_element(By.XPATH, "//*[@id='selectUf']").send_keys(uf)
        time.sleep(1)
        
        # Aguarda até que o campo de seleção de CNAE (atividade) esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='selectCnae']")))
        # Seleciona a atividade correspondente
        navegador.find_element(By.XPATH, "//*[@id='selectCnae']").send_keys(atividade)
        time.sleep(1)
        
        # Aguarda até que o campo de seleção de regime tributário esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='selectCtrib']")))
        # Seleciona o regime tributário correspondente
        navegador.find_element(By.XPATH, "//*[@id='selectCtrib']").send_keys(regime)
        time.sleep(1)
        
        # Preenche o campo de Receita Bruta em 12 meses (R$) se o regime selecionado for "Simples Nacional"
        if regime == "Simples Nacional":
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='receitaBruta']")))
            campo_receita_bruta = navegador.find_element(By.XPATH, "//*[@id='receitaBruta']")
            campo_receita_bruta.clear()
            campo_receita_bruta.send_keys("150000.00")
        
        # Clica no botão de salvar perfil
        navegador.find_element(By.XPATH, "//*[@id='appProfilePoc']/div/button").click()
        time.sleep(1)
        
        # Aguarda até que o campo de seleção de critério esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.ID, "selectCriterio")))
        # Clica no campo de seleção de critério
        navegador.find_element(By.ID, "selectCriterio").click()
        
        # Seleciona a opção 'NCM' no campo de seleção de critério
        navegador.find_element(By.XPATH, "//select[@id='selectCriterio']/option[contains(text(), 'NCM')]").click()
        
        # Aguarda até que o campo de entrada de NCM esteja presente na página
        WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='valor' and @placeholder='Informe a NCM']")))
        # Insere o valor do NCM no campo de pesquisa
        campo_pesquisa = navegador.find_element(By.XPATH, "//input[@id='valor' and @placeholder='Informe a NCM']")
        campo_pesquisa.send_keys(ncm)
        # Pressiona Enter para iniciar a pesquisa
        campo_pesquisa.send_keys(Keys.RETURN)
        
        # Aguarda até que a resposta seja recebida
        WebDriverWait(navegador, 20).until(
            lambda d: any(requisicao.response for requisicao in d.requests if 'portal_imendes/v1/public/Consult' in requisicao.url)
        )

        for requisicao in navegador.requests:
            if requisicao.response and 'portal_imendes/v1/public/Consult' in requisicao.url:
                try:
                    dados = json.loads(requisicao.response.body.decode('utf-8'))
                    print(f"Saída do Console para {email}:")
                    print(json.dumps(dados, indent=2))
                    with open(f'output_{email}.json', 'w') as arquivo:
                        arquivo.write(json.dumps(dados, indent=2))
                    return dados
                except Exception as e:
                    print(f"Erro ao processar a requisição para {email}: {e}")
                    return None
    except Exception as e:
        print(f"Ocorreu um erro para {email}: {e}")
        return None
    finally:
        navegador.quit()

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <link rel="icon" type="image/x-icon" href="/favicon_att.ico">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.16.2/xlsx.full.min.js"></script>
        <title>CLASSIFICADOR FISCAL - NCM</title>
        <style>
            .tabela-container {
                position: relative;
                width: 95% !important;
                height: auto;
                overflow: hidden;
                padding: 20px;
                box-sizing: border-box;
                background: transparent;
                z-index: 1000;
                margin: 20px auto; /* Altera aqui para centralizar */
                display: flex;
                flex-direction: column;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                table-layout: fixed; /* Mantém as colunas com a largura definida */
            }

            .scroll-container {
                max-height: calc(100vh - 350px);
                overflow-y: auto;
                overflow-x: hidden;
                width: 100%;
                padding-bottom: 0;
                margin-top: 290px;
                border: 5px solid transparent;
                scrollbar-width: thin;
                scrollbar-color: white #232323;
            }
            
            /* Estilizar a barra de rolagem */
            .scroll-container::-webkit-scrollbar {
                width: 12px; /* Largura da barra de rolagem */
            }

            .scroll-container::-webkit-scrollbar-thumb {
                background-color: white; /* Cor do indicador de rolagem */
                border-radius: 10px; /* Bordas arredondadas do indicador */
                border: 3px solid #000000; /* Cor da borda do indicador */
            }

            .scroll-container::-webkit-scrollbar-track {
                background-color: #232323; /* Cor do fundo da barra de rolagem */
                border-radius: 10px; /* Bordas arredondadas da barra de rolagem */
            }

            table.purpleHorizon {
                border: 2px solid #0a0909;
                background-color: transparent;
                text-align: center;
                border-collapse: collapse;
                border-radius: 15px;
                overflow: hidden;
            }

            table.purpleHorizon td,
            table.purpleHorizon th {
                border: 2px solid #232323;
                padding: 5px 2px;
                color: #ffffff;
            }

            table.purpleHorizon tbody td {
                font-size: 12px;
                font-weight: bold;
                white-space: normal;
                word-wrap: break-word;
                background-color: black;
            }

            table.purpleHorizon tr:nth-child(even) {
                background: black;
            }

            table.purpleHorizon thead {
                background: linear-gradient(to bottom, #f78340 0%, #f56a1a 66%, #000000 100%);
            }

            table.purpleHorizon thead th {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                text-align: center;
                border-left: 2px solid #7f5a09;
                white-space: normal;
                word-wrap: break-word;
            }

            table.purpleHorizon thead th:first-child {
                border-left: none;
            }

            table.purpleHorizon tfoot {
                font-size: 13px;
                font-weight: bold;
                color: #ffffff;
                background: #fa8709;
                background: linear-gradient(to bottom, #fba546 0%, #fa9321 66%, #fa8709 100%);
            }

            table.purpleHorizon tfoot td {
                background: black;
            }

            body {
                display: flex;
                justify-content: center;
                align-items: flex-start;
                height: 100vh;
                margin: 0;
                text-align: center;
                background-image: url("{{ url_for('static', filename='GTIN.png') }}");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                overflow: hidden;
            }

            body::after {
                content: '';
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: -1;
                pointer-events: none;
                background-image: linear-gradient(transparent, transparent), url("../static/GTIN.png");
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
            }

            button:not(.back-button) {
                width: 180px;
                font-size: 16px;
                height: 40px;
                border: none;
                background: linear-gradient(to bottom, #f45a01, #ffa500);
                border-color: #020305;
                border-radius: 20px;
                border-bottom: 2px solid #232323;
                padding-top: 5px;
                cursor: pointer;
                margin: 5px;
                z-index: 1000;
            }

            .select-container select {
                margin-bottom: 5px !important;
            }

            #salvarButton {
                margin-top: 5px !important;
            }

            input {
                width: 200px;
                height: 30px;
                border-radius: 20px;
                border-color: #020305;
                text-align: center;
                margin: 5px;
            }

            .container {
                width: 95%;
                padding: 0;
                margin: 0;
                box-sizing: border-box;
            }

            h1 {
                margin: 0;
                padding: 20px 0;
                text-align: center;
                position: sticky;
                top: 0;
                background-color: transparent;
                z-index: 1;
            }

            .mouseHand {
                cursor: pointer;
            }

            .growing-search {
                padding: 5px 5px 5px 7px;
                border-radius: 5px;
                background: #fff;
            }

            .growing-search div {
                display: inline-block;
                font-size: 12px;
            }

            .growing-search .input input {
                margin-right: 0;
                border: none;
                font-size: inherit;
                transition: width 200ms;
                padding-top: 5px;
                padding-left: 5px;
                padding-bottom: 5px;
                width: 125px;
                color: #232323;
                border-bottom: 2px solid #232323;
            }

            .growing-search .input input:focus {
                width: 150px;
            }

            .growing-search .submit button {
                margin-left: 0;
                border: none;
                font-size: 1.15em;
                color: #aaa;
                background-color: #fff;
                padding-top: 2px;
                padding-bottom: 2px;
                transition: color 200ms;
            }

            .growing-search .input input:hover,
            .growing-search .submit button:hover {
                cursor: pointer;
            }

            .growing-search .input input:focus,
            .growing-search .submit button:focus {
                outline: none;
            }

            .growing-search .submit button:hover {
                color: #3498db;
            }

            .paginas {
                color: white;
            }

            .table-responsive {
                width: 100%;
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                border: 5px solid transparent;
            }

            #tabelaPrincipal {
                width: 95%;
                table-layout: auto;
            }

            #tabelaPrincipal th,
            #tabelaPrincipal td {
                padding: 8px;
                border: 1px solid #ddd;
                text-align: center;
                vertical-align: middle;
                word-wrap: break-word;
                overflow-wrap: break-word;
                white-space: normal;
                font-size: 14px;
            }

            .col-descricao {
                width: 25%; /* Ajuste conforme necessário */
            }

            .col-ncm {
                width: 10%; /* Ajuste conforme necessário */
            }

            .col-cest {
                width: 10%; /* Ajuste conforme necessário */
            }

            .col-cfop {
                width: 10%; /* Ajuste conforme necessário */
            }
            
            /* Opcional: definir as larguras diretamente no HTML */
            #tabelaPrincipal th.col-descricao {
                width: 25%; /* Aumenta a largura da coluna Descrição */
            }

            #tabelaPrincipal th.col-ncm {
                width: 10%; /* Define a largura da coluna NCM */
            }

            #tabelaPrincipal th.col-cest {
                width: 10%; /* Define a largura da coluna CEST */
            }

            #tabelaPrincipal th.col-cfop {
                width: 10%; /* Define a largura da coluna CFOP */
            }

            .hidden {
                display: none;
            }

            .back-button {
                position: absolute;
                top: 10px;
                left: 10px;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: white !important;
                display: flex;
                justify-content: center;
                align-items: center;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                cursor: pointer;
                font-size: 8px;
                border: none !important;
                color: black !important;
                background-image: none !important;
            }

            button.back-button {
                background-color: white !important;
                border: none !important;
                color: black !important;
            }

            .select-container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            select.form-control {
                width: 200px;
                max-width: 400px;
                height: 30px;
                padding: 5px 10px;
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                background: linear-gradient(to bottom, #f45a01, #ffa500);
                border: none;
                border-radius: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                appearance: none;
                -webkit-appearance: none;
                -moz-appearance: none;
                text-align: center;
                cursor: pointer;
            }

            select.form-control option {
                background-color: #ffffff;
                color: #000000;
                font-weight: bold;
            }

            select.form-control::-ms-expand {
                display: none;
            }

            select.form-control::after {
                content: '\25BC';
                position: absolute;
                right: 15px;
                top: 15px;
                color: #ffffff;
                font-size: 20px;
                pointer-events: none;
            }

            .pagination-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-top: 7vh;
                margin-bottom: 20px;
            }

            .pagination-list {
                display: flex;
                list-style: none;
                padding: 0;
                gap: 5px;
                flex-wrap: nowrap;
                overflow-x: auto;
            }

            .page-item {
                margin: 0 2px;
            }

            .page-item a, .page-item button {
                width: 80px;
                height: 30px;
                padding: 2px 2px;
                display: inline-flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                background: linear-gradient(to bottom, #FFA500, #F45A01);
                border: none;
                border-radius: 15px;
                color: white;
                text-decoration: none;
                font-size: 1.2em;
                font-weight: bold;
                transition: background 0.3s ease;
            }

            .page-item a:hover, .page-item button:hover {
                background: linear-gradient(to bottom, #F56A1A, #D45000);
                cursor: pointer;
            }

            .page-item.disabled a, .page-item.disabled button {
                background: grey;
                cursor: not-allowed;
            }

            .page-item.active a {
                background: #232323;
                pointer-events: none;
            }
        </style>
    </head>
    <body>
        <div class="fixed-top" id="header">
            <div class="container">
                <button class="back-button" onclick="voltar()">
                    <i class="fas fa-arrow-left fa-2x"></i>
                </button>
                <h1 style="margin-top: 5px; margin-bottom: -5px; color: white; font-family: Arial;">
                    <label for="gtinInput"><strong>CLASSIFICADOR FISCAL</strong></label>
                </h1>
                <div id="campoPesquisa" class="d-flex justify-content-center">
                    <div class="select-container" style="margin-right: 10px;">
                        <select id="atividadeSelect" class="form-control" onchange="verificarSelecoes()">
                            <option value="" disabled selected>Selecione uma opção</option>
                            <option value="GERAL">Geral</option>
                            <option value="ATACADO">Atacado</option>
                            <option value="CONSTRUCAO">Construção</option>
                            <option value="INDUSTRIA">Indústria</option>
                            <option value="FARMA">Farma</option>
                            <option value="VAREJO">Varejo</option>
                        </select>
                    </div>
                    <div class="select-container" style="margin-right: 10px;">
                        <select id="regimeSelect" class="form-control" onchange="verificarSelecoes()">
                            <option value="" disabled selected>Selecione uma opção</option>
                            <option value="Simples Nacional">Simples Nacional</option>
                            <option value="Lucro Real">Lucro Real</option>
                            <option value="Lucro Presumido">Lucro Presumido</option>
                        </select>
                    </div>
                    <div class="select-container">
                        <select id="ufSelect" class="form-control" onchange="verificarSelecoes()">
                            <option value="" disabled selected>Selecione uma opção</option>
                            <option value="AC">Acre</option>
                            <option value="AL">Alagoas</option>
                            <option value="AP">Amapá</option>
                            <option value="AM">Amazonas</option>
                            <option value="BA">Bahia</option>
                            <option value="CE">Ceará</option>
                            <option value="DF">Distrito Federal</option>
                            <option value="ES">Espírito Santo</option>
                            <option value="GO">Goiás</option>
                            <option value="MA">Maranhão</option>
                            <option value="MT">Mato Grosso</option>
                            <option value="MS">Mato Grosso do Sul</option>
                            <option value="MG">Minas Gerais</option>
                            <option value="PA">Pará</option>
                            <option value="PB">Paraíba</option>
                            <option value="PR">Paraná</option>
                            <option value="PE">Pernambuco</option>
                            <option value="PI">Piauí</option>
                            <option value="RJ">Rio de Janeiro</option>
                            <option value="RN">Rio Grande do Norte</option>
                            <option value="RS">Rio Grande do Sul</option>
                            <option value="RO">Rondônia</option>
                            <option value="RR">Roraima</option>
                            <option value="SC">Santa Catarina</option>
                            <option value="SP">São Paulo</option>
                            <option value="SE">Sergipe</option>
                            <option value="TO">Tocantins</option>
                        </select>
                    </div>
                </div>
                <div class="button-wrapper d-flex justify-content-center">
                    <button id="salvarButton" onclick="salvarInformacoes()" disabled>Salvar Informações</button>
                </div>
                <div id="inputContainer" class="hidden" style="display: none; flex-direction: column; align-items: center; margin-top: 10px;">
                    <input type="text" id="gtinInput" name="gtinInput" placeholder="Insira o NCM" style="text-align: center; margin-bottom: 5px;">
                </div>
                <div id="buttonContainer" class="hidden" style="display: none; justify-content: center; margin-top: 5px;">
                    <button type="button" id="pesquisarButton" onclick="pesquisar()" disabled>Pesquisar</button>
                </div>
            </div>
        </div>
        
        <div class="container-fluid">
            <div id="resultadoPesquisa" class="tabela-container" style="display: none; width: 90%; margin: 0 auto;">
                <div class="scroll-container">
                    <div class="table-responsive">
                        <table id="tabelaPrincipal" class="purpleHorizon" style="width: 100%;">
                            <thead>
                                <tr>
                                    <th class="col-descricao">Descrição</th>
                                    <th class="col-ncm">NCM</th>
                                    <th class="col-cest">CEST</th>
                                    <th class="col-cfop">CFOP</th>
                                    <th class="col-cst-entrada">CST Entrada</th>
                                    <th class="col-cst-saida">CST Saída</th>
                                    <th class="col-aliq-cofins">Alíquota COFINS</th>
                                    <th class="col-aliq-pis">Alíquota PIS</th>
                                    <th class="col-cst-csosn">CST/CSOSN</th>
                                    <th class="col-natrec">Natureza Receita</th>
                                    <th class="col-alq">Aliq. ICMS(%)</th>
                                    <th class="col-alq">Red. BC ICMS(%)</th>
                                    <th class="col-alq">Red. BC ICMS-ST(%)</th>
                                    <th class="col-alq">Aliq. ICMS-ST(%)</th>
                                    <th class="hidden">Aliq. ICMS Crédito</th>
                                    <th class="hidden">Antecipado</th>
                                    <th class="hidden">Cód. Benef.</th>
                                    <th class="hidden">Cód. Exceção</th>
                                    <th class="hidden">Cód. Regra</th>
                                    <th class="hidden">Desonerado</th>
                                    <th class="hidden">Exceção</th>
                                    <th class="hidden">FCP</th>
                                    <th class="hidden">Isento</th>
                                    <th class="hidden">IVA</th>
                                    <th class="hidden">Aliq. ICMS Interna</th>
                                    <th class="hidden">Aliq. ICMS PDV</th>
                                    <th class="hidden">Data Inic. Vig.</th>
                                    <th class="hidden">UF</th>
                                    <th class="hidden">Atividade</th>
                                    <th class="hidden">Regime Tributário</th>
                                    <th class="hidden">Base Legal PIS/COFINS</th>
                                    <th class="hidden">Base Legal ICMS</th>
                                </tr>
                            </thead>
                            <tbody id="corpoTabela">
                                <!-- Resultados da pesquisa serão inseridos aqui -->
                            </tbody>
                        </table>
                    </div>
                    <!-- Paginação fixada na parte inferior -->
                    <div id="paginationContainer" class="pagination-container">
                        <ul id="paginationList" class="pagination-list"></ul>
                    </div>
                </div>
            </div>
        <div class="modal fade" id="loadingModal" tabindex="-1" role="dialog" aria-labelledby="loadingModalLabel" aria-hidden="true" data-backdrop="static" data-keyboard="false">
            <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                    <div class="modal-body text-center" style="max-height: 100px; padding: 20px;">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Carregando...</span>
                        </div>
                        <p style="margin-top: 10px;">Carregando, aguarde por favor...</p>
                    </div>
                </div>
            </div>
        </div>

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

        <script>
            let currentPage = 1;
            const productsPerPage = 10;
            const maxPagesToShow = 3;
            let informacoesSalvas = false;

            function voltar() {
                window.history.back();
            }

            function verificarSelecoes() {
                const atividade = document.getElementById("atividadeSelect").value;
                const regime = document.getElementById("regimeSelect").value;
                const uf = document.getElementById("ufSelect").value;
                const botaoSalvar = document.getElementById("salvarButton");
                const botaoPesquisar = document.getElementById("pesquisarButton");

                if (atividade && regime && uf) {
                    botaoSalvar.disabled = false;
                    botaoSalvar.classList.add('enabled');
                    
                    // Se as informações foram salvas e houve uma alteração, desabilita o botão "Pesquisar" e mostra uma mensagem
                    if (informacoesSalvas) {
                        botaoPesquisar.disabled = true;
                        alert("Você alterou as informações. Por favor, salve novamente antes de continuar.");
                    }
                } else {
                    botaoSalvar.disabled = true;
                    botaoSalvar.classList.remove('enabled');
                }
            }

            function salvarInformacoes() {
                const atividade = document.getElementById("atividadeSelect").value;
                const regime = document.getElementById("regimeSelect").value;
                const uf = document.getElementById("ufSelect").value;

                axios.post('/api/salvarInformacoes', {
                    atividade: atividade,
                    regime: regime,
                    uf: uf
                })
                .then(resposta => {
                    console.log('Informações salvas:', resposta.data);
                    informacoesSalvas = true;

                    // Exibir os campos de input e botão de pesquisa
                    document.getElementById("inputContainer").style.display = "flex";
                    document.getElementById("buttonContainer").style.display = "flex";
                    document.getElementById("pesquisarButton").disabled = false;
                })
                .catch(erro => {
                    console.error('Erro ao salvar informações:', erro);
                });
            }

            function pesquisar() {
                // Esconde a tabela antes de iniciar uma nova pesquisa
                document.getElementById('resultadoPesquisa').style.display = 'none';

                const atividade = document.getElementById("atividadeSelect").value;
                const regime = document.getElementById("regimeSelect").value;
                const uf = document.getElementById("ufSelect").value;
                const valorEntrada = document.getElementById("gtinInput").value;

                console.log('Iniciando a pesquisa...');

                $('#loadingModal').modal('show'); // Exibir o modal de carregamento

                axios.post('/api/pesquisar', {
                    atividade: atividade,
                    regime: regime,
                    uf: uf,
                    input: valorEntrada
                })
                .then(resposta => {
                    console.log('Pesquisa realizada:', resposta.data);
                    $('#loadingModal').modal('hide'); // Esconder o modal de carregamento

                    processarDados(resposta.data);
                })
                .catch(erro => {
                    console.error('Erro ao realizar pesquisa:', erro);
                    $('#loadingModal').modal('hide'); // Esconder o modal de carregamento
                });
            }

            function processarDados(dados) {
                const corpoTabela = document.getElementById('corpoTabela');
                corpoTabela.innerHTML = ''; // Limpa os resultados anteriores

                if (dados.ncMs && Array.isArray(dados.ncMs)) {
                    // Aqui está a correção para garantir que todos os 22 itens sejam paginados corretamente
                    dadosPaginados = [];
                    
                    // Divida os dados em páginas
                    for (let i = 0; i < dados.ncMs.length; i += productsPerPage) {
                        dadosPaginados.push(dados.ncMs.slice(i, i + productsPerPage));
                    }

                    currentPage = 1;
                    exibirResultado(dadosPaginados[currentPage - 1]);
                    updatePagination(); // Atualiza a paginação com o número correto de páginas
                    
                    // Mostra a tabela após processar os dados
                    document.getElementById('resultadoPesquisa').style.display = 'block';
                } else {
                    console.error('Dados da pesquisa não estão no formato esperado:', dados);
                }
            }

            function exibirResultado(dadosPagina) {
                const atividadeSelecionada = document.getElementById('atividadeSelect').value;
                const regimeSelecionado = document.getElementById('regimeSelect').value;
                const ufSelecionada = document.getElementById('ufSelect').value;
                const corpoTabela = document.getElementById('corpoTabela');
                corpoTabela.innerHTML = ''; // Limpa os resultados anteriores

                dadosPagina.forEach(item => {
                    const linha = document.createElement('tr');
                    linha.innerHTML = `
                        <td>${item.federal.descricao || ''}</td>
                        <td>${item.ncmCode || ''}</td>
                        <td>${item.federal.cestCodigo || ''}</td>
                        <td>${item.state.cfop || ''}</td>
                        <td>${item.federal.cstPisCofinsEntrada || ''}</td>
                        <td>${item.federal.cstPisCofinsSaida || ''}</td>
                        <td>${item.federal.aliqCofins || ''}</td>
                        <td>${item.federal.aliqPis || ''}</td>
                        <td>${item.state.pdv.cstCsosn || ''}</td>
                        <td>${item.federal.natRecIsenta || ''}</td>
                        <td>${item.state.aliquota || ''}</td>
                        <td>${item.state.reducaoBC || ''}</td>
                        <td>${item.state.reducaoBcSt || ''}</td>
                        <td>${item.state.aliqIcmsSt || ''}</td>
                        <td class="hidden">${item.state.aliqIcmsCredito || ''}</td>
                        <td class="hidden">${item.state.estd_antecipado || ''}</td>
                        <td class="hidden">${item.state.pdv.codBenef || ''}</td>
                        <td class="hidden">${item.state.codExcecao || ''}</td>
                        <td class="hidden">${item.state.pdv.codRegra || ''}</td>
                        <td class="hidden">${item.state.desonerado || ''}</td>
                        <td class="hidden">${item.state.pdv.excecao || ''}</td>
                        <td class="hidden">${item.state.pdv.fcp || ''}</td>
                        <td class="hidden">${item.state.isento || ''}</td>
                        <td class="hidden">${item.state.pdv.iva || ''}</td>
                        <td class="hidden">${item.state.pdv.aliqIcmsInterna || ''}</td>
                        <td class="hidden">${item.state.pdv.aliqIcmsPdv || ''}</td>
                        <td class="hidden">${item.state.dtVigIni || ''}</td>
                        <td class="hidden">${ufSelecionada || ''}</td>
                        <td class="hidden">${atividadeSelecionada || ''}</td>
                        <td class="hidden">${regimeSelecionado || ''}</td>
                        <td class="hidden">${item.federal.amparoLegal || ''}</td> <!-- Amparo legal PIS/COFINS -->
                        <td class="hidden">${item.state.amparoLegal.map(al => al.description).join(', ') || ''}</td> <!-- Amparo legal ICMS -->
                    `;
                    corpoTabela.appendChild(linha);
                });
            }
            
            function updatePagination() {
                const totalPages = dadosPaginados.length;

                const paginationContainer = document.getElementById('paginationContainer');
                paginationContainer.innerHTML = '';

                if (currentPage < 1) {
                    currentPage = 1;
                } else if (currentPage > totalPages) {
                    currentPage = totalPages;
                }

                let startPage, endPage;
                if (totalPages <= maxPagesToShow) {
                    startPage = 1;
                    endPage = totalPages;
                } else {
                    if (currentPage <= Math.floor(maxPagesToShow / 2)) {
                        startPage = 1;
                        endPage = maxPagesToShow;
                    } else if (currentPage + Math.floor(maxPagesToShow / 2) >= totalPages) {
                        startPage = totalPages - maxPagesToShow + 1;
                        endPage = totalPages;
                    } else {
                        startPage = currentPage - Math.floor(maxPagesToShow / 2);
                        endPage = currentPage + Math.floor(maxPagesToShow / 2);
                    }
                }

                // Adiciona botão de página anterior
                const previousPageBtn = document.createElement('li');
                previousPageBtn.classList.add('page-item');
                if (currentPage === 1) {
                    previousPageBtn.classList.add('disabled');
                }
                previousPageBtn.innerHTML = `<a class="page-link" href="#" tabindex="-1" onclick="previousPage()">Anterior</a>`;
                paginationContainer.appendChild(previousPageBtn);

                // Adiciona botões de página
                for (let i = startPage; i <= endPage; i++) {
                    const pageItem = document.createElement('li');
                    pageItem.classList.add('page-item');
                    if (i === currentPage) {
                        pageItem.classList.add('active');
                        pageItem.innerHTML = `<a class="page-link" href="#">${i} <span class="sr-only">(atual)</span></a>`;
                    } else {
                        pageItem.innerHTML = `<a class="page-link" href="#" onclick="gotoPage(${i})">${i}</a>`;
                    }
                    paginationContainer.appendChild(pageItem);
                }

                // Adiciona botão de próxima página
                const nextPageBtn = document.createElement('li');
                nextPageBtn.classList.add('page-item');
                if (currentPage === totalPages) {
                    nextPageBtn.classList.add('disabled');
                }
                nextPageBtn.innerHTML = `<a class="page-link" href="#" onclick="nextPage()">Próximo</a>`;
                paginationContainer.appendChild(nextPageBtn);

                // Adiciona botão de "Fechar" e "Mais Info"
                const fecharLi = document.createElement('li');
                fecharLi.classList.add('page-item');
                fecharLi.innerHTML = `<button class="btn btn-primary rounded-pill" style="width: 130px;" onclick="fecharTabela()">Fechar</button>`;
                paginationContainer.appendChild(fecharLi);

                const maisInfoLi = document.createElement('li');
                maisInfoLi.classList.add('page-item');
                maisInfoLi.innerHTML = `<button class="btn btn-primary rounded-pill" style="width: 130px;" onclick="Maisinfo()">Mais Info</button>`;
                paginationContainer.appendChild(maisInfoLi);
            }

            function nextPage() {
                if (currentPage < dadosPaginados.length) {
                    currentPage++;
                    exibirResultado(dadosPaginados[currentPage - 1]);
                    updatePagination();
                }
            }

            function previousPage() {
                if (currentPage > 1) {
                    currentPage--;
                    exibirResultado(dadosPaginados[currentPage - 1]);
                    updatePagination();
                }
            }

            function gotoPage(page) {
                currentPage = page;
                exibirResultado(dadosPaginados[currentPage - 1]);
                updatePagination();
            }

            function Maisinfo() {
                exportarTodosParaExcel();  // Função que exporta os dados para Excel
            }

            function fecharTabela() {
                document.getElementById('resultadoPesquisa').style.display = 'none';
            }

            function exportarTodosParaExcel() {
                const atividadeSelecionada = document.getElementById('atividadeSelect').value;
                const regimeSelecionado = document.getElementById('regimeSelect').value;
                const ufSelecionada = document.getElementById('ufSelect').value;

                const produtos = [];
                
                dadosPaginados.forEach(dadosPagina => {
                    dadosPagina.forEach(item => {
                        const produto = {
                            'Descrição': item.federal.descricao,
                            'NCM': item.ncmCode,
                            'CEST': item.federal.cestCodigo,
                            'CFOP': item.state.cfop,
                            'CST Entrada': item.federal.cstPisCofinsEntrada,
                            'CST Saída': item.federal.cstPisCofinsSaida,
                            'Alíquota COFINS': item.federal.aliqCofins,
                            'Alíquota PIS': item.federal.aliqPis,
                            'CST/CSOSN': item.state.pdv.cstCsosn,
                            'Natureza Receita': item.federal.natRecIsenta,
                            'Aliq. ICMS(%)': item.state.aliquota,
                            'Red. BC ICMS(%)': item.state.reducaoBC,
                            'Red. BC ICMS-ST(%)': item.state.reducaoBcSt,
                            'Aliq. ICMS-ST(%)': item.state.aliqIcmsSt,
                            'Aliq. ICMS Crédito': item.state.aliqIcmsCredito,
                            'Antecipado': item.state.pdv.antecipado,
                            'Cód. Benef.': item.state.pdv.codBenef,
                            'Cód. Exceção': item.state.pdv.codExcecao,
                            'Cód. Regra': item.state.pdv.codRegra,
                            'Desonerado': item.state.pdv.desonerado,
                            'Exceção': item.state.pdv.excecao,
                            'FCP': item.state.pdv.fcp,
                            'Isento': item.state.pdv.isento,
                            'IVA': item.state.pdv.iva,
                            'Aliq. ICMS Interna': item.state.pdv.aliqIcmsInterna,
                            'Aliq. ICMS PDV': item.state.pdv.aliqIcmsPdv,
                            'Data Inic. Vig.': item.state.dtVigIni,
                            'UF': ufSelecionada,
                            'Atividade': atividadeSelecionada,
                            'Regime Tributário': regimeSelecionado,
                            'Base Legal PIS/COFINS': item.federal.amparoLegal,
                            'Base Legal ICMS': item.state.amparoLegal.map(al => al.description).join(', ') 
                        };
                        produtos.push(produto);
                    });
                });

                const livroExcel = XLSX.utils.book_new();
                const folhaExcel = XLSX.utils.json_to_sheet(produtos);

                const largurasColunas = [
                    { wch: 30 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 20 },
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 },
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 15 }, 
                    { wch: 90 }, 
                    { wch: 90 },
                ];

                folhaExcel['!cols'] = largurasColunas;

                XLSX.utils.book_append_sheet(livroExcel, folhaExcel, 'Produtos');

                XLSX.writeFile(livroExcel, 'resultado_pesquisa.xlsx');
            }
        </script>
    </body>
</html>
    ''')

@app.route('/api/salvarInformacoes', methods=['POST'])
def salvar_informacoes():
    dados = request.json
    atividade = dados.get('atividade')
    regime = dados.get('regime')
    uf = dados.get('uf')
    return jsonify({"message": "Informações salvas com sucesso!"})

@app.route('/api/pesquisar', methods=['POST'])
def pesquisar():
    dados = request.json
    atividade = dados.get('atividade')
    regime = dados.get('regime')
    uf = dados.get('uf')
    ncm = dados.get('input')
    
    if credenciais:
        email, senha = credenciais.pop(0).values()
        resultado = realizar_login_e_pesquisa(email, senha, atividade, regime, uf, ncm)
        if resultado:
            return jsonify(resultado)
        else:
            return jsonify({"message": "Falha ao recuperar os dados."}), 500
    else:
        return jsonify({"message": "Nenhuma credencial disponível."}), 400

if __name__ == '__main__':
    app.run(debug=True)
