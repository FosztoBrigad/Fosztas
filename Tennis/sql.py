import psycopg2
connect_dict = {'dbname': 'fosztas', 'user':'postgres', 'password': 'zsakaszi666', 'host': 'localhost'}
create_profile=''' CREATE TABLE IF NOT EXISTS tennis.profile (
                    Name varchar(50) Primary Key, 
                    Age varchar(50), 
                    Country varchar(50),
                    Birthplace varchar(50), 
                    Residence varchar(50),
                    Height varchar(50), 
                    Weight varchar(50),
                    Plays varchar(50), 
                    Backhand varchar(50), 
                    Favorite_Surface varchar(50), 
                    Coach varchar(50), 
                    Turned_Pro INT,
                    Seasons varchar(50), 
                    Active varchar(50), 
                    Prize_Money varchar(50), 
                    Wikipedia varchar(50), 
                    Website varchar(50), 
                    Facebook varchar(50),
                    Twitter varchar(50), 
                    Nicknames varchar(50), 
                    Titles varchar(50), 
                    Grand_Slams varchar(50), 
                    Tour_Finals varchar(50),
                    Masters varchar(50), 
                    Davis_Cups varchar(50), 
                    Team_Cups varchar(50), 
                    Current_Rank varchar(50), 
                    Best_Rank varchar(50),
                    Current_Elo_Rank varchar(50), 
                    Best_Elo_Rank varchar(50), 
                    Peak_Elo_Rating varchar(50), 
                    GOAT_Rank varchar(50),
                    Weeks_at_No_1 INT, 
                    Best_Season varchar(50), 
                    Last_Appearance varchar(50), 
                    Overall varchar(50), 
                    Hard varchar(50), 
                    Clay varchar(50), 
                    Grass varchar(50), 
                    Carpet varchar(50)
)'''

create_links = '''CREATE TABLE IF NOT EXISTS tennis.links (
                   link varchar (70) 
)'''
create_performance = '''CREATE TABLE IF NOT EXISTS tennis.performance(
                    Player varchar(50) Primary Key,
                    Hard varchar(50),
                    Clay varchar(50),
                    Grass varchar(50),
                    Carpet varchar(50),
                    Grand_Slam varchar(50),
                    Tour_Finals varchar(50),
                    Masters varchar(50),
                    Olympics varchar(50),
                    ATP_500 varchar(50),
                    ATP_250 varchar(50),
                    Davis_Cup varchar(50),
                    Team_Cups varchar(50),
                    Deciding_Set varchar(50),
                    Fifth_Set varchar(50),
                    After_Winning_1st_Set varchar(50),
                    After_Losing_1st_Set varchar(50),
                    Tie_Breaks varchar(50),
                    Deciding_Set_Tie_Breaks varchar(50),
                    Outdoor varchar(50),
                    Indoor varchar(50),
                    Best_of_3 varchar(50),
                    Best_of_5 varchar(50),
                    Vs_No_1 varchar(50),
                    Vs_Top_5 varchar(50),
                    Vs_Top_10 varchar(50),
                    Vs_Top_20 varchar(50),
                    Vs_Top_50 varchar(50),
                    Vs_Top_100 varchar(50),
                    Vs_100__Ranked varchar(50),
                    Vs_Higher_Ranked varchar(50),
                    Vs_Lower_Ranked varchar(50),
                    Final_round varchar(50),
                    For_Bronze_Medal_round varchar(50),
                    Semi_Final_round varchar(50),
                    Quarter_Final_round varchar(50),
                    Round_of_16_round varchar(50),
                    Round_of_32_round varchar(50),
                    Round_of_64_round varchar(50),
                    Round_of_128_round varchar(50),
                    Round_Robin_round varchar(50),
                    Very_Fast varchar(50),
                    Fast varchar(50),
                    Medium_Fast varchar(50),
                    Medium varchar(50),
                    Medium_Slow varchar(50),
                    Slow varchar(50),
                    Very_Slow varchar(50),
                    Vs_Higher_Elo varchar(50),
                    Vs_Lower_Elo varchar(50),
                    Vs_Right_Handed varchar(50),
                    Vs_Left_Handed varchar(50),
                    Vs_Two_Handed_bh varchar(50),
                    Vs_One_Handed_bh varchar(50),
                    Vs_Younger varchar(50),
                    Vs_Older varchar(50),
                    Vs_Shorter varchar(50),
                    Vs_Taller varchar(50),
                    Title_result varchar(50),
                    Final_result varchar(50),
                    Semi_Final_result varchar(50),
                    Quarter_Final_result varchar(50),
                    Round_of_16_result varchar(50),
                    Round_of_32_result varchar(50),
                    Round_of_64_result varchar(50),
                    Round_of_128_result varchar(50),
                    Round_Robin_result varchar(50),
                    Bronze_Medal_result varchar(50),
                    Best_of_3__2_0  varchar(50),
                    Best_of_3__2_1  varchar(50),
                    Best_of_3__1_2  varchar(50),
                    Best_of_3__0_2  varchar(50),
                    Best_of_5__3_0  varchar(50),
                    Best_of_5__3_1  varchar(50),
                    Best_of_5__3_2  varchar(50),
                    Best_of_5__2_3  varchar(50),
                    Best_of_5__1_3  varchar(50),
                    Best_of_5__0_3  varchar(50)
)'''

update_links = '''UPDATE tennis.links

'''










#GET column names instead of hard coding it.
"""
conn = psycopg2.connect(**connect_dict)
cursor = conn.cursor()
statement = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'profile'"
cursor.execute(statement)
print(cursor.fetchall())
conn.commit()
cursor.close()
conn.close()"""