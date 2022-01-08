from selenium import webdriver
from functions import concate_profile_data, df_to_db, concate_performance_data, fill_links, db_to_df, get_webdriver, transpose_with_first_row
import time
import random
from random import randint, seed
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd

