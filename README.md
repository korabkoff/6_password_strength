# Password Strength Calculator

This script return password strength score from 1 to 10 where 10
is most secure one. To score 10 password must be 13 characters long
with upper and lowercase, numbers and special characters.
There is a filter for most common passwords, repetitions,
common family names and dates.
Script is require the blacklist of widely used passwords to check if
given password doesn't have match. You can download one the latest
compilation from here:
https://github.com/danielmiessler/SecLists/tree/master/Passwords

# How to run

script require python3.5 Example of script launch on Linux, Python 3.5:
```#!bash
$ python password_strength.py <blacklist_path> # possibly requires call of python3 executive instead of just python
Password: <password>

$ python password_strength.py  brut_force_dict.list
>>> Password: password
>>> 1
$ python password_strength.py brut_force_dict.list
>>> Password: TvF^%KB6euEb$
>>> 10
$ python password_strength.py brut_force_dict.list
>>> Password: TvF^%K
>>> 5

```
You can not see password while typing it in console cause it's more secure

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
