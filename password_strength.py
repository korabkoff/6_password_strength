import argparse
import re
import sys
from math import log2

# filter sequences
def filter_sequence(password, sequence):
    """
    >>> filter_sequence('1234567890', '1234567890')
    's'
    >>> filter_sequence('$654', '0987654321')
    '$s'
    >>> filter_sequence('rtyuw', 'qwertyuiop')
    'sw'
    >>> filter_sequence('', 'qwertyuiop')
    ''
    >>> filter_sequence('4567', '')
    '4567'
    """
    seq = ''
    del_last = False

    for char_idx in range(len(password) - 1):
        char = password[char_idx]
        next_char = password[char_idx + 1]
        if char in sequence:
            current_sequence_char_index = sequence.index(char)
            next_sequence_char = sequence[current_sequence_char_index + 1]
            #                 print ('match ')
            if next_sequence_char == next_char:  # if match
                if del_last:
                    seq = seq[:-1]
                # print ('match next chars')
                seq += str(char) + str(next_char)
                del_last = True

            else:  # if end of sequence
                del_last = False

                if seq and len(sequence) > 2:
                    password = password.replace(seq, 's')
                seq = ''
                #                     print ('end of seq')
        else:
            pass
        # print ('no match ')

        if seq and char_idx == len(password) - 2:
            password = password.replace(seq, 's')
            seq = ''
        # print ('Last char ')

        # print(password, len(seq), seq, char_idx, len(password) - 2)

    return password
def filter_sequences(password):
    """
    >>> filter_sequences('1234567890')
    's'
    >>> filter_sequences('$654')
    '$s'
    >>> filter_sequences('rtyuw')
    'sw'
    >>> filter_sequences('qwerty123456')
    'ss'
    """
    sequences = ('1234567890','0987654321','qwertyuiop','asdfghjkl','zxcvbnm')
    for seq in sequences:
        password = filter_sequence(password, seq)
    return password

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
    >>> filter_phones('+375-29-6-82-63-23')
    'p'
    >>> filter_phones('+375296826323')
    'p'
    >>> filter_phones('6826323')
    'p'
    """
    return (re.sub(r'(\+\d{1,3}?)?[-]?\(?(\d{1,3}?)?\)?[-]?(\d{3})[-]?(\d{2})[-]?(\d{2})', 'p', password))

def filter_dates(password):
    date_pattern = re.compile(r'(([\d]{2})(\W|_)?((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)|[\d])(\W|_)?(19|20)([\d]{2}))|(([a-z]{3})(\W|_)?([\d]{2})(\W|_)?(19|20)([\d]{2}))', flags=re.IGNORECASE)
    return (re.sub(date_pattern, 'd', password))

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

    repeated = re.findall(pattern, password)
    for repeat in repeated:
        split = password.split(repeat)
        split.insert(1, repeat)
        res = ''
        for i in split:
            res += i
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
     lowercase, numeric and special characters. Script filter pasword for balck
     list, repetitions,common family names, phones, dates

    >>> get_password_strength('!PassworD1')
    2
    >>> get_password_strength('1234567890')
    1
    >>> get_password_strength('qwerty')
    1
    >>> get_password_strength('qwertyqwertyqwertyqwerty')
    1
    >>> get_password_strength('TvF^%KB6euEb$')
    10
    >>> get_password_strength('lowercaseonly')
    5
    >>> get_password_strength('169258761168')
    2
    >>> get_password_strength('TvF^%K')
    5
    >>> get_password_strength('korabkoff')
    1
    >>> get_password_strength('PassworD')
    1
    >>> get_password_strength('03may1981')
    1
    >>> get_password_strength('+375296826672')
    1
    """

    filters = (blacklist_filter,filter_dates, filter_names, filter_phones,
               filter_repetitions,filter_sequences)

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
