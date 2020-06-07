#===================================================================

# Autocompletion of AllState applications
# made by selena zhang

#===================================================================

# Preparing this script for final upload to EML servers
    # 1) Search for "::: UPDATE PATHS HERE :::" and do so
    # 2) Search for "::: TO BE UNCOMMENTED :::" and do so
    # 3) Search for "::: TO BE DELETED :::" and do so

#===================================================================

# Import packages
import os
import time
import string
import random
import datetime
import numpy as np
import pandas as pd
from uszipcode import SearchEngine
from fake_useragent import UserAgent

# Import selenium modules
from selenium import webdriver
from pyvirtualdisplay import Display
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as chropopt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

# Import robot movements
from auto_functions import *

#===================================================================

## ::: UPDATE PATHS HERE :::##
browser_path = '/Users/selena_zhang/Desktop/randres'
resume_path  = '/Users/selena_zhang/Desktop/randres/input'
submit_path  = '/Users/selena_zhang/Desktop/randres/output'
error_path   = '/Users/selena_zhang/Desktop/randres/output'

#===================================================================
# Robot for Allstate
#===================================================================

def submit_allstate(details, testing = True):
    try:
        # Initialize chrome options
        chrome_options = chropopt()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--no-sanbdox")
        chrome_options.add_argument("--window-size=1200x900")

        # Path to chrome binary file & Virtual display options
        if (testing == False):
            ua = UserAgent().random
            display = Display(visible=0, size=(1200, 900))
            display.start()
            chrome_options.add_argument('--user-agent="{}"'.format(ua))
            chrome_options.binary_location = '/accounts/projects/pkline/randres/chrome/opt/google/chrome/chrome'

        # browser = webdriver.Chrome(browser_path, options=chrome_options)
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        browser.set_window_size(1300, 800)


        # Big picture options
        firm = details['raw_name']
        app_id = details['id']

        ### 0) Go to URL
        browser.get(details['link'])
        browser.set_window_size(1200, 900)
        try:
            wait_visible((By.XPATH, "//strong[contains(text(), 'Sorry, this position has been filled')]"), browser)

            if (testing == False):
                browser.quit()
                display.sendstop()
            return (details['id'], details['job_id'],)
        except: print("Job exists")

        ### 1) Create an account
        wait_visible((By.PARTIAL_LINK_TEXT,'Apply now'), browser)
        click_at(browser.find_element_by_partial_link_text('Apply now'), browser)
        click_link_by_text('Create an account', browser)

        # Add details
        det_list = [('userName',    details['email']),
                    ('emailConf',   details['email']),
                    ('pwd',         'Pastafarianism!1'),
                    ('pwdConf',     'Pastafarianism!1'),
                    ('fName',       details['firstname']),
                    ('lName',       details['lastname']),]

        for det in det_list:
            scroll_fill("//input[contains(@name, '{}')]".format(det[0]), det[1], browser)

        # Country
        opts = browser.find_elements_by_xpath("//select[@aria-label='Country/Region of Residence']//option")
        opts[-1].click()
        time.sleep(3)
        # Updates
        browser.find_element_by_xpath("//label[contains(text(), 'Receive new job posting')]").click()
        time.sleep(1)

        # Terms
        click_link_by_text("Read and accept the data", browser)
        wait_visible((By.XPATH, "//button[text()='Accept']"), browser)
        time.sleep(3)
        click_at(browser.find_element_by_xpath("//button[text()='Accept']/parent::span"), browser)

        #Create account
        time.sleep(3)
        scroll(browser.find_element_by_xpath("//button[contains(text(), 'Create')]"), browser)
        browser.find_element_by_xpath("//button[contains(text(), 'Create')]").click()
        #click_displayed("//button[contains(text(), 'Create')]", browser)

        # Log in instead if necessary
        try:
            wait_visible((By.XPATH, "//button[contains(text(),'Sign In')]"), browser)
            browser.find_element_by_xpath("//button[contains(text(),'Sign In')]").click()
            for det in [('username', details['email']),('password', 'Pastafarianism!1')]:
                scroll_fill("//input[contains(@name, '{}')]".format(det[0]), det[1], browser)
            browser.find_element_by_xpath("//button[contains(text(),'Sign In')]").click()
            print("Had to log in")
        except: print("Able to create account")

        # If already applied say that
        try:
            wait_visible((By.XPATH, "//div[contains(text(), 'You already applied for this position')]"), browser)
            element = browser.find_element_by_tag_name('body')
            element.screenshot(submit_path + "/{}_app{}_page_submit.png".format(firm,app_id))

            if (testing == False):
                browser.quit()
                display.sendstop()
            return None
        except: pass

        # # except statement
        # try:
        #     wait_visible((By.XPATH, "//div[contains(text(), 'Data Privacy Consent')]"), browser)
        #     browser.find_element_by_xpath("//*[text()='Accept']").click()
        # except:
        #     print("No data privacy consent")

        ### 2) Provide details
        # Expand all sections
        wait_visible((By.XPATH, "//a[contains(text(), 'Expand all sections')]"), browser)
        browser.find_elements_by_xpath("//a[contains(text(), 'Expand all sections')]")[-1].click()

        ##::::: UNCOMMENT HERE BY USING REAL RESUME FILE ::::" "
        # pdf_name = "/{}_{}_{}.pdf".format(details['firm'],details['firstname'],details['lastname'])
        pdf_name = '/resume.pdf'.format('resume')

        try:
            wait_displayed("//span[contains(@class,'trash')]", browser)
            #click_displayed("//a[@title='resume.pdf']", browser)
            #wait_displayed((By.XPATH, "//*[contains(text()='{}')]".format(pdf_name)), browser)
            #wait_visible((By.XPATH, "//*[contains(text()='{}')]".format(pdf_name)), browser)
            print("Resume already uploaded")
        except:
            wait_visible((By.XPATH, "//*[text()='Upload a Resume']"), browser)
            browser.find_element_by_xpath("//*[text()='Upload a Resume']").click()
            time.sleep(2)
            el = browser.find_element_by_xpath("//input[@type='file']")
            el.send_keys(resume_path + pdf_name)

        # # Fill in information
        det_list = [('firstName',   details['firstname']),
                    ('lastName',    details['lastname']),
                    ('cellPhone',   str(details['phone'])),
                    ('address',     string.capwords(details['addy'])),
                    ('city',        string.capwords(details['city'])),
                    ('zip',         "{:05d}".format(details['zipcode'])),]

        for det in det_list:
            scroll_fill("//input[contains(@name, '{}')]".format(det[0]), det[1], browser)

        browser.find_element_by_xpath("//input[contains(@name, 'homePhone')]").clear()

        # Select state
        opts = browser.find_elements_by_xpath("//select[@name='state']//option")
        for op in opts:
            if op.text == states[details['state']]:
                op.click()
                break

        # Delete any existing job and education
        deletes = [k for k in browser.find_elements_by_xpath("//div[@title='Delete Row']") if k.is_displayed()]
        while len(deletes) > 0:
            deletes[0].click()
            time.sleep(3)
            deletes = [k for k in browser.find_elements_by_xpath("//div[@title='Delete Row']") if k.is_displayed()]

        # Add back in job history
        for idx, h in enumerate(details['hist']):
            time.sleep(2)
            add = browser.find_elements_by_xpath("//font[contains(text(), ' Add')]/parent::div")
            #add = [k for k in browser.find_elements_by_xpath("//button[text()='Add new row']") if k.is_displayed()]
            add[0].click()
            time.sleep(3)

            current_emp = browser.find_elements_by_xpath("//label[text()='Present Employer']")[idx]
            current_emp = current_emp.find_elements_by_xpath("parent::div//option")
            if idx == 0:
                current_emp[-1].click()
            else:
                current_emp[1].click()

            # Start date / end date
            stdate = browser.find_elements_by_xpath("//label[text()='Start Date']")[idx]
            stdate = stdate.find_element_by_xpath("parent::div//input")
            stm, sty = h['start'].split("/")
            fill_simple(stdate, "{:02d}/01/{}".format(int(stm),sty), browser)

            if idx > 0:
                stdate = browser.find_elements_by_xpath("//label[text()='End Date']")[idx]
                stdate = stdate.find_element_by_xpath("parent::div//input")
                stm, sty = h['end'].split("/")
                fill_simple(stdate, "{:02d}/01/{}".format(int(stm),sty), browser)

            # Name and position
            scroll_fill("//label[text()='Company Name']/parent::div//input", str_format(h['name']), browser, idx)
            scroll_fill("//label[text()='Title']/parent::div//input", str_format(h['position']), browser, idx)


        #adding education rows
        add = browser.find_elements_by_xpath("//font[contains(text(), ' Add')]/parent::div")
        add[1].click()
        time.sleep(5)
        ###Education
        # #high School
        #name
        scroll_fill("//label[text()='Name Of lnstitution/University']/parent::div//input", str_format(details['schl_name']), browser)
        time.sleep(2)

        #qualification-highest level
        qual = browser.find_elements_by_xpath("//label[text()='Qualification - Highest Level Completed']//parent::div//option")
        qual[5].click()

        #major/course title
        major = browser.find_elements_by_xpath("//label[text()='Major/Course Title']//parent::div//option")
        #to click other
        major[-7].click()
        #START/END DATE
        stdate = browser.find_elements_by_xpath("//label[text()='From Date']")[0]
        stdate = stdate.find_element_by_xpath("parent::div//input")
        stdate.clear()
        fill_simple(stdate, "09/01/{}".format(details['grad_year']-4), browser)
        stdate = browser.find_elements_by_xpath("//label[text()='Completion Date']")[0]
        stdate = stdate.find_element_by_xpath("parent::div//input")
        stdate.clear()
        #stm, sty = 'grad_year'.split("/")
        fill_simple(stdate, "06/30/{}".format(details['grad_year']), browser)

        #college******
        if details['col_name'] is not None:
            add[1].click()
            time.sleep(2)
            #name
            col_row = browser.find_elements_by_xpath("//label[text()='Name Of lnstitution/University']//following-sibling::div[1]//input")
            scroll_fill_element(col_row[1], str_format(details['col_name']), browser)
            time.sleep(2)

            #qualification-highest level
            qual = browser.find_elements_by_xpath("//label[text()='Qualification - Highest Level Completed']//parent::div//option")
            if details['bachelors'] == 0:
                qual[11].click()
            elif details['backelors'] == 1:
                qual[12].click()
            #major/course title

            ### SCRATCH
            # xp_major = "//label[text()='Major/Course Title']/following-sibling::div//select/option[contains(text(),'Other')]"
            # el = browser.find_elements_by_xpath(xp_major)
            # len(el)
            #
            # scroll_xpath("//label[text()='Major/Course Title']//parent::div//option", browser)
            #
            # el = find_displayed(xp_major, browser)
            # len(el)
            #
            major = browser.find_elements_by_xpath("//label[text()='Major/Course Title']//parent::div//option")
            major[-7].click()
            #START/END DATE
            stdate = browser.find_elements_by_xpath("//label[text()='From Date']")[1]
            stdate = stdate.find_element_by_xpath("parent::div//input")
            stdate.clear()
            fill_simple(stdate, "09/01/{}".format(details['grad_year']-4), browser)
            stdate = browser.find_elements_by_xpath("//label[text()='Completion Date']")[1]
            stdate = stdate.find_element_by_xpath("parent::div//input")
            stdate.clear()
            stm, sty = h['end'].split("/")
            fill_simple(stdate, "06/30/{}".format(details['grad_year']), browser)

        # Job specific questions
        try:
            curr_work = browser.find_elements_by_xpath("//label[text()='Are you legally authorized to work in the United States']//following-sibling::div//option")
            curr_work[1].click()
        except: pass

        try:
            curr_sponsor = browser.find_elements_by_xpath("//label[text()='Do you now, or will you in the future, require employment sponsorship (e.g., H-1B visa status) to work legally for Allstate in the United States']//following-sibling::div//option")
            curr_sponsor[-1].click()
        except: pass
        try:
            curr_agent = browser.find_elements_by_xpath("//label[text()='Have you worked as an Allstate employee or Allstate agent previously']//following-sibling::div//option")
            curr_agent[-1].click()
        except: pass

        # try:
        #     how_hear = browser.find_elements_by_xpath("//label[text()='How did you hear about this position?']/parent::div//option")
        #     how_hear[2].click()
        # except:
        #     pass
        #mandatory annual compensation expectation

        try:
            hourly_rate    = random.choice( [12, 12.5, 13] )
            hours_per_week = random.choice( [35, 40] )
            annual_salary  = 52*hours_per_week*hourly_rate
            annual_salary  = str( int( round(annual_salary, -2) ) )

            comp_expect = browser.find_element_by_xpath("//label[text()='Annual Compensation Expectations']//following-sibling::div//input")
            scroll_fill_element(comp_expect, str_format(annual_salary), browser)
            time.sleep(5)
        except: pass

        # Disability if mandatory
        # try:
        #     curr_work = browser.find_elements_by_xpath("//label[contains(text(), 'Please check one of the boxes belo')]/parent::div//option")
        #     curr_work[-1].click()
        #     scroll_fill("//label[text()='Your Name']/parent::div//input", details['firstname'] + ' ' + details['lastname'], browser)
        #     fill_simple(browser.find_element_by_xpath("//label[contains(text(), 's Date')]/parent::div//input"),
        #         datetime.datetime.today().strftime("%m/%d/%Y"), browser)
        # except:
        #     print("No disability")
        #
        # self-identification
        try:
            for el in browser.find_elements_by_xpath("//label[text()='Based on this definition, choose the correct selection']//following-sibling::div//option"):
                scroll(el, browser)
                if "Not Willing" in el.text:
                    el.click()
                    time.sleep(3)
                if 'Not willing' in el.text:
                    el.click()
                    time.sleep(3)
        except: pass

        #pre-screening job-specific
        try:
            highest_edu = browser.find_elements_by_xpath("//label[contains(text(), 'What is the highest level of education you have completed')]/parent::div//input[@type='radio']")
            scroll(highest_edu, browser)
            highest_edu[1].click()
        except: pass

        # try:
        #     salary = browser.find_element_by_xpath("//label[contains(text(), 'What are your salary requirement')]/parent::div//textarea")
        #     scroll(salary, broswer)
        #     fill_simple(salary, np.random.choice(['12 per hour or more', 'at least 12', '12+', '12 but negotiable', 'negotiable',
        #                     'can negotiate', '12 or more', 'flexible', 'can be flexible', 'perfer 12 or more', 'open to discussion',
        #                     'can discuss', 'willing to discuss', 'willing to negotiate']), browser)
        # except:
        #     print("No salary")

        try:
            for i in browser.find_element_by_xpath("//label[contains(text(), 'How many years of estimating experience')]/parent::div//textarea"):
                scroll(i, broswer)
                fill_simple(i, '0', browser)
        except: pass

        try:
            for b in browser.find_element_by_xpath("//label[contains(text(), 'How many years')]/parent::div//[@type='radio']"):
                scroll(b, browser)
                b[0].click()
        except: pass

        try:
            est_apps = browser.find_element_by_xpath("//label[contains(text(), 'What are your salary requirement')]/parent::div//textarea")
            scroll(est_apps, broswer)
            fill_simple(est_apps, np.random.choice(['none', "None", "N/A", "Don't have any experience"]), browser)
        except: pass

        # Signature
        opts = browser.find_elements_by_xpath("//label[contains(text(), 'Typed Signature')]/parent::font//child::input")

        try:
            for sign in browser.find_elements_by_xpath("//label[contains(text(), 'Typed Signature')]/parent::font//child::input"):
                scroll_fill_element(sign,
                        str_format(details['firstname'] + ' ' + details['lastname']), browser)
            # stdate = browser.find_element_by_xpath("//label[text()='Application Date']/parent::div//input")
            # stdate.clear()
            # fill_simple(stdate, datetime.datetime.today().strftime("%m/%d/%Y"), browser)
        except:
            print("No signing")

        # Pre-screening questions, if necessary
        try:
            xp_strong = "//label[contains(text(),'demonstrates a strong customer')]//following-sibling::div//textarea"
            text = "I have assisted customers with dignity and professionalism."
            text1 = "Please see my resume for more information."
            text2 = "In the past, I have held numerous customer service backgrounds and would be able to bring those experiences to this job"
            fill_in_xpath(xp_strong, np.random.choice([text, text1, text2]), browser)
        except:
            pass

        #highest level of education
        try:
            highest_edu = browser.find_element_by_xpath("//label[contains(text(), 'What is the highest level of education you have completed?')]//following-sibling::div") #//input[@type='radio']
            scroll(highest_edu, browser)
            if details['col_name'] is None:
                hschool = browser.find_element_by_xpath("//label[contains(text(), 'A high school degree')]//parent::span")
                hschool.click()
            elif details['bachelors'] == 0:
                hschool = browser.find_element_by_xpath("//label[contains(text(), 'A two-year associate')]//parent::span")
                hschool.click()
            elif details['bachelors'] == 1:
                hschool = browser.find_element_by_xpath("//label[contains(text(), 'A four-year bachelor')]//parent::span")
                hschool.click()
        except:
            pass

        #facilitating
        try:
            facilitatingl = browser.find_element_by_xpath("//label[contains(text(), 'Do you have experience facilitating live training')]//following-sibling::div")
            scroll(facilitatingl, browser)
            answerl = browser.find_elements_by_xpath("//label[contains(text(), 'No')]")
            answerl[2].click()
        except:
            pass

        try:
            facilitatingv = browser.find_element_by_xpath("//label[contains(text(), 'Do you have experience facilitating virtual training/learning')]//following-sibling::div")
            scroll(facilitatingv, browser)
            answerv = browser.find_elements_by_xpath("//label[contains(text(), 'No')]")
            answerv[3].click()
        except:
            pass

        try:
            life_license = browser.find_element_by_xpath("//label[contains(text(), 'Do you currently hold a Life')]//following-sibling::div")
            scroll(life_license, browser)
            license = browser.find_elements_by_xpath("//label[contains(text(), 'No')]")
            license[4].click()
        except:
            pass

        try:
            property_license = browser.find_element_by_xpath("//label[contains(text(), 'Do you currently hold a Property')]//following-sibling::div")
            scroll(property_license, browser)
            prop_license = browser.find_elements_by_xpath("//label[contains(text(), 'No')]")
            prop_license[5].click()
        except:
            pass

        if (testing == False):

            # Click apply
            time.sleep(3);      browser.find_element_by_xpath("//span[text()='Apply']").click()
            try: time.sleep(3); browser.find_element_by_xpath("//span[text()='Apply']").click()
            except: pass

            try: time.sleep(3); click_at(browser.find_element_by_xpath("//span[text()='Apply']"), browser)
            except: pass

            # Final confirmation
            wait_visible((By.XPATH, "//div[contains(text(), 'Your application has been sent')]"), browser)

            element = browser.find_element_by_tag_name('body')
            element.screenshot(submit_path + "/{}_app{}_page_submit.png".format(firm,app_id))

            # Close window
            browser.quit()
            display.sendstop()
            return None

    except Exception as e:
        print("Automation error for {} {} job {} {} {}: {}".format(details['firstname'], details['lastname'],
                    details['firm'], details['city'], details['state'], e))
        try:
            element = browser.find_element_by_tag_name('body')
            element.screenshot(error_path + "/{}_app{}_error.png".format(firm,app_id))

            if (testing == False):
                browser.quit()
                display.sendstop()
        except:
            print("Couldn't print error screen")
        print('\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a')


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  DEBUGGING (::: TO BE DELETED :::)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Initialize chrome options
chrome_options = chropopt()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--no-sanbdox")
chrome_options.add_argument("--window-size=1200x900")
# browser = webdriver.Chrome(browser_path, options=chrome_options)
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
browser.set_window_size(1300, 800)


# Job links
link1 = 'https://careers.allstate.com/job/Rochester-Claims-Service-Specialist-NY-14602/629765600/?feedId=268800&utm_source=ExternalCS&utm_campaign=Allstate_Jobs&_ga=2.224365528.292007944.1581316525-1650229725.1580785125'
link2 = 'https://careers.allstate.com/job/Wall-Township-Inside-Liability-Adjuster-NJ/621797800/?feedId=268800&utm_source=ExternalCS&utm_campaign=Allstate_Jobs&_ga=2.238865987.292007944.1581316525-1650229725.1580785125'
link3 = 'https://careers.allstate.com/job/Overland-Park-Liability-Claims-Service-Specialist-KS-66062/623391100/?feedId=268800&utm_source=ExternalCS&utm_campaign=Allstate_Jobs&_ga=2.71870035.1327985946.1582334792-1587605256.1582334792'
stalelink4 = 'https://careers.allstate.com/job/Charlotte-Entry-Level-Inside-Property-Adjuster-NC-28201/625579900/?feedId=268800&utm_source=ExternalCS&utm_campaign=Allstate_Jobs&_ga=2.142927606.292007944.1581316525-1650229725.1580785125'

# Links tested by Ross
test_link = 'https://careers.allstate.com/job/Irving-Commercial-Liability-Claims-Associate-TX-75014/631343700/?feedId=268800&utm_source=ExternalCS&utm_campaign=Allstate_Jobs&_ga=2.190038690.808347356.1582336817-2054715373.1582336817'


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  TESTING  (::: TO BE DELETED :::)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Running the robot
details = details_example
details['link'] = test_link
details['email'] = 'asdf23@mt2015.com'
submit_allstate(details, testing = True)
