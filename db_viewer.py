import sqlite3
import pandas as pd

def read_table(table: str):
    with sqlite3.connect('byte_server.db') as db:
        return pd.read_sql_query(f'SELECT * FROM {table}', db)

def tournaments():
    return read_table('tournament')

def teams():
    return read_table('team')

def runs():
    return read_table('run')

def turns():
    return read_table('turn')

def submissions():
    return read_table('submission')

def universities():
    return read_table('university')

def team_types():
    return read_table('team_type')

def submission_run_infos():
    return read_table('submission_run_info')


