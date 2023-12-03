from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import requests
import json
import js2py
import html
import sys


urlLogin = 'https://www.publico.pt/api/user/login'
url = "https://www.publico.pt/azul/clima"
original_stdout = sys.stdout
driver = webdriver.Chrome()
pagina = input("Indique a página do resultado da pesquisa: ")

def efetuarLogin():
    driver.get(url)
    div_element = driver.find_element(By.ID, 'banner-and-header')
    div_text = div_element.text
    acceptCookies = driver.find_element(By.XPATH, "//div[@id='qc-cmp2-ui']/div[2]/div/button[2]/span")
    acceptCookies.click()
    login = driver.find_element(By.XPATH, "//header[@id='masthead']/div[2]/div/div/div[2]/ul/li[2]/button/span")
    login.click()
    time.sleep(2)
    campoEmail = driver.find_element(By.ID, "login-email-input")
    campoEmail.send_keys('gisiela@gmail.com')
    botaoContinuar = driver.find_element(By.XPATH, "//input[@value='Continuar']")
    botaoContinuar.click()
    time.sleep(10)
    campoPassword = driver.find_element(By.ID, "login-password-input")
    campoPassword.send_keys('Gis@2022')
    time.sleep(2)
    continuar2 = driver.find_element(By.XPATH, "//form[@id='login-form-password']/div/div[4]/input")
    continuar2.click()

def pesquisar():
    
    brutos = 'dadosBrutos.json'
    filtrados = 'filtrados.json'
    getUrl = 'https://www.publico.pt/api/search?page='+pagina+'&size=18&tags=azul&tags=clima&sec=azul&_=1701374775790'
    response = requests.get(getUrl)
    data = response.json()

    json_data = json.dumps(data)
    
    with open(brutos, 'w') as file:
        file.write(json_data)  
    
    with open(brutos, 'r') as file:
        data = json.load(file)
    
    listaFinal = [{"fullUrl": item["fullUrl"]} for item in data]

    indexed_data = [{"index": index, "fullUrl": item} for index, item in enumerate(listaFinal)]

    with open(filtrados, 'w') as file:
        json.dump(indexed_data, file, indent=2)

    ind = -1
    for item in indexed_data:
        url = indexed_data[ind+1]['fullUrl']['fullUrl']
        ind = ind + 1
        sys.stdout = original_stdout
        print(url + str(ind))
        
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            titles = soup.findAll('h1', attrs={'class':'headline story__headline'})
            for title in titles:
                #with open('output.txt', 'w', encoding='utf-8') as file:
                    #sys.stdout = file
                    titulos = title.get_text()+'\n'
                
            dates = soup.findAll('time', attrs={'class': 'dateline'})
            for date in dates:
                #with open('output.txt', 'a', encoding='utf-8') as file:
                    #sys.stdout = file
                    datas = (date.get_text())

            texts = soup.findAll('div', attrs={'class': 'story__body'})
            for text in texts:
                #with open('output.txt', 'a', encoding='utf-8') as file:
                    #sys.stdout = file
                    textos = (text.get_text())

            completo = str(titulos) + str(datas) + str(textos)
            print(completo)

            # with open('teste.txt', 'w', encoding='utf-8') as file:
            #     sys.stdout = file
            #     print(completo)
            
                #file.write(completo)


        else:
            print(f'Error: {response.status_code}')
            
      
    #Write the new JSON to a file


    


#efetuarLogin()
pesquisar()
#input("continue?")




