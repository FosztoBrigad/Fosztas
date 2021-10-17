from selenium import webdriver
from functions import concate_profile_data, profile_df_to_db

PATH = "C:\Program Files (x86)\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome(PATH, options=options)
"""link = "https://www.ultimatetennisstatistics.com/rankingsTable"
wd.get(link)
links_list = [url.get_attribute('href') for url in wd.find_elements_by_tag_name('a') if url.get_attribute('href') is not None and 'player' in url.get_attribute('href')]
print(links_list)"""
# to do : click on all players, and for each in links_list, insert it into the db
link = 'https://www.ultimatetennisstatistics.com/playerProfile?playerId=6029&tab=profile'
profile_df = concate_profile_data(wd,link)
profile_df_to_db(profile_df)




