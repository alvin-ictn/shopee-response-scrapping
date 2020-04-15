# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv
import pandas as pd

driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get('https://shopee.co.id/search?facet=14783%2C157&keyword=shake&labelIds=1000006&maxPrice=247000&minPrice=230000&noCorrection=true&page=0')
timeout = 20

toko = []
            
            
def ProcessToko():
    global numberpage
    global toko
    global nama_toko
    nama_toko = None
    while nama_toko is None:
        try:
            nama_toko = driver.find_element_by_css_selector(".btn-light--link").get_attribute("href").replace('https://shopee.co.id/','');
        except:
            pass
    if nama_toko in toko:
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    else:
        toko.append(nama_toko)
        print("step 2")
        click_toko_profile = None
        while click_toko_profile is None:
            try:
                #ini toko profile
                click_toko_profile = driver.find_element_by_css_selector(".btn-light--link")
            except:
                pass
        print("step 3")    
        click_toko_profile.click()
        
        click_rating = None
        while click_rating is None:
            try:
                #click rating
                click_rating = driver.find_element_by_xpath('//div[text()="penilaian"]')
            except:
                pass
        print("step 4")    
        click_rating.click()
        
        for ratingto in range(1):
            param1 = ""
            print("IM NUMBAH STAR",ratingto)
            #filter rating 1 ~ 3
            click_rating_star = None
            while click_rating_star is None:
                try:
                    click_rating_star = driver.find_element_by_xpath('//div[starts-with(.,"%s bintang")]'% str(ratingto+1))
                except:
                    pass
            print(click_rating_star.text)
            print("step 5")
            click_rating_star.click()
            
            #for getting all button from < 1 2 3  . . . >
            #driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button')
            #max_button = len(driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button'))
            #sibling = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button[%s]' % (max_button-1))
            #param1 = sibling.get_attribute('class')
            #param1.find("solid")
            
            while "solid" not in param1:
                numberpage = ratingto
                InputData()
                max_button = None
                while max_button is None:
                    try:
                        max_button = len(driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button'))
                    except:
                        pass
                if max_button == 0:
                    param1="solid"
                else:
                    sibling = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button[%s]' % (max_button-1))
                    param1 = sibling.get_attribute('class')
                    
                    driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div/div[2]/section[1]/div/div[2]/div[2]/button[%s]' % (max_button)).click()
            
        print("ITS DONE")
        
        '''
            getLast = None
            while getLast is None:
                try:
                    if(driver.find_elements_by_css_selector(".shopee-button-no-outline.shopee-button-no-outline--non-click")):
                        panjang = len(driver.find_elements_by_css_selector(".shopee-button-no-outline"))
                        driver.find_element_by_xpath('//button[text()="%s"]'% panjang).click()
    
                        panjang = len(driver.find_elements_by_css_selector(".shopee-button-no-outline"))
                    else:
                        getLast = 
                except:
                    pass
            '''
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
#get max page

def InputData():
    global trigger1
    global numberpage
    global nama_toko
    data_feedback = None
    i = 0
    trigger2= None
    while i<5:
        try:
            trigger2 = driver.find_element_by_class_name("shopee-product-rating__like-count").text
            i=i+1
        except:
            i+=1
            sleep(0.5)
        
    print(trigger2)
    
    while data_feedback is None:
        try:
            data_feedback = driver.find_elements_by_class_name("shopee-product-rating")
        except:
            pass
    print(data_feedback)
    with open('new_data.csv','a',encoding="UTF-8",newline='') as f:
        header_data = ['nama_toko','rating','name','feedback','feedback_awto','user_image','produk','product link','tanggal_komen']
        writer = csv.DictWriter(f, fieldnames=header_data)
        try:
            if not(trigger1):
                print("put header")
                writer.writeheader()
                trigger1 = 1
            else:
                print("dont need header anymore")    
        except:
            print("put header")
            trigger1 = 1
            writer.writeheader()
           
        for x in data_feedback:
            #getting user image
            try:
                user_image = x.find_element_by_class_name("image-list-inline-zoom__zoomed-image-item").get_attribute('src').replace('\n','|').replace(',','...')
            except:
                print('user image not found will replace by empty field')
                user_image = ''
            #getting produk name and link
        
            try:
                nama_produk = x.find_elements_by_tag_name('a')[2].text.replace('\n','|').replace(',','...')
            except:
                nama_produk = ''
            #---------------------------------------------------------------
     
            try:
                link_produk = x.find_elements_by_tag_name('a')[2].get_attribute('href').replace('\n','|').replace(',','...')
            except:
                link_produk = ''
   
            try:
                awto_feedback = x.find_element_by_class_name('shopee-product-rating__tags').text.replace('\n','|').replace(',','...')
            except:
                awto_feedback = ''
            print(awto_feedback)

            try:
                feedback = x.find_element_by_class_name('shopee-product-rating__content').text.replace('\n','|').replace(',','...')
            except:
                feedback = ''
            
            try:
                nama_responder = x.find_element_by_class_name('shopee-product-rating__author-name').text.replace('\n','|').replace(',','...')
            except:
                nama_responder = ''
            
            try:
                rating = numberpage+1
            except:
                rating = ''
            try:
                TangKom = x.find_element_by_class_name('shopee-product-rating__time').text.replace('\n','|').replace(',','...')
            except:
                TangKom = ''
            #header_data = ['rating','name','feedback','feedback_awto','user_image','produk','product link']    
            writer.writerow({header_data[0]:nama_toko,header_data[1]:rating,header_data[2]:nama_responder,header_data[3]:feedback,header_data[4]:awto_feedback,header_data[5]:user_image,header_data[6]:nama_produk,header_data[7]:link_produk,header_data[8]:TangKom})

          
get_page = None
while get_page is None:
    try:    
        get_page = driver.find_elements_by_class_name("shopee-mini-page-controller__total")[0].text
    except:
        pass
            
for i in range(int(get_page)):
    get_current = None
    while get_current is None:
        try:
            get_current = driver.find_elements_by_class_name("shopee-mini-page-controller__current")[0].text
        except:
            pass
    count = 0
    while count<5:
        try:
            trigger99 = driver.find_element_by_class_name("shopee-sort-bar").text
            count+=1
        except:
            count+=1
            sleep(0.5)
            
    elements = None
    while elements is None:
        try:
            elements = driver.find_elements_by_css_selector(".shopee-search-item-result__item")
        except:
            print("error when getting contents")
    print(elements)
    for y in elements:
        ActionChains(driver).key_down(Keys.CONTROL).click(y).key_up(Keys.CONTROL).perform()
        #time.sleep(1)
        driver.switch_to_window(driver.window_handles[1])
        print("step 1")
        ProcessToko()
    #driver.find_element_by_css_selector('.shopee-button-outline.shopee-mini-page-controller__next-btn.shopee-button-outline--disabled').get_attribute('class')
    #test = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/button[2]')
    Page_Butt = None
    while Page_Butt is None:
        try:
            Page_Butt = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/button[2]')
        except:
            pass
    Page_Butt.click()
    