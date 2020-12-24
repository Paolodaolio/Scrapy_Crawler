from Database.postgre_DB_manager import *
from classes import Club, Record_Club_Person, Record_Race_Person
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from string_tools import format_time
from classes import Person
from Database.postgre_DB import give_cursor


def scrape_name_in_page(id_race, driver):                                                                               # func to scrape names & performance from the list of results
    elements = driver.find_elements_by_tag_name("tr")
    limit = len(elements)
    for index in range(1, limit-6):
        try:
            time_race = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr['+str(index)+']/td[3]').text
            name = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr['+str(index)+']/td[4]').text
            category = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr['+str(index)+']/td[5]').text
            club_name = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr['+str(index)+']/td[6]').text
            score = driver.find_element_by_xpath('/html/body/div/div[3]/div/div[2]/table/tbody[2]/tr['+str(index)+']/td[7]').text
        except NoSuchElementException:
            time_race = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr['+str(index)+']/td[3]').text           # 2 possible type of table
            name = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr['+str(index)+']/td[4]').text
            category = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr[' + str(index) + ']/td[5]').text
            club_name = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr[' + str(index) + ']/td[6]').text
            score = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div/table/tbody[2]/tr[' + str(index) + ']/td[7]').text
        finally:
            time_race = format_time(time_race)
            person = Person(name)
            insert_person(person)
            id_person = fetch_runner_by_name(person.name)
            race_record = Record_Race_Person(id_person, id_race, score, time_race, category)
            insert_record_race_person(race_record)
            if club_name is not " ":
                club = Club(club_name)                                                                                  # once we collect data, we create python's obj and then we store what we need
                insert_club(club)
                id_club = get_club_id(club)
                club_record = Record_Club_Person(id_club, id_person)
                insert_record_club_person(club_record)


def elem_to_click(elements, index):                                                                                     # used to pass from a page to another inside a structure called Pager(html)
    exception = False
    try:
        scraping = True
        i = 0
        while scraping:
            ele = elements[i]
            number = ele.get_attribute("page")
            if number is None:
                pass
            elif int(number) == index+1:
                # print("found the element", number)
                output = ele
                scraping = False
            else:
                pass
            i += 1
    except IndexError:
        exception = True
    finally:
        if not exception:
            return output
        else:
            return 0


def scrape_routine(id_race, driver):                                                                                    # here we have the main routine for the person collection
    scraping = True
    last_clicked = 0
    i = 1
    while scraping:
        elements = driver.find_elements_by_class_name("yui-pg-page")                                                    # check how many pages
        elements.pop(0)
        elements = elements[:int(len(elements)/2)]
        scrape_name_in_page(id_race, driver)
        to_click = elem_to_click(elements, i)                                                                           # compute which is the next page
        if to_click:
            last_clicked = int(to_click.get_attribute("page"))
            to_click.click()                                                                                            # here we follow the href(html)
        else:
            break
        i += 1
        time.sleep(2)
        if i > last_clicked:                                                                                            # this condition is used to understand WHEN we finished all the pages for each result's table
            scraping = False



