# encoding: utf-8

"""A set of Python 3 function annotation tools supporting Python 2.4 and up.

* Non-declarative syntax.  (Decorators or annotations.)
* No i18n.
* Zero docstrings; comments in Chinese.
* Single monolithic file.
* README is only documentation.
* Estimates: 310 SLoC…
"""

from __future__ import unicode_literals

from boxmongodb import boxmongodb


# From the readme.  (Copy/pasted.  Really.)

class mongoMyAnBox_counter(boxmongodb.Model):
	username = boxmongodb.StringProperty()
	num      = boxmongodb.IntegerProperty(default="1")


def main():
		a = "CcdjhMarx"
		b    = "1984"
		m = mongoMyAnBox_counter(username=a,num=b)
		m.insert()


# Provides

[  # all support 'default'
	'boxmongodb.StringProperty',
	'boxmongodb.DateTimeProperty',  # auto_now
	'boxmongodb.IntegerProperty',
	'boxmongodb.LinkProperty',
	'boxmongodb.AuthProperty',  # never, ever use this (defaults to unixts+sample(10)+sample(10) alnum!)
	'boxmongodb.DictProperty',
	'boxmongodb.EmailProperty'
]
