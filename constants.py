import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())



PROXY_STR = os.environ.get("PROXY_STR")
PROXY = {'https': f'http://{PROXY_STR}', "http": f'http://{PROXY_STR}'}
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,uk;q=0.8',
    'cache-control': 'no-cache',
    # 'cookie': '_gcl_au=1.1.1010159567.1724770427; _clck=lrwzqr%7C2%7Cfoo%7C0%7C1700; cb_user_id=null; cb_group_id=null; cb_anonymous_id=%22f8875f00-4a92-4498-aa04-a424c565a61e%22; _ga=GA1.2.1592189722.1724770430; _gid=GA1.2.236360123.1724770430; _rdt_uuid=1724770427500.6c7841e7-a3d0-45ff-94c8-49bb4ac0d16a; _ga_7KED85T4TT=GS1.2.1724770434.1.1.1724770434.60.0.0; crisp-client%2Fsession%2F6dd7f3c7-8e09-4be5-80a6-16366dc30236=session_6b7be75a-3790-4064-ab36-123fa069cd53; _clsk=pe8tmv%7C1724771605840%7C2%7C1%7Ci.clarity.ms%2Fcollect; ph_phc_wCT090Bolq5W9i3L1HXv5a5HfRcRN6ZRIgMTiLqTCGP_posthog=%7B%22distinct_id%22%3A%2201919454-218b-7b1f-9bbf-327289243d56%22%2C%22%24sesid%22%3A%5B1724771614782%2C%2201919454-2189-7b19-9d50-16b18fc18086%22%2C1724770427273%5D%7D',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': '',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
PROXY_PLAYWRIGHT = {
    "server": "usa.rotating.proxyrack.net:9000",
    'username': 'bendover',
    "password": 'BGWBZRO-1TBG9O0-RA2SHGQ-9CSG6E4-J7QI9QB-OPGMX8P-B9ECWBX',
}

COLUMNS_DOMAIN_INFO = {
    'Root Domain': None,
    # 'verified_data ICP': None,
    # 'verified_data Free trial': None,
    'price link': None,
    "subscription": None,
    "free trial": None,
    "free trial price page": None,
    "redirecting_url": None,
    "status": "not_done",
    # traffic
    'Global Rank': None,
    'Traffic Sources Social': None,
    'Traffic Sources Paid Referrals': None,
    'Traffic Sources Mail': None,
    'Traffic Sources Referrals': None,
    'Traffic Sources Search': None,
    'Traffic Sources Direct': None,
    'Category': None,
    'Top Keywords': None,
    'Snapshot Date': None,
    'Engagements Page Per Visit': None,
    'Engagements Visits': None,
    'Engagements Time On Site': None,
    'Engagements Bounce Rate': None,


    # 'TopCountryShares': None,
}

CLEANSING_SYMBOLS = [
    "\n",
    "\\n",
    "\\\n",
    "\\\\n",
    "\t",
    "\\t",
    "\\\t",
    "\\\\t",
    "\r",
    "\\r",
    "\\\r",
    "\\\\r",
]

FREE_TRIAL_LIST = ["free trial", "started for free", "month free", "$0/mo", "start for free", "days for free",
                   "try for free", "sign up free", "try now for free", "try it free", "days free trial",
                   "started free", "day trial", "days trial", "start trial",  # "for free"
                   "days cancel policy", "try free for 30 days", "try free for 7 days"
                   ]
SUBSCRIPTION_LIST = [
    "per month", "month free", "subscribe", "/mo", "per unit", "per year", "/  mo", "/ mo", "/ day", "/  day"
]