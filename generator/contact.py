# -*- coding: utf-8 -*-
from model.contact import Contact
import random
import string
import os.path
import jsonpickle
import getopt
import sys

# из документации python -> import getopt, sys
# как читать опции командной строки
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of groups", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 3
f = "data/contacts.json"
#  o, a -пары значений, картежи размерности 2
#  название опции и ее значение(строка), если значение опции  -n , количество групп,берем и преобразуем в число
for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " " * 10
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


def random_phone(prefix, maxlen):
    symbols = string.digits + " +-()"
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata = [
    Contact(firstname=firstname, lastname=lastname, middlename=random_string("middlename", 20),
            nickname=random_string("nickname", 10), company=random_string("company", 20),
            address=random_string("address", 20), homepage=random_string("homepage", 10),
            email2=random_string("email2", 10), address2=random_string("address2", 20),
            email=random_string("email", 20), homephone=random_phone("homephone", 10),
            mobilephone=random_phone("mobilephone", 10), workphone=random_phone("workphone", 10),
            secondaryphone=random_phone("secondaryphone", 10))
    for firstname in ["", random_string("firstname", 10)]
    for lastname in ["", random_string("lastname", 20)]]


file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)
with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(testdata))






