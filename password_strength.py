import argparse
import re
import sys
from math import log2



# Family names
def filter_names(password):
    """
    >>> filter_names('korabkoff')
    'n'
    >>> filter_names('Ivanov')
    'n'
    >>> filter_names('Kovalenko')
    'n'
    """
    name_pattern = re.compile(r'[A-z]+(ov|ich|ko|ev|in|ik|uk|off)')
    return re.sub(name_pattern,'n',password)


 # phone formats
def filter_phones(password):
    """
    >>> filter_phones('+375-29-682-63-23')
    'p'
    >>> filter_phones('+375296826423')
    'p423'
    >>> filter_phones('6826323')
    'p'
    """
    return re.sub(r'(\+\d{1,3}?)?[-]?\(?(\d{1,3}?)?\)?[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})', 'p', password)


def filter_dates(password):
    date_pattern = re.compile(r'(([\d]{2})(\W|_)?((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|[\d])(\W|_)?(19|20)([\d]{2}))|(([a-z]{3})(\W|_)?([\d]{2})(\W|_)?(19|20)([\d]{2}))', flags=re.IGNORECASE)
    return re.sub(date_pattern, 'd', password)


def filter_repetitions(password):
    """
    >>> filter_repetitions('677767776e')
    '67776e'
    >>> filter_repetitions('e11111^')
    'e1^'
    >>> filter_repetitions('e123123123o5454')
    'e123o54'
    """
    pattern = re.compile(r"(.+?)\1+")
    index = 1
    repeated = re.findall(pattern, password)
    for repeat in repeated:
        split = password.split(repeat)
        split.insert(index, repeat)
        res = ''
        for ocurrence in split:
            res += ocurrence
        password = res

    return password
    # return re.sub(pattern, repetiotion, password)


# brut check
def blacklist_filter(password):
    """
    >>> blacklist_filter('!PassworD1')
    '!b1'
    """
    with open('brut_force_dict.list') as blacklist_dict_file:
        blacklist = [row.strip() for row in blacklist_dict_file]

        match = max([re.findall(black_match, password, flags=re.IGNORECASE)
                     for black_match in blacklist])[0]
    if match:
        return re.sub(match, 'b', password)
    return password


def parse_args(args):

    parser = argparse.ArgumentParser(description='Get password strength')
    parser.add_argument('password', help='password')

    return parser.parse_args(args)


def get_password_strength(password):
    """
    To get maximum score 10 password must be 13 chars long and have upper case,
     lowercase, numeric and special characters. Script filter pasword if in black
     list,have repetitions,common family names, phones, dates and replace it with 'b',
      'r', 'n', 'p', 'd' respectivly

    >>> get_password_strength('!PassworD1')
    2
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
    """

    filters = (blacklist_filter,filter_dates, filter_names, filter_phones,
               filter_repetitions)

    for the_filter in filters:
        password = the_filter(password)
        # print(the_filter.__name__ + ': ' + password)

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

    strength = round(password_entropy / 8)

    if strength < 1:
        strength = 1
    if strength > 10:
        strength = 10
    return strength


if __name__ == '__main__':

    try:
        parser = parse_args(sys.argv[1:])

        password = parser.password
    except IOError:
        password = None

    print(get_password_strength(password))

