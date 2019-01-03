# Password Strength Calculator

This script return password strength score from 1 to 10 where 10
is most secure one. To score 10 password must be 13 characters long
with upper and lowercase, numbers and special characters.
There is a filter for most common passwords, repetitions,
common family names and dates.
# How to run

script require python3.5 Example of script launch on Linux, Python 3.5:
```#!bash
$ python password_strength.py <password> # possibly requires call of python3 executive instead of just python

$ python password_strength.py PassworD!
>>> 2
$ python password_strength.py TvF^%KB6euEb$
>>> 10
$ python password_strength.py TvF^%K
>>> 5

```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
