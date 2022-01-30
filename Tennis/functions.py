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
                       "After_Losing_1st_Set", "Tie_Breaks", "Deciding_Set_Tie_Breaks", "Outdoor", "Indoor",
                       "Best_of_3", "Best_of_5", "Vs_No_1", "Vs_Top_5", "Vs_Top_10", "Vs_Top_20",
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
                       "player"]

statistics_columns = ['Aces',
                      'Ace_pct',
                      'Aces_per_Svc_Game',
                      'Aces_per_Set',
                      'Aces_per_Match',
                      'Double_Faults',
                      'Double_Fault_pct',
                      'DFs_per_Second_Serve_pct',
                      'DFs_per_Svc_Game',
                      'DFs_per_Set',
                      'DFs_per_Match',
                      'Aces_per_DFs_Ratio',
                      'Ace_Against',
                      'Ace_Against_pct',
                      'Double_Faults_Against',
                      'Double_Fault_Against_pct',
                      'First_Serve_pct',
                      'First_Serve_Won_pct',
                      'Second_Serve_Won_pct',
                      'First_Serve_Effectiveness',
                      'Serve_Rating',
                      'Service_Points_Won_pct',
                      'Svc_In_play_Pts_Won_pct',
                      'Points_per_Service_Game',
                      'Pts_Lost_per_Svc_Game',
                      'Break_Points_Saved_pct',
                      'BPs_per_Svc_Game',
                      'BPs_Faced_per_Set',
                      'BPs_Faced_per_Match',
                      'Service_Games_Won_pct',
                      'Svc_Gms_Lost_per_Set',
                      'Svc_Gms_Lost_per_Match',
                      'Serve_Max_Speed',
                      'First_Serve_Average_Speed',
                      'Second_Serve_Average_Speed',
                      'Serve_Average_Speed',
                      'First_per_Second_Srv_Spd_Ratio',
                      'Srv_Max_per_Avg_Spd_Ratio',
                      'First_Srv_Return_Won_pct',
                      'Second_Srv_Return_Won_pct',
                      'Return_Rating',
                      'Return_Points_Won_pct',
                      'Rtn_In_play_Pts_Won_pct',
                      'Points_per_Return_Game',
                      'Pts_Won_per_Rtn_Game',
                      'Break_Points_Won_pct',
                      'BPs_per_Return_Game',
                      'BPs_per_Set',
                      'BPs_per_Match',
                      'Return_Games_Won_pct',
                      'Rtn_Gms_Won_per_Set',
                      'Rtn_Gms_Won_per_Match',
                      'Total_Points_Played',
                      'Total_Points_Won',
                      'Total_Points_Won_pct',
                      'Tot_Second_Srv_In_pl_Pts_W_pct',
                      'Total_Break_Points_Won_pct',
                      'Rtn_to_Svc_Points_Ratio',
                      'Points_per_Game',
                      'Points_per_Set',
                      'Points_per_Match',
                      'Winner_pct',
                      'Unforced_Error_pct',
                      'Forced_Error_pct',
                      'Winners_per_UEs_Ratio',
                      'Winner_Against_pct',
                      'UE_Against_pct',
                      'FE_Against_pct',
                      'Wnrs_per_FEs_Against_Ratio',
                      'Net_Points_pct',
                      'Net_Points_Won_pct',
                      'Points_Won_at_Net_pct',
                      'Net_Effectiveness',
                      'Total_Games_Played',
                      'Total_Games_Won',
                      'Games_Won_pct',
                      'Games_per_Set',
                      'Games_per_Match',
                      'Tie_Breaks_Played',
                      'Tie_Breaks_Won',
                      'Tie_Breaks_Won_pct',
                      'Tie_Breaks_per_Set_pct',
                      'Tie_Breaks_per_Match',
                      'Sets_Played',
                      'Sets_Won',
                      'Sets_Won_pct',
                      'Sets_per_Match',
                      'Matches_Played',
                      'Matches_Won',
                      'Matches_Won_pct',
                      'Points_Dominance',
                      'In_play_Points_Dominance',
                      'Second_Srv_In_play_Pts_Dom',
                      'Games_Dominance',
                      'Break_Points_Ratio',
                      'Pts_to_Matches_Over_Perf',
                      'Pts_to_Sets_Over_Perf',
                      'Pts_to_Gms_Over_Perf',
                      'S_Pts_to_S_Gms_Ov_Perf',
                      'R_Pts_to_R_Gms_Ov_Perf',
                      'Pts_to_TBs_Over_Perf',
                      'Gms_to_Matches_Ov_Perf',
                      'Gms_to_Sets_Over_Perf',
                      'Sets_to_Matches_Ov_Perf',
                      'BPs_Over_Performing',
                      'BPs_Saved_Over_Perf',
                      'BPs_Conv_Over_Perf',
                      'Opponent_Rank',
                      'Opponent_Elo_Rating',
                      'Upsets_scored',
                      'Upsets_scored_pct',
                      'Upsets_against',
                      'Upsets_against_pct',
                      'Upsets',
                      'Upsets_pct',
                      'Point_Time_seconds',
                      'Game_Time_minutes',
                      'Set_Time_minutes',
                      'Match_Time',
                      'player']


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
    wd = get_webdriver()
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
    wd = get_webdriver()
    wd.get(link + '&tab=performance')
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


def concate_statistics_data(link, wd):
    wd.get(link + '&tab=statistics')
    html = wd.page_source
    frames = pd.read_html(html)
    stat = pd.concat([transpose_with_first_row(df) for df in frames[3:]], axis=1, join="inner")
    stat['player'] = wd.title[29:]
    stat.columns = stat.columns.str.replace(" ", "_")
    stat.columns = stat.columns.str.replace(".", "")
    stat.columns = stat.columns.str.replace(":", "_")
    stat.columns = stat.columns.str.replace("-", "_")
    stat.columns = stat.columns.str.replace("+", "_")
    stat.columns = stat.columns.str.replace("%", "pct")
    stat.columns = stat.columns.str.replace("/", "per")
    stat.columns = stat.columns.str.replace("(", "")
    stat.columns = stat.columns.str.replace(")", "")
    stat.columns = stat.columns.str.replace("1st", "First")
    stat.columns = stat.columns.str.replace("2nd", "Second")  # TODO
    stat.drop(columns=[col for col in stat if col not in statistics_columns], inplace=True)
    print(stat['player'])
    df_to_db(stat, 'tennis.statistics')


def df_to_db(df, table):
    conn = psycopg2.connect(**connect_dict)
    cursor = conn.cursor()
    df_columns = list(df)
    columns = ",".join(df_columns)
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
    insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)
    psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
    conn.commit()
    cursor.close()
    conn.close()


def fill_links(wd):
    link = "https://www.ultimatetennisstatistics.com/rankingsTable"
    wd.get(link)
    wd.find_element_by_xpath("""//*[@id="rankingsTable-header"]/div/div/div[5]/div[1]/button""").click()
    wd.find_element_by_xpath("""//*[@id="rankingsTable-header"]/div/div/div[5]/div[1]/ul/li[3]""").click()
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
    df = pd.read_sql("SELECT * FROM {}".format(table), dbconnection)
    return df


def populate_sql_table(table):
    for link in db_to_df('tennis.links')['link']:
        if table == 'tennis.profile':
            concate_profile_data(link)
        elif table == 'tennis.performance':
            concate_performance_data(link)
        elif table == 'tennis.statistics':
            concate_statistics_data(link, get_webdriver())

def populate_matches_table():
    for link in db_to_df('tennis.links')['link']:
        database = db_to_df('tennis.matches')

        wd = get_webdriver(headless=False)
        wd.maximize_window()
        wd.get(link+'&tab=matches')
        wd.find_element_by_xpath("""//*[@id="matchesTable-header"]/div/div/div[4]/div[1]/button""").click()
        wd.find_element_by_xpath("""//*[@id="matchesTable-header"]/div/div/div[4]/div[1]/ul/li[4]""").click()
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)

        try:
            html = wd.page_source
            df = pd.read_html(html)[0]
            df[['Winner', 'Loser']] = df['Match Details'].str.split(' d. ', 1, expand=True)
            df['Winner'] = df['Winner'].str.replace("[ ][\(].*?[\)]", "", regex=True)
            df['Loser'] = df['Loser'].str.replace("[ ][\(].*?[\)]", "", regex=True)
            df['Winner_elo'] = df['Winner'].str.extract('Elo (\d*)', expand=True)
            df['Winner_rank'] = df['Winner'].str.extract('Rank (\d*)', expand=True)
            df['Loser_elo'] = df['Loser'].str.extract('Elo (\d*)', expand=True)
            df['Loser_rank'] = df['Loser'].str.extract('Rank (\d*)', expand=True)
            df['Winner'] = df['Winner'].str.extract('(.+?(?= Rank))', expand=True)
            df['Loser'] = df['Loser'].str.extract('(.+?(?= Rank))', expand=True)
            df['Surface'] = df['Surface'].str.replace("[ ][\(].*?[\)]", "", regex=True)
            df['Score'] = df['Score'].str.replace("[\(].*?[\)]", "", regex=True)
            df.drop(['Match Details', 'H2H', 'W/L', 'Stats'], inplace=True, axis=1)
            pd.set_option('display.max_columns', None)
            df.columns = df.columns.str.lower()
            # df_to_db(df, 'tennis.matches')
        except StaleElementReferenceException:
            print('exception happened')
        finally:
            db_new_merge = database.merge(df.drop_duplicates(subset=['date', 'winner', 'loser']),
                                          how='right', indicator=True)
            df_new = db_new_merge[db_new_merge['_merge'] == 'right_only']
            df_new.drop(['_merge'], axis=1, inplace=True)
            print('there were {} originally, but only {} is added'.format(len(df),len(df_new)))
            df_to_db(df_new, 'tennis.matches')
            time.sleep(randint(2, 7))
            wd.quit()


# in case it's not working, here are the populate functions for each table
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
