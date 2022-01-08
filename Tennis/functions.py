import pandas as pd
from selenium import webdriver
import psycopg2
import psycopg2.extras
from sql import connect_dict
from sqlalchemy import create_engine
import time
import random
from random import randint, seed
from selenium.common.exceptions import StaleElementReferenceException

profile_columns = ['Age', 'Country', 'Birthplace', 'Residence', 'Height', 'Weight',
                   'Plays', 'Backhand', 'Favorite_Surface', 'Coach', 'Turned_Pro',
                   'Seasons', 'Active', 'Prize_Money', 'Wikipedia', 'Website', 'Facebook',
                   'Twitter', 'Nicknames', 'Titles', 'Grand_Slams', 'Tour_Finals',
                   'Masters', 'Davis_Cups', 'Team_Cups', 'Current_Rank', 'Best_Rank',
                   'Current_Elo_Rank', 'Best_Elo_Rank', 'Peak_Elo_Rating', 'GOAT_Rank',
                   'Weeks_at_No_1', 'Best_Season', 'Last_Appearance',
                   'Overall', 'Hard', 'Clay', 'Grass', 'Carpet', 'Name']

# see sql.py for the approach to get them from sql db instead of hard coding it

# NOTE underscores are needed to insert into sql db
performance_columns = ["Hard", "Clay", "Grass", "Carpet", "Grand_Slam", "Tour_Finals", "Masters", "Olympics", "ATP_500",
                       "ATP_250", "Davis_Cup", "Team_Cups", "Deciding_Set", "Fifth_Set", "After_Winning_1st_Set",
                       "After_Losing_1st_Set", "Tie_Breaks",
                       "Deciding_Set_Tie_Breaks",
                       "Outdoor",
                       "Indoor",
                       "Best_of_3",
                       "Best_of_5",
                       "Vs_No_1",
                       "Vs_Top_5",
                       "Vs_Top_10",
                       "Vs_Top_20",
                       "Vs_Top_50",
                       "Vs_Top_100",
                       "Vs_100__Ranked",
                       "Vs_Higher_Ranked",
                       "Vs_Lower_Ranked",
                       "Final_round",
                       "For_Bronze_Medal_round",
                       "Semi_Final_round",
                       "Quarter_Final_round",
                       "Round_of_16_round",
                       "Round_of_32_round",
                       "Round_of_64_round",
                       "Round_of_128_round",
                       "Round_Robin_round",
                       "Very_Fast",
                       "Fast",
                       "Medium_Fast",
                       "Medium",
                       "Medium_Slow",
                       "Slow",
                       "Very_Slow",
                       "Vs_Higher_Elo",
                       "Vs_Lower_Elo",
                       "Vs_Right_Handed",
                       "Vs_Left_Handed",
                       "Vs_Two_Handed_bh",
                       "Vs_One_Handed_bh",
                       "Vs_Younger",
                       "Vs_Older",
                       "Vs_Shorter",
                       "Vs_Taller",
                       "Title_result",
                       "Final_result",
                       "Semi_Final_result",
                       "Quarter_Final_result",
                       "Round_of_16_result",
                       "Round_of_32_result",
                       "Round_of_64_result",
                       "Round_of_128_result",
                       "Round_Robin_result",
                       "Bronze_Medal_result",
                       "Best_of_3__2_0",
                       "Best_of_3__2_1",
                       "Best_of_3__1_2",
                       "Best_of_3__0_2",
                       "Best_of_5__3_0",
                       "Best_of_5__3_1",
                       "Best_of_5__3_2",
                       "Best_of_5__2_3",
                       "Best_of_5__1_3",
                       "Best_of_5__0_3",
                       "player"
                       ]


def get_webdriver(headless=True):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(PATH, options=options)
    return wd


def transpose_with_first_row(df):
    df = df.T
    df.dropna(axis=1, inplace=True)
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    return df


def create_df_from_records(empty_df):
    dict_empty_df = empty_df.to_dict()
    tuple_list = list(dict_empty_df.keys())
    tuple_list = tuple_list[0:2]
    df = pd.DataFrame(tuple_list)
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    return df


def concate_profile_data(link):
    wd=get_webdriver()
    wd.get(link)
    get_title = wd.title[29:]
    html = wd.page_source
    frames = pd.read_html(html)
    df1 = transpose_with_first_row(frames[0])
    df2 = transpose_with_first_row(frames[1])
    df3 = create_df_from_records(frames[2])
    profile = pd.concat([df1, df2, df3], axis=1, join="inner")
    profile['Name'] = get_title
    profile.columns = profile.columns.str.replace(" ", "_")
    profile.columns = profile.columns.str.replace(".", "")
    profile.drop(columns=[col for col in profile if col not in profile_columns], inplace=True)
    df_to_db(profile, 'tennis.profile')

def concate_performance_data(link):
    wd=get_webdriver()
    wd.get(link)
    html = wd.page_source
    frames = []
    for i in pd.read_html(html):
        df = transpose_with_first_row(i)
        if i.T.index[0] == 'Round Breakdown':
            df = df.add_suffix('_round')
        elif i.T.index[0] == 'Result Breakdown':
            df = df.add_suffix('_result')
        df.reset_index(drop=True, inplace=True)
        frames.append(df)

    df = pd.concat(frames, axis=1, join="inner")
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace(".", "")
    df.columns = df.columns.str.replace(":", "_")
    df.columns = df.columns.str.replace("-", "_")
    df.columns = df.columns.str.replace("+", "_")
    df['player'] = wd.title[29:]
    df.drop(columns=[col for col in df if col not in performance_columns], inplace=True)
    df_to_db(df, 'tennis.performance')


def df_to_db(df, table):
    conn = psycopg2.connect(**connect_dict)
    cursor = conn.cursor()
    df_columns = list(df)
    columns = ",".join(df_columns)
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
    insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)
    # print(insert_stmt)
    # print(df.values)
    psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
    conn.commit()
    cursor.close()
    conn.close()


def fill_links(wd):
    link = "https://www.ultimatetennisstatistics.com/rankingsTable"
    wd.get(link)
    dropdown = wd.find_element_by_xpath("""//*[@id="rankingsTable-header"]/div/div/div[5]/div[1]/button""").click()
    top100 = wd.find_element_by_xpath("""//*[@id="rankingsTable-header"]/div/div/div[5]/div[1]/ul/li[3]""").click()
    # wd.quit()
    try:
        links_list = [url.get_attribute('href') for url in wd.find_elements_by_tag_name('a') if
                      url.get_attribute('href') is not None and 'player' in url.get_attribute('href')]
    except StaleElementReferenceException:
        links_list = [url.get_attribute('href') for url in wd.find_elements_by_tag_name('a') if
                      url.get_attribute('href') is not None and 'player' in url.get_attribute('href')]
        df = pd.DataFrame(links_list, columns=['link'])
        df_to_db(df, 'tennis.links')


def db_to_df(table):
    engine = create_engine('postgresql+psycopg2://postgres:zsakaszi666@localhost:5432/fosztas')
    dbconnection = engine.connect()
    df = pd.read_sql("SELECT link FROM {}".format(table), dbconnection)
    return df

def populate_sql_table(table):
    for link in db_to_df('tennis.links')['link']:
        print(link)
        seed(randint(2, 100))
        period = random.uniform(1, 6)
        if table=='tennis.profile':
            concate_profile_data(link)
        elif table=='tennis.performance':
            concate_performance_data(link+"&tab=performance")
        print(link)
        time.sleep(period)



#in case it's not working, here are the populate functions for each table
"""        
def populate_profile():
    for link in db_to_df('tennis.links')['link']:
        seed(randint(2, 100))
        period = random.uniform(1, 6)
        concate_profile_data(link)
        time.sleep(period)

def populate_performance():
    for link in db_to_df('tennis.links')['link']:
        seed(randint(2, 100))
        period = random.uniform(1, 6)
        concate_performance_data(link+"&tab=performance")
        print(link)
        time.sleep(period)"""