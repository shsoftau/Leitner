import openpyxl
import pandas as pd

from common_duckdb_qry import *

df = pd.read_excel('D:/Python/Leitner/import/import_cards.xlsx')
append_df_to_db(duckdb_fpath,'flashcards',df)

