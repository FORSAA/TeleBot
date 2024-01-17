from imports.BrowserInteractionClass_import_all import *

class BrowserInteraction():
    @staticmethod
    def login_to_account(login: str, password: str, browser: webdriver.Chrome):
        browser.get("https://e-school.obr.lenreg.ru/authorize/login")
        browser.implicitly_wait(20)

        school_name_selection = browser.find_element(By.CLASS_NAME, "select2__button")
        login_box = browser.find_element(By.NAME, "loginname")
        password_box = browser.find_element(By.NAME, "password")
        login_button = browser.find_element(By.CLASS_NAME, "primary-button")

        school_name_selection.click()
        school_name_input = browser.find_element(By.CLASS_NAME, "select2-search__field")
        school_name_input.send_keys('МОБУ "СОШ "ЦО "Кудрово"')
        browser.find_elements(By.CLASS_NAME, "org-name-data")[1].click()

        login_box.send_keys(login)
        password_box.send_keys(password)

        login_button.click()

    @staticmethod
    def do_after_login_process(browser: webdriver.Chrome):
        continue_button = browser.find_element(By.XPATH, "//button[@title='Продолжить']")
        continue_button.click()
        if (not browser.current_url.endswith('/studentdiary/')):
            browser.get('https://e-school.obr.lenreg.ru/angular/school/studentdiary/')
        sleep(3)

    @staticmethod
    def log_out(browser: webdriver.Chrome):
        browser.find_element(By.XPATH, "//a[@href='JavaScript:Logout(true);']").click()
        sleep(0.7)
        browser.find_element(By.XPATH, "//button[@class='btn btn-primary']").click()

    @staticmethod
    def get_exercises(browser: webdriver.Chrome, is_photo: bool, date_offset: int) -> str:
        date_with_offset = get_date(date_offset)

        exercises_table = browser.find_element(By.XPATH, f"//span[contains(., '{date_with_offset}')]").find_element(
            By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
        exercises_rows = exercises_table.find_elements(By.XPATH, ".//tr[@class='ng-scope']")

        if not is_photo:
            rows = []
            print(f'DEBUG | INFO | GETTING ROWS AND FORMATTING STRINGS.')
            for row in exercises_rows:
                rows.append([row.text])
            return_string = f'\n'
            for item in rows:
                item_text = '\n'.join(item)
                item_text = item_text.split('\n')
                lesson_number = item_text[0]
                subject = item_text[1]
                time_and_room = item_text[2]
                task = item_text[3] if len(item_text)>3 else ""
                formatted_item = f"Урок №{lesson_number}: Предмет: {subject}\nВремя/Кабинет: {time_and_room}\nЗадание: {task}\n\n {'='*40}\n\n"
                return_string += formatted_item
            return return_string
        else:
            if (exercises_table.screenshot(os.getcwd()+r'\screenshots\Homework_Screenshot.png')):
                print(f'DEBUG | INFO | OPENING AND RETURNING SCREENSHOT FILE.')
                return 'screenshot'
            else:
                print(f'DEBUG | INFO | SCREENSHOT ERROR. RETURNING.')
                return 'screenshot_error'

    @staticmethod
    def get_homework(auth_data: dict, is_photo: bool, date_offset: int) -> str:
        login, password = auth_data.values()

        browser_options = Options()

        # browser_options.add_argument("--headless=new")
        browser_options.add_argument("--window-size=1000,2000")

        browser = webdriver.Chrome(options=browser_options)

        print(f'DEBUG | INFO | OPENING BROWSER. . .')

        browser.implicitly_wait(5)

        try:
            print(f'DEBUG | INFO | LOGGINING. . .')
            BrowserInteraction.login_to_account(login, password, browser)

        except NoSuchElementException:
            print(f'DEBUG | ERROR | LOGIN ERROR. GETTING BACK.')
            return 'login_error'

        sleep(1.2)
        if (browser.current_url.endswith('SecurityWarning.asp')):
            BrowserInteraction.do_after_login_process(browser)

        return_data: str = BrowserInteraction.get_exercises(browser, is_photo, date_offset)

        BrowserInteraction.log_out(browser)

        browser.close()

        return return_data


if __name__ == '__main__':
    BrowserInteraction.get_homework({'login':'ЗахаровЕ9', 'password':'5084433'}, False, 0)