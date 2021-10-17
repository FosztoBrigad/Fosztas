import pandas as pd
import psycopg2
import psycopg2.extras
from sql import connect_dict


profile_columns = ['Age', 'Country', 'Birthplace', 'Residence', 'Height', 'Weight',
       'Plays', 'Backhand', 'Favorite_Surface', 'Coach', 'Turned_Pro',
       'Seasons', 'Active', 'Prize_Money', 'Wikipedia', 'Website', 'Facebook',
       'Twitter', 'Nicknames', 'Titles', 'Grand_Slams', 'Tour_Finals',
       'Masters', 'Davis_Cups', 'Team_Cups', 'Current_Rank', 'Best_Rank',
       'Current_Elo_Rank', 'Best_Elo_Rank', 'Peak_Elo_Rating', 'GOAT_Rank',
       'Weeks_at_No_1', 'Best_Season', 'Last_Appearance',
       'Overall', 'Hard', 'Clay', 'Grass', 'Carpet', 'Name']
#see sql.py for the approach to get them from sql db instead of hard coding it

def transpose_with_first_row(df):
    df=df.T
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
    return(df)

def concate_profile_data(wd,link):
    wd.get(link)
    get_title = wd.title[29:]
    html = wd.page_source
    frames = pd.read_html(html)
    df1 = transpose_with_first_row(frames[0])
    df2 = transpose_with_first_row(frames[1])
    df3 = create_df_from_records(frames[2])
    profile = pd.concat([df1, df2, df3], axis=1, join="inner")
    profile['Name']=get_title
    profile.columns = profile.columns.str.replace(" ", "_")
    profile.columns = profile.columns.str.replace(".", "")
    profile.drop(columns=[col for col in profile if col not in profile_columns], inplace=True)
    return profile

def profile_df_to_db(df):
    conn = psycopg2.connect(**connect_dict)
    cursor = conn.cursor()
    df_columns = list(df)
    columns = ",".join(df_columns)
    values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
    insert_stmt = "INSERT INTO {} ({}) {}".format('tennis.profile', columns, values)
    print(insert_stmt)
    print(df.values)
    psycopg2.extras.execute_batch(cursor, insert_stmt, df.values)
    conn.commit()
    cursor.close()
    conn.close()