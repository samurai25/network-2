import os
import pathlib
import unittest
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service 


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 


service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


#driver.get("http://127.0.0.1:8000/admin/")

#username = driver.find_element(By.ID, "id_username")
#password = driver.find_element(By.ID, "id_password")
#login = driver.find_element(By.XPATH, "//input[@type='submit']")
#username.send_keys("sasha")
#password.send_keys(1)
#login.click()

#driver.get("http://127.0.0.1:8000/login")
#username = driver.find_element(By.NAME, "username")
#password = driver.find_element(By.NAME, "password")
#login = driver.find_element(By.XPATH, "//input[@type='submit']")
#username.send_keys("Sasha")
#password.send_keys(1)
#login.click()

#text = driver.find_element(By.ID, "id_post")
#text.send_keys("TEST")
#post = driver.find_element(By.XPATH, "//input[@value='Post']")
#post.click()

# like a post
#wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
#button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button')))
#button.click() 


#time.sleep(2)
# dislike a post
#wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
#button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button')))
#button.click()

# Profile page
#profile = driver.find_element(By.CLASS_NAME, 'nav-link')
#profile.click()

# Following page
#following = driver.find_element(By.XPATH, '//a[contains(text(), "Following")]')
#following.click()


# Test Follow button click
#wait = WebDriverWait(driver, 10)
#profile = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@value="Test"]')))
#profile.click()

#follow_button = driver.find_element(By.ID, 'follow_button')
#time.sleep(2)
#follow_button.click()

#time.sleep(2)

#wait = WebDriverWait(driver, 10)
#profile = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@value="Test"]')))
#profile.click()

#follow_button = driver.find_element(By.ID, 'follow_button')
#time.sleep(2)
#follow_button.click()

# Test Next page click   
#next_btn = driver.find_element(By.XPATH, '//a[contains(text(), "Next")]')
#next_btn.click()

# Test Previous page click
#time.sleep(2)
#previous_btn = driver.find_element(By.XPATH, '//a[contains(text(), "Previous")]')
#previous_btn.click()
        
        
class WebpageTests(unittest.TestCase):

    def test_title(self):
        """Make sure title is correct"""
        driver.get("http://127.0.0.1:8000/")
        self.assertEqual(driver.title, "Social Network")
        
        
    def test_login(self):
        """Login is correct"""
        driver.get("http://127.0.0.1:8000/login")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        login = driver.find_element(By.XPATH, "//input[@type='submit']")
        username.send_keys("Sasha")
        password.send_keys(1)
        login.click()
        
        wait = WebDriverWait(driver, 10)
        profile = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="profile"]')))
        self.assertEqual(profile.get_attribute('value'), "Sasha")
        
    ####################################  
    def test_new_post(self):
        """New post is created"""

        # Create a new post
        text = driver.find_element(By.ID, "id_post")
        text.send_keys("Hello, world!")
        post = driver.find_element(By.XPATH, "//input[@value='Post']")
        post.click()
        
        wait = WebDriverWait(driver, 10)
        p = wait.until(EC.visibility_of_element_located((By.XPATH, "//p")))
        self.assertEqual(p.text, "Hello, world!")
        

        # Like a Post
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.visibility_of_element_located((By.XPATH, '//button')))
        button.click()
        wait = WebDriverWait(driver, 10)
        like = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '1')]")))
        
        self.assertEqual(like.text, "1")
        
        time.sleep(2)
    

        # Dislike a Post
        wait2 = WebDriverWait(driver, 10)
        button2 = wait2.until(EC.visibility_of_element_located((By.XPATH, '//button')))
        button2.click()
        wait2 = WebDriverWait(driver, 10)
        dislike = wait2.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '0')]")))
        
        self.assertEqual(dislike.text, "0")
        
        time.sleep(2)
         
        # Test follow button 
        driver.get("http://127.0.0.1:8000/user_profile/Sasha2/")
              
        wait = WebDriverWait(driver, 10)
        follow_button = wait.until(EC.visibility_of_element_located((By.ID, 'follow_button')))
        time.sleep(2)
        follow_button.click()
        
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/user_profile/Sasha2/")
        time.sleep(2)

        b = driver.find_element(By.XPATH, "//input[@value='Unfollow']")
        self.assertEqual(b.get_attribute('value'), "Unfollow")

    
    
    def test_following_page(self):
        # Test Following Page
        driver.get("http://127.0.0.1:8000/following")
        wait = WebDriverWait(driver, 10)
        h2 = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'h2'))) 
        self.assertEqual(h2.text, "Following")

    def test_profile_page(self):
        # Test Following Page
        driver.get("http://127.0.0.1:8000/profile")
        wait = WebDriverWait(driver, 10)
        span = wait.until(EC.visibility_of_element_located((By.TAG_NAME, 'span'))) 
        self.assertEqual(span.text, "Sasha")
        
    def test_user_profile_page(self):
        driver.get("http://127.0.0.1:8000/user_profile/Sasha2/")
        
        

        
    def tear_down(self):
        driver.close()
        driver.quit()

         
if __name__ == "__main__":
    unittest.main()
    
    
