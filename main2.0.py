import scrapy
from selenium import webdriver
from scrapy import Selector
import re
from classes import Race
from scrapy.crawler import CrawlerProcess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     urls = ['http://www.kikourou.net/resultats/poupard+guillaume.html']  # runs for specific user
#
#     def start_requests(self):
#         next_url = '//*[@id="tableresultats"]/tbody/tr[1]/td[2]/a[2]'                       # href to get partecipants
#         urls.append(next_url)
#
#         # # while True:
#         #     next_url = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/div[1]/a[3]').click()
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)
#             driver.get(url)
#
#     def parse(self, response):
#         print(response)
#         # sel = Selector(text=response)
#         # print(sel.xpath("//dd//text()").getall())
#         # print(sel.xpath('//*[@id="ongletfiche"]/dl/dd[1]/font/font').extract())
#
#
#         # for t in response.xpath('//*[@id="ongletfiche"]/dl/dd[1]/font/font'):
#         #     print(t.get())


def scrape_races(url,driver):
    classe = '/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr/td[2]/div'
    perf = '/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr/td[3]/div'
    nom = '/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr/td[4]/div'
    cat = '/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr/td[5]/div'
    club = '/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr/td[6]/div'

    input_elem = driver.find_element_by_xpath('// *[ @ id = "filtrenom"]')
    input_elem.send_keys("poupard guillaume")
    driver.implicitly_wait(2)
    try:
        element = WebDriverWait(driver, 2).until(   # this is needed to wait the browser load the html
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "poupard guillaume"))
        )
    except TimeoutException:
        pass
    finally:
        position = driver.find_element_by_xpath(classe).text
        time = driver.find_element_by_xpath(perf).text
        nom = driver.find_element_by_xpath(nom).text
        category = driver.find_element_by_xpath(cat).text
        club = driver.find_element_by_xpath(club).text
        date_race = driver.find_element_by_xpath('//*[@id="contenuprincipal"]/p').text
        date_race = re.sub('Voir la fiche de la course :', '', date_race)
        date = date_race.split(' du ')[-1]
        date_race = re.sub(' du '+date, '', date_race)
    print(position,time,nom,category,club,date_race,date)
    race = Race(position,time,nom,category,club,date_race,date)
    return race

driver_path = 'C:/Users/paolo/chrome_driver/chromedriver.exe'
driver = webdriver.Chrome(executable_path=driver_path)
url = 'http://www.kikourou.net/resultats/poupard+guillaume.html'
driver.get(url)
limit = driver.find_elements_by_class_name('new')   # we need the number of races
races = []

for i in range(1,len(limit)):
    if i!=1:
        driver.get(url)
    driver.find_element_by_xpath('//*[@id="tableresultats"]/tbody/tr['+str(i)+']/td[2]/a[2]').click()   #that goes on members of the race
    driver.implicitly_wait(1)
    races.append(scrape_races(url,driver))

driver.close()

# I'm not using spider right now

# spider = QuotesSpider("spider")
# process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
# process.crawl(QuotesSpider)
# process.start() # the script will block here until the crawling is finished