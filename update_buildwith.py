import datetime
import requests
import sys


sys.path.append('../')
# from managers.dbs_manag import PsqlManagment
# from managers.notifications import slack_notifications

api_key = '503fb9c8-bcf0-431f-b006-4e210c45a320'
api_key = '83be39c7-80d5-49ea-8133-b2f90a375653'
source = 'Google'
request_link = f'https://api.builtwith.com/lists7/api.json?KEY={api_key}&TECH={source}&META=yes&SINCE=yesterday '
request_link = f'https://api.builtwith.com/lists7/api.json?KEY={api_key}&TECH={source}&META=no' # &ALL=true
# offset = ''


def get_domain_list_from_api():
    unique_domain = set()
    offset = ''

    for try_count in range(101):
        domains = []
        print(request_link + offset)
        res = requests.get(request_link + offset)
        if res.status_code == 200:
            api_results = res.json()['Results']
            for item in api_results:
                domain = item['D']
                first_detected = str(datetime.datetime.fromtimestamp(item['FD']).date()) if item['FD'] else None
                domains = (domain, str(datetime.datetime.now().date()), first_detected)
                unique_domain.add(domains)

            if res.json()['NextOffset'] != 'END':
                offset = '&OFFSET=' + res.json()['NextOffset']
                # update_postgres()
                yield unique_domain
                unique_domain = set()
            else:
                yield domains
                unique_domain = set()
                # update_postgres()
                break

        else:
            if try_count > 95:
                pass
                # slack_notifications('error', message='cant update builwith',
                #                     data={'reason': f'response status code: {res.status_code}'})
            if try_count == 100:
                break


def get_domains():
    try:
        offset_str = ''
        offset_num = 0
        while True:
            domains = set()
            print(request_link + offset_str)
            response = requests.get(request_link + offset_str)
            if response.status_code == 200:
                api_results = response.json()['Results']
                for item in api_results:
                    domain = item['D']
                    first_detected = str(datetime.datetime.fromtimestamp(item['FD']).date()) if item['FD'] else None
                    domains.add(domain)

                if response.json()['NextOffset'] != 'END':
                    offset = '&OFFSET=' + response.json()['NextOffset']
                    print(offset)
                # offset_num = offset_num + len(domains)
                # offset_str = f"&OFFSET={offset_num}"

                yield domains

    except Exception as e:
        print(e)


def update_postgres():
    pass
    # PsqlManagment().write_to_db(list(unique_domain), f"""buildwith_domains ("Domain", date_added, "First Detected")""",
    #                             confl_st=f"""on conflict ("Domain") do NOTHING""")
    #

def update_buildwith():
    get_domain_list_from_api()


if __name__ == '__main__':
    for r in get_domains():
        print(r)