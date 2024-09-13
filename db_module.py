import os
import time
import traceback

import aiopg
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor


columns = ('Root Domain,'
           'updated_at,'
           'status,'
           'price link,subscription,free trial,free trial price page,redirecting_url,GlobalRank,TrafficSources Social,TrafficSources Paid Referrals,TrafficSources Mail,TrafficSources Referrals,TrafficSources Search,TrafficSources Direct,Category,TopKeywords,SnapshotDate,Engagments PagePerVisit,Engagments Visits,Engagments TimeOnSite,Engagments BounceRate'
           '')


Q_CREATE_STRIPE_SITES = """
CREATE TABLE IF NOT EXISTS public.stripe_sites (
    root_domain VARCHAR(255),
    updated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(255),
    price_link TEXT,
    subscription BOOLEAN,
    free_trial BOOLEAN,
    free_trial_price_page BOOLEAN,
    redirecting_url VARCHAR(255),
    global_rank NUMERIC,
    traffic_sources_social NUMERIC,
    traffic_sources_paid_referrals NUMERIC,
    traffic_sources_mail NUMERIC,
    traffic_sources_referrals NUMERIC,
    traffic_sources_search NUMERIC,
    traffic_sources_direct NUMERIC,
    category VARCHAR(255),
    top_keywords TEXT,
    snapshot_date VARCHAR(255),
    engagements_page_per_visit NUMERIC,
    engagements_visits NUMERIC,
    engagements_time_on_site NUMERIC,
    engagements_bounce_rate NUMERIC
);

"""

ON_CONFLICT = """
ON CONFLICT (root_domain) DO UPDATE
SET 
    updated_at = EXCLUDED.updated_at,
    status = EXCLUDED.status,
    price_link = EXCLUDED.price_link,
    subscription = EXCLUDED.subscription,
    free_trial = EXCLUDED.free_trial,
    free_trial_price_page = EXCLUDED.free_trial_price_page,
    redirecting_url = EXCLUDED.redirecting_url,
    global_rank = EXCLUDED.global_rank,
    traffic_sources_social = EXCLUDED.traffic_sources_social,
    traffic_sources_paid_referrals = EXCLUDED.traffic_sources_paid_referrals,
    traffic_sources_mail = EXCLUDED.traffic_sources_mail,
    traffic_sources_referrals = EXCLUDED.traffic_sources_referrals,
    traffic_sources_search = EXCLUDED.traffic_sources_search,
    traffic_sources_direct = EXCLUDED.traffic_sources_direct,
    category = EXCLUDED.category,
    top_keywords = EXCLUDED.top_keywords,
    snapshot_date = EXCLUDED.snapshot_date,
    engagements_page_per_visit = EXCLUDED.engagements_page_per_visit,
    engagements_visits = EXCLUDED.engagements_visits,
    engagements_time_on_site = EXCLUDED.engagements_time_on_site,
    engagements_bounce_rate = EXCLUDED.engagements_bounce_rate;
"""


DB_TABLE_NAME = 'stripe_sites'
# CREDS = {
#     'host': "127.0.0.1",
#     'dbname': 'testo',
#     'user': "postgres",
#     'password': 112,
#     'port': 5433,
# }
import os
CREDS = {
    'host': os.environ.get("DB_HOST"),
    'dbname': 'postgres',
    'user': "postgres",
    'password': os.environ.get("DB_PASS"),
    'port': 5432,
}


def execute_db(cursor, connection, df):
    try:
        tuples = [tuple(x) for x in df.to_numpy()]
        cols = ','.join(list(df.columns))
        query = "INSERT INTO %s(%s) VALUES %%s" % (DB_TABLE_NAME, cols)

        psycopg2.extras.execute_values(cursor, query, tuples)
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as err:
        print(f'Error {err}')
        connection.rollback()
        connection.close()
    finally:
        cursor.close()


def simple_execute(query):
    try:
        with PSQLConnector(**CREDS) as connection:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)
            connection.commit()
    except Exception as err:
        print(err)
    finally:
        cursor.close()


def write_to_db(connection, to_db_list, table_name, confl_st=None):
    # cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    signs = ['%s'] * len(to_db_list[0])
    signs = '(' + ','.join(signs) + ')'
    args_str = b','.join(cursor.mogrify(signs, x) for x in to_db_list)
    args_str = args_str.decode()

    insert_statement = """INSERT INTO %s VALUES """ % table_name
    if confl_st:
        conflict_statement = confl_st
    else:
        conflict_statement = """ ON CONFLICT DO NOTHING"""
    attempts = 0
    while attempts <= 3:
        attempts += 1
        try:
            cursor.execute(insert_statement + args_str + conflict_statement)
            connection.commit()

            return True
        except Exception as e:
            print(traceback.format_exc())
            if attempts >= 5:
                connection.rollback()
                attempts += 1
                time.sleep(3)
            else:
                raise e


def create_table():
    with PSQLConnector(**CREDS) as conn:
        cursor = conn.cursor()
        cursor.execute(Q_CREATE_STRIPE_SITES)
        conn.commit()
        cursor.close()


class PSQLConnector:
    """Context manager for accessing databases using `with` context manager"""

    def __init__(
            self,
            port: int = 5432,
            host: str = None,
            dbname: str = None,
            user: str = None,
            password: str = None,
            cursor_factory=None,
            # application_name: str = None,
    ):
        if not cursor_factory:
            self._cursor_factory = RealDictCursor
        else:
            self._cursor_factory = cursor_factory
        self._connect_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        # self._application_name = application_name or get_alternate_application_name()

    def __enter__(self):
        for _ in range(5):
            try:
                self.connection = psycopg2.connect(
                    self._connect_url,
                    cursor_factory=self._cursor_factory,
                    # application_name=self._application_name,
                )
                return self.connection
            except Exception as e:
                print(e)
                continue
        else:
            raise Exception('Max postgres connection attempts exceeded.')

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            self.connection.commit()
        else:
            self.connection.rollback()
        self.connection.close()


class AIOPSQLConnector:
    """Context manager for accessing databases using `with` context manager"""

    def __init__(
            self,
            port: int = 5432,
            host: str = None,
            dbname: str = None,
            user: str = None,
            password: str = None,
            cursor_factory=None,
            # application_name: str = None,
    ):
        if not cursor_factory:
            self._cursor_factory = RealDictCursor
        else:
            self._cursor_factory = cursor_factory
        self._connect_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        # self._application_name = application_name or get_alternate_application_name()
        self.pool = None

    async def __aenter__(self):
        for _ in range(5):
            try:
                self.pool = await aiopg.create_pool(self._connect_url)
                self.connection = await self.pool.acquire()
                return self.connection
            except Exception as e:
                print(e)
                continue

        else:
            raise Exception('Max postgres connection attempts exceeded.')

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.connection.close()


async def async_write_to_db(connection, to_db_list, table_name, confl_st=None):
    cursor = await connection.cursor(cursor_factory=RealDictCursor)
    signs = ['%s'] * len(to_db_list[0])
    signs = '(' + ','.join(signs) + ')'
    args_str = b','.join(cursor.mogrify(signs, x) for x in to_db_list)
    args_str = args_str.decode()

    insert_statement = """INSERT INTO %s VALUES """ % table_name
    if confl_st:
        conflict_statement = confl_st
    else:
        conflict_statement = """ ON CONFLICT DO NOTHING"""
    attempts = 0
    while attempts <= 3:
        attempts += 1
        try:
            await cursor.execute(insert_statement + args_str + conflict_statement)
            return True
        except Exception as e:
            print(traceback.format_exc())

            if attempts != 5:
                attempts += 1
                time.sleep(3)
            else:
                raise e


if __name__ == '__main__':
    create_table()
    # df = pd.read_csv("files/domains1M.csv")
    file_path = "files/domains1M.csv"

    chunk_size = 10000
    with PSQLConnector(**CREDS) as conn:
        start_position = 340 # else error
        with open(file_path, 'r') as f:
            f.seek(start_position)
            for n, chunk in enumerate(pd.read_csv(f, chunksize=chunk_size)):
                chunk_root_domain = chunk[['Root Domain']]
                res = write_to_db(conn, to_db_list=list(chunk_root_domain.to_numpy().tolist()),
                                  table_name=f'{DB_TABLE_NAME} (root_domain)')
    # domains = df.to_dict(orient='records')

    print()