# -*- coding: utf-8 -*-
"""bb_amz_spen.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hVesKgZFrZzabEZbnjhj4uV38yGB2BOg
"""

#!apt-get update > /dev/null # --fix-missing
#!apt install chromium-chromedriver > /dev/null
# !cp /usr/lib/chromium-browser/chromedriver /usr/bin > /dev/null
#!pip install selenium > /dev/null

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import shutil
import time
import os
import json
import re
import datetime
def waitForElementToPopUp(driver, xpath,timeout=10):
    try:
        element_present = EC.presence_of_element_located((By.XPATH,xpath ))
        WebDriverWait(driver, timeout).until(element_present)
        return driver.find_element(By.XPATH,xpath)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None
def waitForElementToPopUpbyID(driver, ID,timeout=10):
    try:
        element_present = EC.presence_of_element_located((By.ID,ID ))
        WebDriverWait(driver, timeout).until(element_present)
        return driver.find_element(By.ID,ID)
    except TimeoutException:
        print("Timed out waiting for page to load")
        return None


def start_driver_1(headless=True):
    if not headless:
        return webdriver.Firefox()
    firefox_options = webdriver.firefox.options.Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--no-sandbox')
    return webdriver.Firefox(options=firefox_options)
def start_driver(headless=True):
    if not headless:
        return webdriver.Chrome(executable_path='/home/dev04/Downloads/chromedriver')
    firefox_options = webdriver.chrome.options.Options()
    firefox_options.add_argument('--headless')
    firefox_options.add_argument('--no-sandbox')
    firefox_options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=firefox_options)


def dump_json(raw_data_file, out_data_file):
    with open(raw_data_file) as f:
        data = f.read().strip().split("\n")
    js_data = list(map(lambda x: json.loads(x), data))

    with open(out_data_file, "w") as f:
        json.dump(js_data, f, indent=2)
def remove_dot(s):
    if s[0] == '.':
        return s[1:]
    else:
        return s
def remove_dot_if_not_empty(s):
    if s != '':
        return remove_dot(s)
    else:
        return s
def getQuantityList(txt):
  x = re.findall("(?i)[0-9.]|grams|g|kg|pcs|pc| U |%", txt)
  #print(x)
  str_concat= ""
  w_list=[]
  q_list=[]
  for i in x:
    str_concat= str_concat+i
    #print("before string",str_concat)
    i=i.lower()
    if (i=='kg'or i=='g'or i=='grams' or i == 'gm' or i =='-' or i =='%') :
        w_list.append(str_concat)
        if w_list[-1].isalpha() or w_list[-1]=='-'or ('%' in w_list[-1] ):
            w_list.pop()
        str_concat=''
        
    if (i=='pcs' or i=='pc' or i ==' u '):
      
      q_list.append(str_concat)
     
      if q_list[-1].isalpha():
            #print("the element is popped")
            q_list.pop()
      str_concat=''

  print("this is the w_list and q_list",w_list,q_list)    
  Pcs=remove_dot_if_not_empty(('-'.join(w_list)))
  Kgs=remove_dot_if_not_empty(('-'.join(q_list)))
  #print(w_list, q_list)
  return Pcs,Kgs
import requests
import json
def token_auth():  
  data = {'UserName':'urbankisaanmandi',
  'Password': 'ukv3@2021@',
  'grant_type':'password',}
  url = 'https://services.urbankisaan.com/mandiapi/api/token'
  headers = {'Content-type': 'application/x-www-form-urlencoded'}
  r = requests.post(url, data=data, headers=headers)
  data1 = json.loads((r.content.decode()).replace("\\",""))
  return data1['token_type']+" "+data1['access_token']
def getProductData(product_id):
    json_data = "{\"productId\":"+str(product_id)+" ,\"StateName\": \"TELANGANA\",\"City\": \"TELANGANA\"}"
    body = json.dumps({"Condition":"Getdata_ByPrid",
    "Jsonstring":json_data})
    url = 'https://mandiapi.urbankisaan.com/api/Products/GetProductsdata'
    headers = {'Content-type':'application/json','Authorization': token_auth() }
    r = requests.post(url, data=body, headers=headers)
    product_data = (r.content.decode())
    return json.loads(product_data)
def addUrbanKissanData(original_dict,productID):
    uk_diction = json.loads(getProductData(productID)['ds']['Table'][0]['Products'])['Products'][0]
    for k,v in uk_diction.items():
        original_dict[k] = str(v)
    return original_dict
def get_Amazon_product_data(prim_list):
    driver = start_driver_1(False)
    pincodes={'Hyderabad':'500001','Vizag':'530026','Bangalore':'560008','Pune':'411006','Mumbai':'400004','Chennai':'600003'}
    for pin in pincodes:
        try : 
            driver.get('https://www.amazon.in/')
            time.sleep(3)
            #ele=waitForElementToPopUpbyID(driver,'glow-ingress-line2')
            #ele.click()
            
            ele=driver.find_element(by=By.ID,value='glow-ingress-line2')
            if ele.is_enabled()==True:
                print("The click element is ",ele.is_enabled())
                ele.click()
                pass
            else:
                print("Refreshing the page")
                driver.refresh()
                time.sleep(3)
                ele.click()
            time.sleep(3)
            #ele=waitForElementToPopUpbyID(driver,'GLUXZipUpdateInput')
            #ele.click()
            driver.find_element(by=By.ID,value='GLUXZipUpdateInput').clear()
            time.sleep(2)
##            ele=waitForElementToPopUpbyID(driver,'GLUXZipUpdateInput')
##            ele.send_keys(pincodes[pin])
            driver.find_element(by=By.ID,value='GLUXZipUpdateInput').send_keys(pincodes[pin])
            time.sleep(2)
##            ele=waitForElementToPopUp(driver,'//*[@id="GLUXZipUpdate"]/span')
##            ele.click()
            driver.find_element(by=By.XPATH,value ='//*[@id="GLUXZipUpdate"]/span').click()
            time.sleep(3)
                 
            for attr in prim_list:
              driver.get(attr['Primary Link'])
              print("Starting Download from: {}".format(attr['Primary Link']))
              html = driver.execute_script("return document.documentElement.outerHTML")
              product = bs(html, 'html.parser')
              time.sleep(delay)
                
              try:  
                storeDict={}
                time.sleep(2)
                storeDict['Product'] =(product.find("h1", {"id": "title"}).text).strip()
                # prod_dict[Quantity] = product.find("span", {"data-bind": "label"}).text
                try:
                    price=driver.find_element_by_xpath('//*[@id="corePrice_feature_div"]/div/span[1]/span[2]').text
                except:
                    try:
                        price=driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]/span').text
                    except:
                        price="Not Available"
                try:
                    discount_price=driver.find_element_by_xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr[1]/td[2]').text
                except:
                    try:
                        discount_price=driver.find_element_by_xpath('//*[@id="corePriceDisplay_desktop_feature_div"]/div[2]/span/span[1]/span/span[2]').text
                    except:
                        discount_price="NotAvailable"
                    
                storeDict['Price']=discount_price.strip('\u20b9').split(' ')[0] 
                storeDict['Discount_Price']=price.strip('\u20b9').split('\n')[0]
                try:    
                    check = product.find('span',{'class','a-color-success'}).text
                    print(check)
                    storeDict['InStock']='In Stock'
        ##        print(check)
        ##        if not(str(check.find('In stock'))=='-1'):
        ##          storeDict['InStock']='In Stock'
        ##        else:
                except:    
                  storeDict['InStock']='Not IN Stock'
                weight_id = ['kg','g']
                quantity_id=['pc','pcs']
                w_list = []
                q_list = []  
                Abcd_list=getQuantityList(storeDict['Product'])
                storeDict['Weight']=Abcd_list[0]
                storeDict['Quantity']=Abcd_list[1]
                storeDict['DateTime']=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                    
                # storedata=product.find('div',{'class':'col-sm-12 col-xs-5 prod-view ng-scope'}).find('a').get('href')
                storedata = driver.current_url
                storeDict['source_link_Type'] = attr['SourceType']
                storeDict['UK_PID'] = attr['UKId']
                storeDict['Web_url']=storedata
                storeDict['Source']='Amazon'
                storeDict['City']=pin
                storeDict['Imgurl']=''
                y=re.search(r"dp+/+\w{10}",storedata)
                data=y.group().strip('dp')
                # data = data.strip('/')
                storeDict ['ID']= data
                #############Adding Urban Kisaan Data here #####################
                try:
                    addUrbanKissanData(storeDict,attr['UKId'])
                    storeDict['UK_Qty']=str(storeDict['productQty'])+str(storeDict['Qtyuom'])
                except Exception as e:
                    print('Didnt recieve any product info : ',e)
                with open(raw_data_file_new, "a") as f:
                  data = json.dumps(storeDict)
                  f.write(data + "\n") 
              except Exception as e:
                  print("Skipped the link",attr,e)
        except Exception as e:
            print("Skipping location , onto the next city!")
            #driver.quit()
            #return storeDict
        driver.delete_all_cookies()    
def get_Bigbasket_product_data(bb_list):
    driver = start_driver_1(False)
    # global Given_data
    print("driver started")
    #city_list=[ 'Pune','Bangalore','Chennai','Guntur-Rural', 'Hyderabad', 'Kadapa', 'Khammam', 'Kurnool', 'Nellore', 'Rajamahendravaram', 'Sangareddy', 'Tirupati', 'Vijayawada-Guntur', 'Visakhapatnam']
    #city_list=['Mumbai']
    city_list=[ 'Bangalore','Chennai', 'Hyderabad','Visakhapatnam']
    for city in city_list:
        setCityLocation(driver,city)
        time.sleep(5)
        if(not execFunctionUntilboolean(checkLocationBool,setCityLocation,city,driver)):
            continue
        for attr in bb_list:
            
            driver.get(attr['Primary Link'])
            print("Starting Download from: {}".format(attr['Primary Link']))
            html = driver.execute_script("return document.documentElement.outerHTML")
            product = bs(html, 'html.parser')
            time.sleep(delay)
            # try:
            storeDict={}
            storeDict['Product'] =product.find("h1", {"class": "GrE04"}).text
            # prod_dict[Quantity] = product.find("span", {"data-bind": "label"}).text
            quantity_str = storeDict['Product'].split(',')[-1]
            weight_id = ['kg','g']
            quantity_id=['pc','pcs']
            w_list = []
            q_list = []

            Abcd_list=getQuantityList(quantity_str)
                
            storeDict['Weight']=Abcd_list[0]
            storeDict['Quantity']=Abcd_list[1]
            storeDict['DateTime']=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            storeDict['Discount_Price'] = product.find('td',{'class':'IyLvo'}).text
            try:
                storeDict['Price'] = product.find('td',{'class':'_2ifWF'}).text
            except:
                storeDict['Price'] = product.find('td',{'class':'IyLvo'}).text
            storeDict['Web_url']=driver.current_url
            storeDict['ID']=storeDict['Web_url'].split('/')[4]
            try:
                storeDict['InStock']=product.find('div',{'class':'Cs6YO rippleEffect'}).text
            except:
                try:
                    storeDict['InStock']=product.find('div',{'class':'mNjsf'}).text
                except:
                    storeDict['InStock']="NA"
                    print("Error : no valid class for InStock")
            
            #storeDict['Web_url'] = driver.current_url
            storeDict['source_link_Type'] = attr['SourceType']
            storeDict['UK_PID'] = attr['UKId']
            storeDict['City'] = city
            # storeDict['Web_url']="https://www.bigbasket.com/"+storedata
            storeDict['Source']='Big basket'
            y=re.search(r"/\d+",storeDict['Web_url'])
            data=y.group()
            storeDict['ID']=data[1:]
            #############Adding Urban Kisaan Data here #####################
            try:
                addUrbanKissanData(storeDict,attr['UKId'])
                storeDict['UK_Qty']=str(storeDict['productQty'])+str(storeDict['Qtyuom'])
            except Exception as e:
                print('Didnt recieve any product info : ',e)
            with open(raw_data_file_new, "a") as f:
                data = json.dumps(storeDict)
                f.write(data + "\n")
            # except:
            #     print("Link Error")
            #return storeDict
    driver.quit()
def get_Spencers_product_data(spen_list):
  driver = start_driver(False)
  #print("Chrome driver is working")
  #driver = webdriver.Chrome('/usr/bin/chromedriver')
  pincode=['500001','530026']
  for id in pincode:
          driver.delete_all_cookies()
          driver.get("https://www.spencers.in/")
          time.sleep(3)
          # driver.find_element_by_class_name('social-login').click()
          driver.find_element(by=By.CLASS_NAME, value='social-login').click()
          # driver.find_element_by_id('locate-address').clear()
          driver.find_element(by=By.ID, value='locate-address').clear()
          driver.find_element(by=By.ID, value='locate-address').send_keys(id)
          # driver.find_element_by_id('locate-address').send_keys(pin)
          time.sleep(2)
          # driver.find_element_by_id('ui-id').click()
          driver.find_element(by=By.ID, value='ui-id').click()
          time.sleep(2)
          # driver.find_element_by_link_text("Select Delivery Store").click()
          driver.find_element(by=By.LINK_TEXT, value='Select Delivery Store').click()
          time.sleep(2)
          # driver.find_element_by_xpath('//*[@id="social-form-locate"]/ul/li/label').click()
          driver.find_element(by=By.XPATH, value='//*[@id="social-form-locate"]/ul/li/label').click()
          # driver.find_element_by_link_text("Select Delivery Location").click()
          driver.find_element(by=By.LINK_TEXT, value='Select Delivery Location').click()
          time.sleep(3)
          for attr in spen_list:
              driver.get(attr['Secondary Link'])
              print("Starting Download from: {}".format(attr['Secondary Link']))
              html = driver.execute_script("return document.documentElement.outerHTML")
              product = bs(html, 'html.parser')
              time.sleep(delay)
              storeDict={}
              print(product.find('span',{'id':'current_store'}).text)
              try:
                storeDict['Product'] =product.find("span", {"class":'base'}).text
                print(storeDict['Product'])
                product_sub = product.find("div", {"class": "product-info-price"})
                discount_price = product_sub.find("span", {"data-price-type": "finalPrice"}).text
                storeDict['Discount_Price']=discount_price.strip('\u20b9')
                try:
                    Price = product_sub.find("span", {"data-price-type": "oldPrice"}).text
                    storeDict['Price']=Price.strip('\u20b9')
                except :
                    storeDict['Price'] = 'NO Discount'
                    storeDict['InStock']="InStock"
                weight_id = ['kg','g']
                quantity_id=['pc','pcs']
                w_list = []
                q_list = []

                Abcd_list=getQuantityList(storeDict['Product'])
                    
                storeDict['Weight']=Abcd_list[0]
                storeDict['Quantity']=Abcd_list[1]    
                storeDict['Web_url'] = driver.current_url
                storeDict['ID']= 'NO ID'
                storeDict['source_link_Type'] =  attr['SourceType']
                storeDict['Source']= 'Spencers'
                storeDict['UK_PID']= attr['UKId']
                storeDict['DateTime']=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                if id=='500001':
                    storeDict['City']='Hyderabad'
                else:
                    storeDict['City']='Vizag'
                storeDict['Imgurl']= ""
                
                #############Adding Urban Kisaan Data here #####################
                try:
                    addUrbanKissanData(storeDict,attr['UKId'])
                    storeDict['UK_Qty']=str(storeDict['productQty'])+str(storeDict['Qtyuom'])
                except Exception as e:
                    print('Didnt recieve any product info : ',e)
                with open(raw_data_file_new, "a") as f:
                            data = json.dumps(storeDict)
                            f.write(data + "\n") 
              except :
                pass
              
          
   #driver.quit()                     
  #return storeDict
def getPrice(prodcutSObj):
    # storeObj(prodcutSObj,'prodSoup.obj')
    price_info = prodcutSObj.find('tbody',{'class':'flex items-center justify-start mb-1 text-base font-bold text-darkOnyx-800'}).tr.text
    price = re.findall("\d+.\,*\d+",price_info)[0]
    price=price.strip('\u20b9')
    print(price)
    return price
def get_Bigbasket_Mumbai_product_data(bb_list):
    driver = start_driver(False)
    delay = 8
    # global Given_data
    print("driver started")
    # city_list=[ 'Pune','Bangalore','Chennai','Guntur-Rural', 'Hyderabad', 'Kadapa', 'Khammam', 'Kurnool', 'Nellore', 'Rajamahendravaram', 'Sangareddy', 'Tirupati', 'Vijayawada-Guntur', 'Visakhapatnam']
    city_list=[ 'Pune','Mumbai']
    #city_list=['Mumbai']
    for city in city_list:
        print("Now scraping for city : ",city)
        base_url='https://www.bigbasket.com/'
        driver.get(base_url)
        # html = driver.execute_script("return document.documentElement.outerHTML")
        time.sleep(3)
        try:
            driver.find_element_by_class_name('arrow-marker').click()
        except:
            continue
##            time.sleep(3)
##            driver.refresh()
##            time.sleep(3)
##            driver.find_element_by_class_name('arrow-marker').click()
        driver.find_element_by_class_name('ui-select-toggle').click()
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[1]/div/input[1]').send_keys(city)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="ui-select-choices-row-1-0"]').click()
        driver.find_element_by_name('skipandexplore').click()
        print("Location set")
        for attr in bb_list:
            driver.get(attr['Primary Link'])
            print("Starting Download from: {}".format(attr['Primary Link']))
            html = driver.execute_script("return document.documentElement.outerHTML")
            product = bs(html, 'html.parser')
            time.sleep(delay)
            storeDict={}
            time.sleep(3)
            # try :
            storeDict['Product'] =product.find("h1", {"class": "Description___StyledH-sc-82a36a-6 mlluv"}).text
            # prod_dict["Quantity"] = product.find("span", {"data-bind": "label"}).text
            try:
                storeDict['Discount_Price'] = getPrice(product)
            except Exception as e:
                print("Price not captured since product is currently unavailable")
            quantity_str = storeDict['Product'].split(',')[-1]
            weight_id = ['kg','g']
            quantity_id=['pc','pcs']
            w_list = []
            q_list = []
            Abcd_list=getQuantityList(quantity_str)
            storeDict['Weight']=Abcd_list[0]
            storeDict['Quantity']=Abcd_list[1]
            storeDict['DateTime']=datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # storeDict['Discount_Price'] = product.find('tbody',{'class':'flex items-center justify-start mb-1 text-base font-bold text-darkOnyx-800'}).text
            try:
                storeDict['Price'] = product.find('span',{'class':'line-through'}).text.strip('\u20b9')
            except:
                #storeDict['Price'] = product.find('td',{'class':'IyLvo'}).text
                print("No discount available")
            storeDict['Web_url']=driver.current_url
            storeDict['ID']=storeDict['Web_url'].split('/')[4]
            try:
                check = product.find('button',{'class','Button-sc-1dr2sn8-0 CTA___StyledButton2-yj3ixq-8 bLAlRq kkFvCv'}).text
                print(check)
                print('In Stock')
                ##        print(check)
                ##        if not(str(check.find('In stock'))=='-1'):
                ##          storeDict['InStock']='In Stock'
                ##        else:
            except:
                print('Not IN Stock')
            #storeDict['Web_url'] = driver.current_url
            storeDict['source_link_Type'] = attr['SourceType']
            storeDict['UK_PID'] = attr['UKId']
            storeDict['City'] = city
            # storeDict['Web_url']="https://www.bigbasket.com/"+storedata
            storeDict['Source']='Big basket'
            y=re.search(r"/\d+",storeDict['Web_url'])
            data=y.group()
            storeDict['ID']=data[1:]
            #############Adding Urban Kisaan Data here #####################
            try:
                addUrbanKissanData(storeDict,attr['UKId'])
                storeDict['UK_Qty']=str(storeDict['productQty'])+str(storeDict['Qtyuom'])
            except Exception as e:
                print('Didnt recieve any product info : ',e)
        # except Exception as e:
            #     print("Link Exception : ",e)
            with open(raw_data_file_new, "a") as f:
                data = json.dumps(storeDict)
                f.write(data + "\n")
            #return storeDict
    driver.quit()
def checkLocationBool(city,driver):
    html = driver.execute_script("return document.documentElement.outerHTML")
    product = bs(html, 'html.parser')
    webPageCurrentLocation = product.find("span", {"class": "hvc"}).text
    print("Current location : ",webPageCurrentLocation)
    print(city)
    print(city in webPageCurrentLocation)
    return (city in webPageCurrentLocation)
def execFunctionUntilboolean(boolFunc,retryFunc,city,driver,retry_thresh=3):
    trial = 0
    while(trial<retry_thresh):
        if(boolFunc(city,driver)):
            return True
        else:
            retryFunc(driver,city)
            trial = trial +1
            print("Trial failed. Trying again",trial)
    return False
def setCityLocation(driver,city):
    print("Now scraping for city : ",city)
    base_url='https://www.bigbasket.com/'
    driver.get(base_url)
    time.sleep(3)
    try:
        driver.find_element_by_class_name('arrow-marker').click()
    except:
        return False
    driver.find_element_by_class_name('ui-select-toggle').click()
    driver.find_element_by_xpath('//*[@id="headerControllerId"]/header/div/div/div/div/ul/li[2]/div/div/div[2]/form/div[1]/div/input[1]').send_keys(city)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="ui-select-choices-row-1-0"]').click()
    driver.find_element_by_name('skipandexplore').click()
if __name__ == "__main__":
    #driver = start_driver()
    delay = 5
    DEBUG = True
    All_Data = []
    OUTPUT_DIR = "Output"
    #pincods = ['530026','500001']
    #my_data_check = ['Primary','Secondary','Tertiary']
    out_data_file = os.path.join(OUTPUT_DIR, "data.json")
    raw_data_file_new=os.path.join(OUTPUT_DIR, "raw_file_new.txt")
    #data = [['Primary Link Source','Primary Link'],['Secondary Link Source', 'Secondary Link'],['Tertiary Source', 'Tertiary Link']]
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    raw_data_file = os.path.join(OUTPUT_DIR, "raw_data.txt")
    with open(raw_data_file_new, "w") as f:
        pass
    bb_list=[]
    amz_list=[]
    spen_list=[]
    df = pd.read_excel('Mandi Price Match Links.xlsx')
    for i,attr in df.iterrows():
      #print(attr)
      if  attr['Primary Link Source']=='Big Basket':
            bb_list.append({'Primary Link':attr['Primary Link'],'UKId':attr['UK Product Id'],'SourceType':"Primary"})
            # BigBasket_Data = get_Bigbasket_product_data(bb_list)
            # All_Data.append(BigBasket_Data)
      elif  attr['Primary Link Source']=='Amazon':
             
            amz_list.append({'Primary Link':attr['Primary Link'],'UKId':attr['UK Product Id'],'SourceType':"Primary"})

            #  Amazon_Data = get_Amazon_product_data(primary_list)             
            #  All_Data.append(Amazon_Data)
      elif   attr['Primary Link Source']=='Spencers':    
            spen_list.append({'Secondary Link':attr['Secondary Link'],'UKId':attr['UK Product Id'],'SourceType':"Primary"})
      
      if attr['Secondary Link Source']=='Spencers':
          spen_list.append({'Secondary Link':attr['Secondary Link'],'UKId':attr['UK Product Id'],'SourceType':"Secondary"})
          # Spencers_DATA = get_Spencers_product_data(spen_list)
      elif attr['Secondary Link Source']=='Amazon':
          amz_list.append({'Secondary Link':attr['Secondary Link'],'UKId':attr['UK Product Id'],'SourceType':"Secondary"})
      elif attr['Secondary Link Source']=='Big Basket':
          bb_list.append({'Secondary Link':attr['Secondary Link'],'UKId':attr['UK Product Id'],'SourceType':"Secondary"})    
          # All_Data.append(storeDict)                          
      
      if attr['Tertiary Source']=='Spencers':
          spen_list.append({'Secondary Link':attr['Teritiary Link'],'UKId':attr['UK Product Id'],'SourceType':"Teritiary"})
      else:
        pass
    print(spen_list)    
    bbmData = get_Bigbasket_Mumbai_product_data(bb_list) 
    BigBasket_Data = get_Bigbasket_product_data(bb_list)
    Spencers_DATA = get_Spencers_product_data(spen_list)
    Amazon_Data = get_Amazon_product_data(amz_list)
    
    #BigBasket_Data = get_Bigbasket_product_data(bb_list)
    dump_json(raw_data_file_new, out_data_file)
    print("JSON file saved as {}".format(raw_data_file_new))
    print("Download finished from all the links.")
    #dump_json(raw_data_file, out_data_file)
   # print("JSON file saved as {}".format(raw_data_file))
    
