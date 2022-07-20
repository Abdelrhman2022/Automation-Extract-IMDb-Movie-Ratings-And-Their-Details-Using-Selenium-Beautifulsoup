#  Imports

from selenium import webdriver
import pandas as pd 
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By


#  Part 1 - Browser Automation with Selenium


driver = webdriver.Chrome(executable_path= r'.\chromedriver.exe')
driver.get('https://imdb.com')

# maximize window
driver.maximize_window()
time.sleep(3)


# dropdown
dropdown = driver.find_element(By.CLASS_NAME ,'nav-search-form__categories')
dropdown.click()
time.sleep(1)

# avanced search from dropdown menu
element = driver.find_element( By.LINK_TEXT,'Advanced Search')
element.click()
time.sleep(3)

# click on avanced title search
adv_title = driver.find_element(By.LINK_TEXT,'Advanced Title Search')
adv_title.click() 
time.sleep(3)


# select feature film
feature_film = driver.find_element(By.ID,'title_type-1')
feature_film.click() 

# select tv movie
tv_movie = driver.find_element(By.ID,'title_type-2')
tv_movie.click()

# min date
min_date = driver.find_element(By.NAME,'release_date-min')
min_date.click()
min_date.send_keys('1990')

# max date
max_date = driver.find_element(By.NAME,'release_date-max')
max_date.click()
max_date.send_keys('2022')

# rating min
rating_min = driver.find_element(By.NAME,'user_rating-min')
rating_min.click()
dropdown_2 = Select(rating_min)
dropdown_2.select_by_visible_text('5.0')

# rating max
rating_max = driver.find_element(By.NAME,'user_rating-max')
rating_max.click()
dropdown_3 = Select(rating_max)
dropdown_3.select_by_visible_text('10')

# oscar nominated
oscar_nominated = driver.find_element(By.ID,'groups-7')
oscar_nominated.click()

# color
color = driver.find_element(By.ID, 'colors-1')
color.click()

# language
language = driver.find_element(By.CLASS_NAME,'languages')
dropdown_4 = Select(language)
dropdown_4.select_by_visible_text('English')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# 250 results
results_count = driver.find_element(By.ID,'search-count')
dropdown_5 = Select(results_count)
dropdown_5.select_by_index(2)

# submit
submit = driver.find_element(By.XPATH,'(//button[@type="submit"])[2]')
submit.click()

# current
current_url = driver.current_url 




# Extract Data with Beautiful Soup
total_list_items = []
def extract_data(current_url):
    # get request
    response = requests.get(current_url)
    time.sleep(3)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # result items (starting point)
    total_list_items.append(soup.find_all('div', {'class':'lister-item'})) 

extract_data(current_url)

while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        next_page = driver.find_element( By.LINK_TEXT,'Next »')
        next_page.click()
        # current 
        extract_data(driver.current_url )
    except:
        break


#  Data we need to extract

# - movie title
# - year
# - duration
# - genre
# - rating



# list comprehension
movie_title = []
year = []
duration = []
genre = []
rating = []
for list_items in total_list_items:
    for result in list_items:
        try:
            movie_title.append(result.find('h3').find('a').get_text())
        except:
            movie_title.append('')
            
        try:
            year.append(result.find('h3').find('span', {'class':'lister-item-year'}).get_text().replace('(', '').replace(')', '')
                        .replace('I ', '').replace('I', '').replace(' TV Movie', '').replace('V ', ''))
        except:
            year.append('')
            
        try:
            duration.append(result.find('span', {'class':'runtime'}).get_text())
        except:
            duration.append('')
        
        try:
            genre.append(result.find('span', {'class':'genre'}).get_text().strip())
        except:
            genre.append('')
            
        try:
            rating.append(result.find('div', {'class':'ratings-imdb-rating'}).get_text().strip() )
        except:
            rating.append('')




# create dataframe
imdb_df = pd.DataFrame({'Movie Title': movie_title, 'Year': year, 'Duration':duration,
                       'Genre': genre, 'Rating':rating})



imdb_df.head()



# output in CSV file
imdb_df.to_csv('imdb_multiple_pages.csv', index=False)






