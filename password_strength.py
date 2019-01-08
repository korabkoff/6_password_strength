import re
import sys
from math import log2
import getpass
import requests


def check_slavonic_family_names(password):
    """
    Replace common slavonic family names with 'n'

    >>> check_slavonic_family_names('korabkoff')
    'n'
    >>> check_slavonic_family_names('Ivanov')
    'n'
    >>> check_slavonic_family_names('Kovalenko')
    'n'
    """
    name_pattern = re.compile(r'[A-z]+(ov|ich|ko|ev|in|ik|uk|off)')
    return re.sub(name_pattern, 'n', password)


def check_phones(password):
    """
    Replace phones with 'p'

    >>> check_phones('+375-29-682-63-23')
    'p'
    >>> check_phones('+12(429)6826423')
    'p'
    >>> check_phones('6826323')
    'p'
    """
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
    """
    Replace dates with 'd'

    >>> check_dates('03 may 1981')
    'd'
    >>> check_dates('03_MAY_1981')
    'd'
    >>> check_dates('03051981')
    'd'
    """

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
    """
    Replace repetitions with 'r'


    >>> check_repetitions('677767776e')
    '67776e'
    >>> check_repetitions('e11111^')
    'e1^'
    >>> check_repetitions('e123123123o5454')
    'e123o54'
    """
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
    """
    Return text from given url request.

    >>> get_blacklist_from_url('http://wrong_address.txt')
    >>> blacklist_url = 'https://raw.githubusercontent.com/korabkoff/6_password_strength/master/brut_force_dict.list'
    >>> get_blacklist_from_url(blacklist_url)
    'password\\n123123\\n'
    """

    try:
        blacklist_req = requests.get(url)
    except:
        return None
    asseptable_status_code = 200
    if blacklist_req.status_code <= asseptable_status_code:
        return str(blacklist_req.text)
    else:
        return None


def check_blacklist(password, blacklist):
    """
    Replace blacklisted password with 'b' based on provided blacklist.

    >>> blacklist_url = 'https://raw.githubusercontent.com/korabkoff/6_password_strength/master/brut_force_dict.list'
    >>> check_blacklist('password', (get_blacklist_from_url(blacklist_url)))
    'b'
    >>> check_blacklist('qzwxec', (get_blacklist_from_url(blacklist_url)))
    'qzwxec'
    >>> check_blacklist(None, None)

    >>> check_blacklist('', (get_blacklist_from_url(blacklist_url)))

    """
    if not password or not blacklist:
        return None

    if password in blacklist:
        password = 'b'

    return password


def get_password_strength(password):
    """
    Return strength of a given password scoring from 1 to 10 where 10 is most secure one.

    To get maximum score 10 password must be 13 chars long and have upper case,
    lowercase, numeric and special characters. Script check password if in black
    list, have repetitions, common family names, phones, dates and replace it with 'b',
    'r', 'n', 'p', 'd' respectively and then get the score.

    >>> get_password_strength('b')
    1
    >>> get_password_strength('password')
    1
    >>> get_password_strength('maxmaxmaxmaxmax')
    2
    >>> get_password_strength('TvF^%KB6euEb$')
    10
    >>> get_password_strength('TvF^%K')
    5
    >>> get_password_strength('korabkoff')
    1
    >>> get_password_strength('03may1981')
    1
    >>> get_password_strength('+375-29-682-66-72')
    1
    >>> get_password_strength(None)

    """
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

