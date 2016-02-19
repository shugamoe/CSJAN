#CHALK CRAWLER

import requests
from robobrowser import RoboBrowser
import getpass

url = 'https://chalk.uchicago.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1/'

username = input('enter username: ')
password = getpass.getpass('enter password: ')


browser = RoboBrowser(history = True)
browser.open(url)
login_form = browser.get_form(action='/webapps/login/')
login_form['user_id'] = username
login_form['password'] = password
browser.session.headers['Referer'] = url
browser.submit_form(login_form)
print(str(browser.select('title')))

