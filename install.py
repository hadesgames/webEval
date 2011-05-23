#!/usr/bin/env python2

import os
import shutil
import sys

if os.path.isdir('install') is False:
	print "I can't find directory install, quiting"
	exit(0)

os.chdir('install')

try:
	import setuptools
	print "Setup tools found, continuing"
except:
	print "Cannot find setuptools, please install python-setuptools"
	exit(0)

def install (short_name, name):
    print "Okay, i will try to install %s" % name
    shutil.copy('%s.makefile' % short_name, 'Makefile')
    if os.system("make") != 0:
    	exit(0)
    else:
    	print "Succesfully installed %s" % name
		
def install_package(short_name, name):
    if len(sys.argv) > 1 and sys.argv[1] == '-y':
        install(short_name, name)
    else:
      for i in xrange(3):
    	  print "Cannot find %s, do you want me to install it ? [Y/n]" % name,
          input = raw_input()
          if input.lower().find('y') != -1:
              install(short_name)
              break
          elif input.lower().find('n') != -1:
              print "Okay, skipping"
              break
  			
try:
	import django
	print "Django found, continuing"
except:
	install_package('django', 'Django')

try:
	import facebook
	print "Facebook support found, continuing"
except:
	install_package('pyfacebook', 'Facebook support')

try:
	import south
	print "South support found, continuing"
except:
	install_package('south', 'South migration tool')

try:
	import django_extensions
	print "Django extensions found, continuing"
except:
	install_package('django_extensions', 'Django extensions')
	
try:
	import annoying
	print "Django annoying found, continuing"
except:
	install_package('django_annoying', 'Django annoying')

try:
	import MySQLdb
	print "Python MySQL module found, continuing"
except:
	install_package('mysql_python', 'Python MySQL module')
	
try:
	import creoleparser
	print "Creole parser found, continuing"
except:
	install_package('creole_parser', 'Creole parser')
	
try:
	import markdown
	print "Markdown parser found, continuing"
except:
	install_package('markdown', 'Markdown parser')
try:
	import textile
	print "Textile parser found, continuing"
except:
	install_package('textile', 'Textile parser')
try:
	import sqlite3
	print "Python Sqlite3 module found, continuing"
except:
	install_package('sqlite3', 'Python Sqlite3 module')
	
try:
	import captcha
	print "Django simple captcha module found, continuing"
except:
	install_package('simple_captcha', 'Django simple captcha')

try:
	import pygments
	print "Pygments library found, continuing"
except:
	install_package('pygments', 'Pygments library')
	
try:
	import tagging
	print "Tagging library found, continuing"
except:
	install_package('tagging', 'Tagging library')

try:
	import recaptcha
	print "Recaptcha library found, continuing"
except:
	install_package('recaptcha', 'Recaptcha library')
	
try:
	import akismet
	print "Akismet library found, continuing"
except:
	install_package('akismet', 'Akismet library')
	
""" 
try:
	import registration
	print "Django registration found, continuing"
except:
	install_package('registration', 'Django registration')

try:
	import haystack
	print "Haystack found, continuing"
except:
	install_package('haystack', 'Haystack')
"""

try:
	import django_openid_auth
	print "Django openid auth found, continuing"
except ImportError:
	install_package('authopenid', 'Django openid auth')
except:
	pass

try:
	import oauth2
	print "Django oauth found, continuing"
except ImportError:
	install_package('oauth', 'Django oauth')
	
"""
try:
	import piston
	print "Django piston found, continuing"
except ImportError:
	install_package('piston', 'Django piston')
"""
	
try:
	import pagination
	print "Django pagination found, continuing"
except ImportError:
	install_package('pagination', 'Django pagination')
	
try:
	import dateutil
	print "Django dateutil found, continuing"
except ImportError:
	install_package('dateutil', 'Django dateutil')
	
try:
	import Image
	print "Python Image Library found, continuing"
except ImportError:
	install_package('pil', 'Python Image Library')
	
try:
	import simplejson
	print "Simplejson found, continuing"
except ImportError:
	install_package('simplejson', 'Simplejson')
	
try:
	import postmarkup
	print "Postmarkup found, continuing"
except ImportError:
	install_package('postmarkup', 'Postmarkup')
	
try:
	import devserver
	print "Devserver found, continuing"
except ImportError:
	install_package('devserver', 'Devserver')