from selenium import webdriver
from functions import get_webdriver, df_to_db, db_to_df, populate_matches_table
import random
import requests
from random import randint, seed
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import time
import json

profile=db_to_df('tennis.profile')
statistics=db_to_df('tennis.statistics')
matches=db_to_df('tennis.matches')
performance=db_to_df('tennis.performance')

profile.to_csv('profile.csv')
matches.to_csv('matches.csv')
statistics.to_csv('statistics.csv')
performance.to_csv('performance.csv')

