import re
from math import log2

def get_password_strength(password):
    '''
    Return strength of the given password in scale from 1 to 10.
    to be scored as 10 password must be 12 chars and have lowercase,
    upercase, digits and special characters  
    
    >>> get_password_strength('!@23wvHG(F7y')
    10
    >>> get_password_strength('!@23wvHG')
    7
    >>> get_password_strength('1234567890')
    4
    >>> get_password_strength('QWER')
    2
    >>> get_password_strength('186')
    1
    '''
    all_chars_count = {
                       '[a-z]': 26,
                       '[A-Z]': 26,
                       '\d': 10,
                       '\W|_': 32
                      }    
    variations = 0
    for chars_type in all_chars_count.items():
        if bool(re.search(chars_type[0], password)):
            variations += chars_type[1]
             
    password_entropy = log2(variations) * len(password)
    
    strength = round(password_entropy / 8)
    
    if strength < 1:
        strength = 1
    if strength > 10:
        strength = 10
    return strength


if __name__ == '__main__':
    import doctest
    doctest.testmod()
