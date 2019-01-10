import re
import sys
from math import log2
import getpass
import requests


def check_slavonic_family_names(password):

    name_pattern = re.compile(r'[A-z]+(ov|ich|ko|ev|in|ik|uk|off)')
    return re.sub(name_pattern, 'n', password)


def check_phones(password):

    return re.sub(r'''(\+\d{1,3})?           # international code from 1 to 3 digits
                        [-]?                 # posible -
                        \(?                  # posible (
                        (\d{1,3}?)?          # domestic code from 1 to 3 digits
                        \)?                  # posible )
                        [-]?                 # posible -
                        (\d{1,3})            # 3 digits
                        [-]?                 # posible -
                        (\d{2})              # 2 digits
                        [-]?                 # posible -
                        (\d{2}               # 2 digits
                        )''', 'p', password, flags=re.X)


def check_dates(password):

    date_pattern = re.compile(r'''(([\d]{2})                  # day - two digitals
                                  (\W|_)?                     # possible ' ' or _
                                  ([A-z]{3}|[\d]{2})             # month - 3 letters or 2 digits
                                  (\W|_)?                     # possible ' ' or _
                                  (19|20)([\d]{2}))           # year
                                  |                           # or
                                  (([A-z]{3}|[\d]{2})            # month - 3 letters or 2 digits
                                  (\W|_)?                     # possible ' ' or _
                                  ([\d]{2})                   # day - two digits
                                  (\W|_)?                     # possible ' ' or _
                                  (19|20)([\d]{2}))           # year
                                  ''', re.X)
    return re.sub(date_pattern, 'd', password)


def check_repetitions(password):

    pattern = re.compile(r"(.+?)\1+")
    index = 1
    repeated = re.findall(pattern, password)
    for repeat in repeated:
        split = password.split(repeat)
        split.insert(index, repeat)
        res = ''
        for occurrence in split:
            res += occurrence
        password = res

    return password


def get_blacklist_from_url(url):

    try:
        blacklist_req = requests.get(url)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        return None
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
        return None

    acceptable_status_code = 200
    if blacklist_req.status_code <= acceptable_status_code:
        return str(blacklist_req.text)
    else:
        return None


def check_blacklist(password, blacklist):

    if not password or not blacklist:
        return None

    if password in blacklist:
        password = 'b'

    return password


def get_password_strength(password):

    if not password:
        return None

    blacklist_url = \
        'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/darkweb2017-top10000.txt'
    password = check_blacklist(password, get_blacklist_from_url(blacklist_url))

    checks = (
        check_dates,
        check_slavonic_family_names,
        check_phones,
        check_repetitions
               )

    for check in checks:
        password = check(password)

    all_chars_count = {
        '[a-z]': 26,
        '[A-Z]': 26,
        '\d': 10,
        '\W|_': 32
    }
    variations = 0
    for chars_group in all_chars_count.items():
        if bool(re.search(chars_group[0], password)):
            variations += chars_group[1]

    password_entropy = log2(variations) * len(password)

    score_tuning = 8

    strength = round(password_entropy / score_tuning)

    min_strength, max_strength = 1, 10
    strength = max(min(max_strength, strength), min_strength)

    return strength


def get_user_password():
    try:
        password = getpass.getpass()

    except Exception as err:
        print('ERROR:', err)
    else:
        return password

if __name__ == '__main__':

    password = get_user_password()

    print(get_password_strength(password))

