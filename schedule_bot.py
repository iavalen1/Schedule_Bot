from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

USERNAME = "***"
PASSWORD = "***"
DATES = ["10/5/2020","10/6/2020","10/7/2020","10/8/2020","10/9/2020"]
HOURS = ["07:45 - 11:15","11:45 - 14:45","15:15 - 18:15"]
HOME_URL = ""
LOGIN_URL_SEGMENT = ""
CHROME_PROFILE_DIRECTORY = ""
CHROME_DRIVER_DIRECTORY = ""
DRIVER = None

def main():
    
    # Load schedule page
    DRIVER.get(HOME_URL)

    while(True):
        # Checks if current page is a login page
        if LOGIN_URL_SEGMENT in DRIVER.current_url:
            login()
            time.sleep(10)
        try:
            # Check if all hours claimed
            if all_claimed():
                break
            # Adds any available hours
            if DRIVER.current_url == HOME_URL:
                for date in DATES:
                    for hour in HOURS:
                        if DRIVER.find_elements_by_css_selector('div[id*="%s"]' % date) != []:
                            if available(date,hour):
                                add_hour_block(date,hour)
        
            # Delay
            time.sleep(5)

            # Refesh page
            DRIVER.refresh()
            time.sleep(10)
        except Exception as e:
            print(e)
            # Refesh page
            DRIVER.get(HOME_URL)
            time.sleep(10)

    # Logout
    logout()

def initDriver(profileDirectory, driverDirectory):
    # Load existing chrome profile and set to headless mode
    options = Options()
    options.add_argument(profileDirectory)
    
    # Return chrome driver
    return webdriver.Chrome(executable_path=driverDirectory,chrome_options=options)

def login():
    # Login page
    DRIVER.find_element_by_id("login").send_keys(USERNAME)
    time.sleep(1)
    DRIVER.find_element_by_id("password").send_keys(PASSWORD)
    time.sleep(1)
    DRIVER.find_element_by_name("SubmitButton").click()

def logout():
    # Click dropdown menu
    DRIVER.find_element_by_partial_link_text("").click()
    time.sleep(1)

    # Click log out
    DRIVER.find_element_by_partial_link_text("Sign out").click()
    time.sleep(1)

    # Confirm log outs
    DRIVER.find_elements_by_xpath('//button[.="Yes, sign out"]')[1].click()
    
    
    
def add_hour_block(date,hour):

    date_element = DRIVER.find_element_by_xpath('//*[@id="%s"]' % date)
    containers = date_element.find_elements_by_tag_name("a")
    
    for container in containers:
        if hour in container.text:
            container.click()
            time.sleep(2)
            DRIVER.find_element_by_xpath('//button[text()="Accept"]').click()
            time.sleep(2)
            DRIVER.find_element_by_xpath('//button[text()="Yes, I accept"]').click()
            time.sleep(3)
            DRIVER.find_element_by_xpath('//a[text()="Done"]').click()
            print("Added more hours! %s : %s" % (date,hour))
            time.sleep(10)
            return
			
def available(date,time):

    date_element = DRIVER.find_element_by_xpath('//*[@id="%s"]' % date)

    if not claimed(date,time):
        if time in date_element.text:
            return True

    return False

def claimed(date,time):

    if DRIVER.find_elements_by_css_selector('div[id*="%s"]' % date) != []:
        date_element = DRIVER.find_element_by_css_selector('div[id="%s"]' % date)
        blocks = date_element.find_elements_by_tag_name('div')

        for block in blocks:
            if block.find_elements_by_css_selector('li[class*="claimed"]') != []:
                if block.find_element_by_css_selector('div[class="time-display"]').text == time:
                    return True

    return False

def all_claimed():
    for date in DATES:
        for time in HOURS:
            if not claimed(date,time):
                return False
    
    print("All dates claimed!")
    return True

if __name__ == '__main__':
    DRIVER = initDriver(CHROME_PROFILE_DIRECTORY,CHROME_DRIVER_DIRECTORY)
    main()
    DRIVER.close()
    exit()
