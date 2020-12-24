from string_tools import format_text, date_format
import scrapy
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from scrapy import Selector
import re
from classes import Race, Person
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Database.postgre_DB_manager import insert_person, insert_race, get_race_id
from name_scrape import scrape_routine



def table_filled(driver):                                                                                               # check is the result's table is empty or not
    filled = False
    try:
        test_time1 = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr[1]/td[3]').text
        if test_time1 != '':
            filled = True
    except NoSuchElementException:
        try:
            test_time2 = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr[1]/td[3]').text
        finally:
            if test_time2 != '':
                filled = True
            else:
                filled = False
    finally:
        if filled:
            print("\ntable is filled\n")
        else:
            print("\ntable is empty\n")
        return filled

driver_path = 'C:/Users/paolo/chrome_driver/chromedriver.exe'                                                           # driver for selenium
driver = webdriver.Chrome(executable_path=driver_path)
url = 'http://www.kikourou.net/resultats/'                                                                              # starting url
driver.get(url)
lis=driver.find_elements_by_tag_name("li")                                                                              # we found how many records to scrape we have in the page
if lis > 101:
    lis = 101
print("found "+str(len(lis))+" different races")

for i in range(17, len(lis)):                                                                                           # we loop the main routine on every race we found
    print("stiamo analizzando la corsa #", i-1)                                                                         # in the page we got maximum 100 races
    if i != 1:
        driver.get(url)                                                                                                 # fro the 1st one we don't need it
    results_url = driver.find_element_by_xpath('//*[@id="listresult"]/li['+str(i)+']/a[1]').get_attribute("href")
    element = driver.find_element_by_xpath('//*[@id="listresult"]/li['+str(i)+']/a[2]')
    driver.get(element.get_attribute("href"))
    race_name = driver.find_element_by_xpath('//*[@id="titrecourse"]/h1').text
    driver.find_element_by_xpath('//*[@id="liongletkikou"]/a').click()
    number_of_runners = driver.find_element_by_xpath('//*[@id="ongletkikou"]/div[7]/p/a').text
    number_of_runners = re.sub('coureurs', '', number_of_runners)  # partecipants
    driver.find_element_by_xpath('//*[@id="liongletinfo"]/a').click()
    data = driver.find_element_by_xpath('//*[@id="ongletinfo"]/div[1]/div/p').text  # race date
    list = format_text(data)
    date = date_format(list[0])                                                                                         # we can have different groups of informations (probably based on how the admin inserted it)
    if len(list) > 2:                                                                                                   # so we need to handle it as much as possible
        elevation = list[2]
    else:
        elevation = 0
    race = Race(elevation, date, number_of_runners, race_name, list[1])                                                 # create the race
    insert_race(race)
    id_race = get_race_id(race)
    print("fetched id race #"+str(id_race))
    driver.get(results_url)
    if table_filled(driver):                                                                                            # is the table is filled we can start to scrape the athlete's results
        scrape_routine(id_race,driver)
