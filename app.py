from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

# Set up the ChromeDriver service
service = Service("C:/webdriver/chromedriver.exe")  # Use forward slashes or double backslashes for the path

# Initialize WebDriver using the Service
driver = webdriver.Chrome(service=service)

# Open WhatsApp Web
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code
print("Please scan the QR code and press Enter to continue...")
input()

# Specify the contact or group name where you'll receive the "Activate" message
contact_name = 'Dazzal David'  # Replace with the contact name or number

# Locate the search box and find the contact
search_box_xpath = '//div[@contenteditable="true"][@data-tab="3"]'
search_box = driver.find_element(By.XPATH, search_box_xpath)
search_box.send_keys(contact_name)
search_box.send_keys(Keys.RETURN)

def get_last_message():
    # Adjust the XPath if needed based on WhatsApp Web's structure
    messages_xpath = "//div[contains(@class, 'message-in')]//span[contains(@class, 'selectable-text')]"
    messages = driver.find_elements(By.XPATH, messages_xpath)
    return messages[-1].text if messages else ''

def send_message(message):
    try:
        # Set up WebDriverWait for the message input box
        wait = WebDriverWait(driver, 30)
        # Wait for the input box to be present
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')))
        inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p'
        input_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, inp_xpath))
        )
        # Ensure the input box is focused
        input_box.click()  # Click to focus
        time.sleep(1)  # Wait a moment to ensure focus

        # Send the message
        input_box.send_keys(message)
        input_box.send_keys(Keys.RETURN)
        time.sleep(10)  # Wait to ensure message is sent
    except Exception as e:
        print(f"Error sending message: {e}")
        driver.quit()


last_processed_message = ""


# Continuously monitor the chat for the "Activate" message
while True:
    last_message = get_last_message().strip().lower()
    print(f"Last message received: {last_message}")  # Debug output

    if last_message == 'activate' and last_message != last_processed_message:
        print("Activating the script...")
        send_message('The Script will Run Now')
        subprocess.Popen(['python', 'run.py'])  # Trigger your script
        last_processed_message = last_message  # Update the last processed message

    elif last_message == 'debug' and last_message != last_processed_message:
        send_message('Hii How are you')
        last_processed_message = last_message  # Update the last processed message

    elif last_message == 'exit' and last_message != last_processed_message:
        send_message('Ending The Machine')
        last_processed_message = last_message  # Update the last processed message
        break

    time.sleep(10)  # Check every 10 seconds

# Close the browser when done
driver.quit()
