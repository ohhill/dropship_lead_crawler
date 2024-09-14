import json
import time
import traceback

import pandas as pd
# import hrequests
import requests
from urllib.parse import urlparse
# from hrequests import Session
from selectolax.lexbor import LexborHTMLParser
from multiprocessing.dummy import Pool, Lock

import urllib3

from db_module import PSQLConnector, CREDS, DB_TABLE_NAME, write_to_db, ON_CONFLICT

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from boto_operations import MediaS3
from playwright_module import render_page
from constants import (
    PROXY,
    PROXY_PLAYWRIGHT,
    SUBSCRIPTION_LIST,
    FREE_TRIAL_LIST,
    CLEANSING_SYMBOLS,
    COLUMNS_DOMAIN_INFO,
    HEADERS
)
IS_RENDER_PAGE = False
s3_bucket = MediaS3()

class ThreadSafeDict:
    def __init__(self):
        self.lock = Lock()
        self.data = {'result': [], 's_status': 0}

    def add(self, k, v):
        with self.lock:
            self.data[k] = v

    def get(self, k):
        with self.lock:
            return self.data[k]

    def append(self, k, v):
        with self.lock:
            self.data[k].append(v)

    def update(self, v_dict):
        with self.lock:
            self.data.update(v_dict)

lock = Lock()
stat = ThreadSafeDict()

def fetch(url: str):
    for _ in range(7):
        try:
            response = requests.get(url,
                                    headers=HEADERS,
                                    proxies=PROXY,
                                    timeout=30,
                                    verify=False,
                                    allow_redirects=True
                                    )
            response.raise_for_status()
            return response.content
        except requests.exceptions.HTTPError as http_err:
            if response.status_code in [404, 530]:
                break
        except requests.exceptions.Timeout:
            print("Error: The request timed out.")
            break
        except Exception as e:
            print(e)


def get_redirecting_url(url: str) -> str:
    try:
        resp = requests.head(url, allow_redirects=True, proxies=PROXY)
        return resp.url
    except Exception as e:
        print(e)
        return url


def get_similarweb_info(url: str) -> dict:
    try:
        similarweb_info = fetch(
            "http://data.similarweb.com/api/v1/data?domain=" + url.split("//")[1].replace("www.", ""))
        similarweb_info = json.loads(similarweb_info or "{}")
        return similarweb_info
    except BaseException as e:
        print(e)
        return {}


def s3_save_data(page_text, s3_filepath, response) -> bool:
    if not page_text:
        return False
    for ft in FREE_TRIAL_LIST:
        if ft in page_text:
            s3_bucket.upload_to_s3(s3_filepath, response)
            return True
    s3_bucket.upload_to_s3(f"others/{s3_filepath}", response)
    return False


def is_free_trial(page_text):
    if not page_text:
        return None
    for ft in FREE_TRIAL_LIST:
        if ft in page_text:
            return True
    return False


def process_one_domain(domain: str) -> dict[str, str]:
    try:
        default_result = COLUMNS_DOMAIN_INFO.copy()
        default_result['Root Domain'] = domain['root_domain']
        url = "http://" + domain['root_domain'] if not 'http' in domain['root_domain'] else domain['root_domain']

        netloc_domain = urlparse(url).netloc.replace("www.", "")
        s3_filepath = f"{netloc_domain.split('.')[1]}/{netloc_domain}"
        print(s3_filepath)

        url = get_redirecting_url(url)
        redirecting_url = url if domain['root_domain'] != url else None
        response = fetch(url)

        if not response and IS_RENDER_PAGE:
            response = render_page(
                url,
                proxy={
                    "server": "usa.rotating.proxyrack.net:9000",
                    'username': 'bendover',
                    "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
                }
            )
            if not response:
                return default_result

        similarweb_info = get_similarweb_info(url)

        parser = LexborHTMLParser(str(response))
        tree = parser.css('a')
        result = [element.attributes for element in tree]
        result_filtered = set(t['href'] for t in result if t and 'href' in t and t['href']
                              and ('pric' in t['href']
                              or 'purchase' in t['href'] or 'plans' in t['href'] or "pricing" in str(t))
                              or {})
        result_filtered = result_filtered if result_filtered else None
        if not result_filtered and IS_RENDER_PAGE:
            content = render_page(
                url,
                proxy={
                    "server": "usa.rotating.proxyrack.net:9000",
                    'username': 'bendover',
                    "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
                }
            )
            parser = LexborHTMLParser(content)
            tree = parser.css('a')
            result = [element.attributes for element in tree]
            result_filtered = set(t['href'] for t in result if t and 'href' in t and t['href']
                                  and ('pric' in t['href']
                                       or 'purchase' in t['href'] or 'plans' in t['href'] or "pricing" in str(t))
                                  or {})
            result_filtered = result_filtered if result_filtered else None

        subscription_list = ["per month", "month free", "subscribe", "/mo", "per unit", "per year", "/  mo"]
        is_free_trial, is_subscription = False, False
        try:
            html_cleanup = parser.text()
            for p in CLEANSING_SYMBOLS:
                html_cleanup = html_cleanup.replace(p, "").strip()

            page_text = html_cleanup.lower()
            is_free_trial = s3_save_data(html_cleanup, f"{s3_filepath}/main.html", str(response)[2:-1])
            if not is_free_trial and IS_RENDER_PAGE:
                content = render_page(
                    url,
                    proxy={
                        "server": "usa.rotating.proxyrack.net:9000",
                        'username': 'bendover',
                        "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
                    }
                )
                is_free_trial = s3_save_data(content, f"{s3_filepath}/main.html", content)

            if result_filtered:
                for sub in subscription_list:
                    if sub in page_text:
                        is_subscription = True
                        break

        except Exception as e:
            print(e)

        is_free_trial_price_page, page_text = None, None
        price_urls = []
        if result_filtered:
            for n, p_url in enumerate(list(result_filtered)[:5:-1]):
                if len(p_url) > 20:
                    continue
                continue_flag = False
                for cm in ['instagram', 'pinterest', 'twitter', 'fb.', 'discord']:
                    if cm in p_url:
                        continue_flag = True
                        break
                if continue_flag:
                    continue
                sep_sl = "/" if "/" != p_url[0] and url[-1] != "/" else ""
                price_url = 'http://' + netloc_domain + sep_sl + p_url if not 'http' in p_url else p_url
                price_urls.append(price_url)
                print(price_url)
                response = fetch(price_url)
                if not response:
                    continue

                parser = LexborHTMLParser(str(response))
                html_cleanup = parser.text()
                for p in CLEANSING_SYMBOLS:
                    html_cleanup = html_cleanup.replace(p, "").strip()

                page_text = html_cleanup.lower()
                is_free_trial_price_page = s3_save_data(page_text, f"{s3_filepath}/price.html", str(response)[2:-1])
                if not is_free_trial_price_page and IS_RENDER_PAGE:
                    content = render_page(
                        url,
                        proxy={
                            "server": "usa.rotating.proxyrack.net:9000",
                            'username': 'bendover',
                            "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
                        }
                    )
                    is_free_trial_price_page = s3_save_data(content, f"{s3_filepath}/price.html", content)

                for sub in subscription_list:
                    if sub in page_text:
                        is_subscription = True
                        break
                if is_free_trial_price_page:
                    break

        if result_filtered:
            stat.update({'s_status': stat.get('s_status') + 1})

        return {
            'Root Domain': domain['root_domain'],
            'price link': ",\n".join(price_urls) if price_urls else None,
            "subscription": is_subscription,
            "free trial": is_free_trial,
            "free trial price page": is_free_trial_price_page,
            "redirecting_url": redirecting_url,
            "status": "done",

            'Global Rank': similarweb_info.get('GlobalRank', {}).get('Rank'),
            'Traffic Sources Social': similarweb_info.get('TrafficSources', {}).get('Social'),
            'Traffic Sources Paid Referrals': similarweb_info.get('TrafficSources', {}).get('Paid Referrals'),
            'Traffic Sources Mail': similarweb_info.get('TrafficSources', {}).get('Mail'),
            'Traffic Sources Referrals': similarweb_info.get('TrafficSources', {}).get('Referrals'),
            'Traffic Sources Search': similarweb_info.get('TrafficSources', {}).get('Search'),
            'Traffic Sources Direct': similarweb_info.get('TrafficSources', {}).get('Direct'),
            'Category': similarweb_info.get("Category", None),
            'Top Keywords': str(similarweb_info.get('TopKeywords', None)),
            'Snapshot Date': similarweb_info.get('SnapshotDate', None),
            'Engagements Page Per Visit': similarweb_info.get('Engagments', {}).get('PagePerVisit'),
            'Engagements Visits': similarweb_info.get('Engagments', {}).get('Visits'),
            'Engagements Time On Site': similarweb_info.get('Engagments', {}).get('TimeOnSite'),
            'Engagements Bounce Rate': similarweb_info.get('Engagments', {}).get('BounceRate'),
            # 'TopCountryShares': similarweb_info.get('TopCountryShares', None),
        }
    except Exception as e:
        print(traceback.format_exc())
        return default_result


def get_domain_from_db(chunk_size):
    try:
        with PSQLConnector(**CREDS) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT root_domain FROM public.{DB_TABLE_NAME} WHERE status is NULL LIMIT {chunk_size}")
            domains = cursor.fetchall()
        return domains
    except Exception as e:
        print(traceback.format_exc())
        return domains


def save_db(result):
    for r in result:
        fields = ','.join(r.keys()).lower().replace(" ", "_")
        with PSQLConnector(**CREDS) as conn:
            result = write_to_db(
                conn,
                [list(r.values())], f'public.{DB_TABLE_NAME} ({fields})',
                confl_st=ON_CONFLICT
            )


def run_process():
    # df = pd.read_csv("files/domains_ai_3200.csv")
    # df = pd.read_csv("files/domain_co_1k.csv")
    # df = pd.read_csv("files/similarweb_zero.csv")
    # domains = df.to_dict(orient='records')[:300]

    # stat.update({'count': len(domains)})

    while True:
        domains = get_domain_from_db(chunk_size=1000)
        if not domains:
            break
        pool = Pool(200)
        res = pool.map(process_one_domain, domains)
        pool.close()
        pool.join()

        save_db(res)
        # saving

    # df = pd.DataFrame([r for r in res if r])
    # df.to_excel("files/first_test_ai.xlsx", engine='xlsxwriter')
    # df.to_csv("files/test14_ai_plwr.csv", index=False)
    # print(stat.data['s_status'])


if __name__ == '__main__':
    time_start = time.time()
    run_process()
    print(time.time() - time_start)
