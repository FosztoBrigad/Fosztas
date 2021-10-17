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