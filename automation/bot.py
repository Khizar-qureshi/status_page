import json
import time
from fake_useragent import UserAgent
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ECimport 
from selenium.webdriver.support import expected_conditions as EC
import pdb
from utils.constants import Login, Time

def setup_driver():
    """
    Set up and return the Selenium WebDriver with undetected_chromedriver and fake user-agent.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-background-timer-throttling")  # Keep browser active
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument("--start-maximized")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options)
    return driver
# def setup_driver():
#     return webdriver.Chrome()

def save_cookies(driver, filename):
    """
    Save cookies from the current browser session to a file.
    """
    cookies = driver.get_cookies()
    with open(filename, "w") as file:
        json.dump(cookies, file)
    print(f"Cookies saved to {filename}")

def load_login_cookies(driver, filename):
    """
    Load cookies from a file into the browser session.
    """
    with open(filename, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    print(f"Cookies loaded from {filename}")

def login_and_store_cookies(driver):
    """
    Log in to LinkedIn and store session cookies.
    """
    driver.get(Login.link)
    Time.sleep()  # Wait for the login page to load

    # Perform login
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    email_field.send_keys("your_email@example.com")
    password_field.send_keys("your_password")
    password_field.send_keys(Keys.RETURN)
    Time.sleep()  # Wait for the login page to load

def login_to_game(driver):
    driver.get(Login.link)

    username = driver.find_element(By.ID, 'userName')
    username.send_keys(Login.username)

    signupcode = driver.find_element(By.ID, 'password')
    signupcode.send_keys(Login.password)

    submit = driver.find_element(By.ID, 'loginButton')
    submit.click()
    time.sleep(2)

    login_block = driver.find_element(By.ID, 'accountLink')
    if Login.username in login_block.text:
        print("Login created successfully")
    else:
        print("Invalid login")

def find_first_move(driver):
    squares = driver.find_elements(By.XPATH, "//div[contains(@class, 'square')]")
    print(f"Number of squares found: {len(squares)}")

    for square in squares:
        ActionChains(driver).move_to_element(square).perform()
        background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');", square)
        print(background_color)
        if background_color == "rgb(169, 169, 169)" or background_color == "rgb(105, 105, 105)":
            print(f"Square: {square.get_attribute('class')}, Background color: {background_color}")
            target_square = get_drag_location(driver, square)
            return square, target_square
    return None, None

def get_drag_location(driver, start_square):
    squares = driver.find_elements(By.XPATH, "//div[contains(@class, 'square')]")
    for square in squares:
        background_color = driver.execute_script(
            "return window.getComputedStyle(arguments[0]).getPropertyValue('background-color');", square
        )
        print(f"Square: {square.get_attribute('class')}, Background color: {background_color}")
        if (background_color == "rgb(105, 105, 105)" or background_color == "rgb(169, 169, 169)") and start_square != square:
            print("Found draging location")
            return square
    return None

def make_random_move(driver):
    start_square, target_square = find_first_move(driver)
    if start_square == None or target_square == None:
        print("No possible moves found!")
    else:
        print("dragging")
        ActionChains(driver).drag_and_drop(start_square, target_square).perform()
        print("Move performed!")
        return True
    return False

def check_login_status():
    driver = setup_driver()
    login_to_game(driver)
    try:
        driver.get("http://onemovechess-web.northcentralus.cloudapp.azure.com/Chess")
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "chessBoard")))
            print("Chessboard Found")
            time.sleep(1)
            player_to_move = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/main/h2")))
            print(player_to_move.text)
            new_board_assigned = True
            while new_board_assigned:
                make_random_move(driver)
                print("starting in 30 seconds")
                time.sleep(30)
        except:
            print("Chess Board not found")
        pdb.set_trace()
    finally:
        driver.quit()

check_login_status()