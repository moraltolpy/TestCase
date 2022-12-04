import os

from selenium import webdriver


def before_all(context):
    if os.getenv('CI', False):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        context.browser = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_options)
    else:
        context.browser = webdriver.Firefox(executable_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'geckodriver'))
        # context.browser = webdriver.Chrome('features/chromedriver')
    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'


def before_scenario(context, scenario):
    from django.contrib.auth.models import User
    User.objects.all().delete()


def after_all(context):
    context.browser.quit()
