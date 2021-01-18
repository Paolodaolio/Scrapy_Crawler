from race_scrape import table_filled
from selenium import webdriver
from name_scrape import scrape_routine
from string_tools import *
from Database.postgre_DB_manager import *
import time

driver_path = 'C:/Users/paolo/chrome_driver/chromedriver.exe'                                                           # driver for selenium
driver = webdriver.Chrome(executable_path=driver_path)
page_index = 25
race_index = 51                                                                                                         #partire minimo da 2
url = "http://www.kikourou.net/calendrier/resultats.php?resultats=1&resultatssigne=2&page=0"                            #+str(page_number)                                                                              # starting url
driver.get(url)


for page_number in range(page_index, 104):
    url = "http://www.kikourou.net/calendrier/resultats.php?resultats=1&resultatssigne=2&page=" + str(page_number)      # starting url
    driver.get(url)
    lis = driver.find_elements_by_tag_name("tr")  # check if it correct
    print("trovate "+str(len(lis)-5) + " gare nella pagina : " + str(url))
    for i in range(race_index, 101):                                                                                    # we loop the main routine on every race we found
        print("stiamo analizzando la corsa #"+str(page_number)+"."+str(i - 1))                                          # in the page we got maximum 100 races
        if i != 2:                                     # TODO PARTIAMO DA PAGINA 18 GARA 2
            url = "http://www.kikourou.net/calendrier/resultats.php?resultats=1&resultatssigne=2&page="+str(page_number)# starting url
            driver.get(url)

        driver.find_element_by_xpath("/html/body/div[1]/div[3]/table/tbody/tr["+str(i)+"]/td[2]/a").click()             # click on the race
        race_name = driver.find_element_by_xpath('//*[@id="titrecourse"]/h1').text
        results_url = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div[7]/p/a").get_attribute("href")
        driver.find_element_by_xpath('//*[@id="liongletkikou"]/a').click()
        number_of_runners = driver.find_element_by_xpath('//*[@id="ongletkikou"]/div[7]/p/a').text
        number_of_runners = re.sub('coureurs', '', number_of_runners)  # partecipants
        driver.find_element_by_xpath('//*[@id="liongletinfo"]/a').click()
        time.sleep(0.5)
        data = driver.find_element_by_xpath('//*[@id="ongletinfo"]/div[1]/div/p').text  # race date
        list = format_text(data)
        date = date_format(list[0])
        if len(list) > 2:                                                                                               # so we need to handle it as much as possible
            elevation = list[2]
        else:
            elevation = 0
        race = Race(elevation, date, number_of_runners, race_name, list[1])                                             # create the race
        insert_race(race)
        id_race = get_race_id(race)
        driver.get(results_url)
        if table_filled(driver):                                                                                        # is the table is filled we can start to scrape the athlete's results
            scrape_routine(id_race, driver)
