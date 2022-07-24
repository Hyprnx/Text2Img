import logging

from base import BaseClass
from common.database_connect import connect_to_database

import selenium
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

from common.get_webdriver import get_selenium_chrome_webdriver_path
from credentials.chrome_user_data import user_data_path  # create a folder name credentials and paste your Chrome
                                                        # user data path there
def clone_database(db_name):
    db_name = db_name.lower()
    if db_name in db.list_collection_names():
        db[db_name].drop()
    db[db_name].insert_many(db['news'].find({}))
    logging.info(f'Successfully cloned {db_name}')

db = connect_to_database()
clone_database('temp')
db = db.temp


class Automation(BaseClass):
    def __init__(self, headless=False):
        super().__init__()
        try:
            self.log.info("Setting options, initializing Selenium...")
            options = Options()
            prefs = {"profile.default_content_setting_values.notifications": 2}
            options.headless = headless
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("detach", True)
            user_data_option = "user-data-dir=" + user_data_path
            options.add_argument(user_data_option)
            service = Service(get_selenium_chrome_webdriver_path())
            self.driver = Chrome(service=service, options=options)
            user_agent = self.driver.execute_script("return navigator.userAgent;")
            self.log.info(f"Current User Agent is:{user_agent}")
        except BaseException as e:
            self.log.critical(e)
            self.log.info('Initialize failed, aborting')
            self.driver.quit()

    def get_text(self):
        documents_count = db.count_documents({"source": "vnexpress"})
        for i in range(documents_count):
            res = db.find_one()
            db.delete_one({"_id": res['_id']})
            yield res['title'], res['body']


if __name__ == '__main__':
    def test():
        documents_count = db.count_documents({"source": "vnexpress"})
        for i in range(documents_count):
            res = db.find_one()
            db.delete_one({"_id": res['_id']})
            yield res['title'], res['body']


    for title, body in test():
        print(f"{title=}, \n{body=}")
