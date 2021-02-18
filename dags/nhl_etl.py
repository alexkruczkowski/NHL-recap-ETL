import requests
import json
import pandas as pd
from datetime import date, timedelta
import datetime
from extract import json_extract
import numpy as np
import sqlalchemy
from sqlalchemy.orm import sessionmaker 
import sqlite3

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # Check if dataframe is empty
    if df.empty:
        print("No games found. Finishing execution")
        return False 

    # Primary Key Check
    if pd.Series(df['game_id']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")

    # Check that dates in the data match yesterday's date
    yesterday = (date.today() - timedelta(1)).strftime('%Y-%m-%d')

    timestamps = df["date"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strftime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one of the returned games does not have yesterday's date")

    return True


def run_nhl_etl():
    database_location = "sqlite:///nhl_games_highlights.sqlite"
    # Extract yesterday's NHL game schedule
    yesterdays_date = (date.today() - timedelta(1)).strftime('%Y-%m-%d')

    response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?date={}".format(yesterdays_date))
    data = response.json()

    #Get yesterday's game info only if the game is complete
    game_status, game_content, game_links, home_score, home_team, away_score, away_team, game_id, game_date = ([] for i in range(9))

    for team in (data['dates'][0]['games']):
        if (team['status']['detailedState']) == 'Final':
            game_status.append(team['status']['detailedState'])
            game_content.append(team['content']['link'])
            game_links.append(team['link'])
            home_score.append(team['teams']['home']['score'])
            home_team.append(team['teams']['home']['team']['name'])
            away_score.append(team['teams']['away']['score'])
            away_team.append(team['teams']['away']['team']['name'])
            game_id.append((team['content']['link']).split('/')[4])
            game_date.append(yesterdays_date)
        else:
            pass

    #Find the link to the game recap on nhl.com
    video_recap = []
    for link in game_content:
        response = requests.get("https://statsapi.web.nhl.com/{}".format(link))
        names = json_extract(response.json(), 'url')
        link=([s for s in names if 'game-recap/' in s])
        video_recap.append('nhl.com'+link[0])

    #Insert game info and link to recap into a pandas df
    recap_df = pd.DataFrame(np.column_stack([game_date, game_id, game_status, game_content, game_links, home_team, \
                                            home_score, away_team, away_score, video_recap]), 
                                columns=['date', 'game_id', 'game_status', 'game_content','game_links','home_team', \
                                            'home_score','away_team','away_score', 'video_recap'])
    # Convert date column to datetime
    recap_df['date'] = pd.to_datetime(recap_df['date'])

    # Validate results
    if check_if_valid_data(recap_df):
        print("Data valid, proceed to Load stage")

    # Load
    engine = sqlalchemy.create_engine(database_location)
    conn = sqlite3.connect('nhl_games_highlights.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS nhl_games_highlights(
        date VARCHAR(200),
        game_id VARCHAR(200),
        game_status VARCHAR(200),
        game_content VARCHAR(200),
        game_links VARCHAR(200),
        home_team VARCHAR(200),
        home_score VARCHAR(200), 
        away_team VARCHAR(200),
        away_score VARCHAR(200),
        video_recap VARCHAR(300),
        CONSTRAINT primary_key_constraint PRIMARY KEY (game_id)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        recap_df.to_sql("nhl_games_highlights", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
        