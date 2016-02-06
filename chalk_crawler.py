#CHALK CRAWLER

from lxml import html
import requests
import urllib3
import getpass

url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1'

username = input('enter username: ')
password = getpass.getpass('enter password: ')

pool_man = urllib3.PoolManager()
pool_man.headers['username'] = username
pool_man.headers['password'] = password

r = pool_man.urlopen('GET', url)
page = r.read()

print(page)
