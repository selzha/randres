#===================================================================

# Autocompletion of Kroger applications
# made by selena zhang

import pandas as pd
import numpy as np
import time
import datetime
import os
import random

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as chropopt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
# ::: UNCOMMENT HERE IF NEEDED :::#
#from pyvirtualdisplay import Display
# #Import fake user agent
# from fake_useragent import UserAgent
# ua = UserAgent().random
import string

from uszipcode import SearchEngine

from auto_functions import *

## ::: UPDATE PATHS HERE :::##
# driver = webdriver.Chrome(ChromeDriverManager().install())
#browser_path = '/Users/selena_zhang/Desktop/randres'
resume_path  = '/Users/selena zhang1/Desktop/randres/input'
submit_path  = '/Users/selena zhang1/Desktop/randres/output'
error_path   = '/Users/selena zhang1/Desktop/randres/output'

hourly_rate    = random.choice( [12, 12.5, 13] )
hours_per_week = random.choice( [35, 40] )
annual_salary  = 52*hours_per_week*hourly_rate
annual_salary  = str( int( round(annual_salary, -2) ) )

def submit_kroger(details):
    try:
        # Big picture opxtions
        firm = details['raw_name']
        app_id = details['id']

        ### 0) Go to URL
        browser.get(details['link'])
        browser.set_window_size(1200, 900)
        try:
            wait_visible((By.XPATH, "//strong[contains(text(), 'Sorry, this position has been filled')]"), browser, delay=15)
            browser.quit()
            display.sendstop()
            #return (details['id'], details['job_id'])
        except:
            print("Job exists")

        ### 1) Create an account
        scroll_click_xp("//button[contains(text(), 'Apply now')]", browser, delay=5)
        time.sleep(10)
        # scroll_click_xp("//*[@id='content']/div/div[2]/div/div[1]/div[1]/div/div/ul/li[3]", browser, delay=3)
        # click_text("Apply Now", browser)

        # wait_visible((By.PARTIAL_LINK_TEXT,'Apply Now'), browser)
        # click_at(browser.find_element_by_partial_link_text('Apply Now'), browser)
        click_link_by_text('Create an account', browser)

        # Add details
        for det in [('userName', details['email']), ('emailConf', details['email']),
            ('pwd', 'Pastafarianism!1'), ('pwdConf', 'Pastafarianism!1'), ('fName', details['firstname']),
                ('lName', details['lastname'])]:
            scroll_fill("//input[contains(@name, '{}')]".format(det[0]), det[1], browser)

        # Country
        opts = browser.find_elements_by_xpath("//select[@aria-label='Country/Region of Residence']//option")
        opts[1].click()
        time.sleep(3)
        # Updates
        browser.find_element_by_xpath("//label[contains(text(), 'Receive new job posting')]").click()
        time.sleep(2)

        # Terms
        click_link_by_text("Read and accept the data", browser)
        wait_visible((By.XPATH, "//button[text()='Accept']"), browser)
        time.sleep(3)
        click_at(browser.find_element_by_xpath("//button[text()='Accept']/parent::span"), browser)

        #Create account
        time.sleep(3)
        scroll(browser.find_element_by_xpath("//button[contains(text(), 'Create')]"), browser)
        browser.find_element_by_xpath("//button[contains(text(), 'Create')]").click()

        # Log in instead if necessary
        try:
            wait_visible((By.XPATH, "//button[contains(text(),'Sign In')]"), browser)
            browser.find_element_by_xpath("//button[contains(text(),'Sign In')]").click()
            for det in [('username', details['email']),('password', 'Pastafarianism!1')]:
                scroll_fill("//input[contains(@name, '{}')]".format(det[0]), det[1], browser)
            browser.find_element_by_xpath("//button[contains(text(),'Sign In')]").click()
            print("Had to log in")
        except:
            print("Able to create account")

        # If already applied say that
        try:
            wait_visible((By.XPATH, "//div[contains(text(), 'You already applied for this position')]"), browser)
            element = browser.find_element_by_tag_name('body')
            element.screenshot(submit_path + "/{}_app{}_page_submit.png".format(firm,app_id))

            # Close window
            # ::::  UNMARK HERE ::::###
            # browser.quit()
            # display.sendstop()
            #return None
        except:
            pass

        ### 2) Provide details
        # Expand all sections
        wait_visible((By.XPATH, "//a[contains(text(), 'Expand all sections')]"), browser)
        browser.find_elements_by_xpath("//a[contains(text(), 'Expand all sections')]")[-1].click()
        ## Upload the resume
        ##:::::UPDATE PDF NAME HERE::::" "
        pdf_name = '{}.pdf'.format('resume')
        #pdf_name = "{}_{}_{}.pdf".format(details['firm'],details['firstname'],details['lastname'])
        try:
            wait_displayed("//span[contains(@class,'trash')]", browser, delay = 1)
            print("Resume already uploaded")
        except:
            wait_visible((By.XPATH, "//*[text()='Upload a Resume']"), browser)
            browser.find_element_by_xpath("//*[text()='Upload a Resume']").click()
            time.sleep(2)
            el = browser.find_element_by_xpath("//input[@type='file']")
                ####::::UPDATE HERE:::#####
            el.send_keys('/Users/selenazhang 1/Desktop/randres/input/resume.pdf') #+ pdf_name)

        # # Fill in information
        for det in [('firstName', details['firstname']), ('lastName', details['lastname']),
            ('cellPhone', str(details['phone'])), ('address', string.capwords(details['addy'])),
            ('city', string.capwords(details['city'])), ('zip',"{:05d}".format(details['zipcode'])),
            ]:
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

        # Add back in job history (by defaut there is already 1 position required)
        for idx, h in enumerate(details['hist']):
            if idx != 0:
                add = browser.find_elements_by_xpath("//div[contains(text(), ' Add')]")
                add[0].click()
                time.sleep(3)

            time.sleep(2)
            current_emp = browser.find_elements_by_xpath("//label[text()='Employer Type']")[idx]
            current_emp = current_emp.find_elements_by_xpath("parent::div//option")
            if idx == 0:
                current_emp[2].click()
            else:
                current_emp[-1].click()

            # Start date / end date
            stdate = browser.find_elements_by_xpath("//label[text()='From Date']")[idx]
            stdate = stdate.find_element_by_xpath("parent::div//input")
            stdate.clear()
            stm, sty = h['start'].split("/")
            fill_simple(stdate, "{:02d}/01/{}".format(int(stm),sty), browser)

            if idx == 0:
                stdate = browser.find_elements_by_xpath("//label[text()='End Date']")[idx]
                stdate = stdate.find_element_by_xpath("parent::div//input")
                #stdate.clear()
            elif idx > 0:
                stdate = browser.find_elements_by_xpath("//label[text()='End Date']")[idx]
                stdate = stdate.find_element_by_xpath("parent::div//input")
                #stdate.clear()
                stm, sty = h['end'].split("/")
                fill_simple(stdate, "{:02d}/01/{}".format(int(stm),sty), browser)
            time.sleep(2)
            #company country
            company_country = browser.find_elements_by_xpath("//label[text()='Company Country']")[idx]
            company_country = company_country.find_elements_by_xpath("parent::div//option")
            company_country[1].click()
            time.sleep(2)
            #company state
            comp_state = browser.find_elements_by_xpath("//label[text()='Company State']")[idx]
            comp_state = comp_state.find_elements_by_xpath("parent::div//option")
            for op in comp_state:
                if op.text == states[h['state']]:
                    op.click()
                    break
            time.sleep(2)
            #position type:
            postype = browser.find_elements_by_xpath("//label[text()='Position Type']")[idx]
            postype = postype.find_elements_by_xpath("parent::div//option")
            postype[1].click()
            time.sleep(2)
            #employment type
            emp_type = browser.find_elements_by_xpath("//label[text()='Employment Type']")[idx]
            emp_type = emp_type.find_elements_by_xpath("parent::div//option")
            emp_type[1].click()
            time.sleep(2)
            #reason for Leaving
            if idx == 0:
                pass 
                # rsnforleaving = browser.find_elements_by_xpath("//label[text()='Reason for Leaving']")[idx]
                # rsnforleaving = rsnforleaving.find_elements_by_xpath("parent::div//option")
                # rsnforleaving[2].click()
            elif idx > 0:
                rsnforleaving = browser.find_elements_by_xpath("//label[text()='Reason for Leaving']")[idx]
                rsnforleaving = rsnforleaving.find_elements_by_xpath("parent::div//option")
                rsnforleaving[1].click()
            time.sleep(2)
            # Name, position details
            scroll_fill("//label[text()='Company Name']/parent::div//input", str_format(h['name']), browser, idx)
            time.sleep(2)
            scroll_fill("//label[text()='Position/Title']/parent::div//input", str_format(h['position']), browser, idx)
            time.sleep(2)
            scroll_fill("//label[text()='Company City']/parent::div//input", str_format(h['city']), browser, idx)
            time.sleep(2)
            scroll_fill("//label[text()='Company Postal Code']/parent::div//input", str(h['zip']), browser, idx)
            time.sleep(2)
            scroll_fill("//label[text()='Company Telephone']/parent::div//input", str(h['phone']), browser, idx)
            time.sleep(2)
            scroll_fill("//label[text()='Reason for Leaving Description']/parent::div//input", str_format(h['whyleave']), browser, idx)
            # may we contact this employer
            maywecontact = browser.find_elements_by_xpath("//label[text()='May we contact this employer?']")[idx]
            maywecontact = maywecontact.find_elements_by_xpath("parent::div//option")
            maywecontact[-1].click()
            time.sleep(2)
        #adding education rows
        add = browser.find_elements_by_xpath("//div[contains(text(), ' Add')]")
        add[1].click()
        time.sleep(3)
        ###Education
        # #high School

        #education type
        qual = browser.find_elements_by_xpath("//label[text()='Education Type']//following-sibling::div//option")
        qual[1].click()

        ## Country
        hscountry = browser.find_elements_by_xpath("//label[text()='Country']//following-sibling::div//option")
        hscountry[1].click()
        time.sleep(2)
        ##city
        scroll_fill("//label[text()='City']//following-sibling::div//input", str_format(details['schl_city']), browser)
        time.sleep(2)
        #name
        #if other, enter school name
        scroll_fill("//label[text()='If other, enter School/Institution Name']//following-sibling::div//child::input", str_format(details['schl_name']), browser)
        time.sleep(2)
        ##state
        hsstate = browser.find_elements_by_xpath("//label[text()='State']//following-sibling::div//option")
        for op in hsstate:
            if op.text == states[details['state']]:
                op.click()
                break
        time.sleep(3)

        #degree status
        deg_stat = browser.find_elements_by_xpath("//label[text()='Degree Status']//following-sibling::div//child::select//child::option")
        deg_stat[3].click()
        time.sleep(2)
        #area of study
        areaofstudy = browser.find_elements_by_xpath("//label[text()='Area of Study']//following-sibling::div//child::select//child::option")
        #high school, NA
        areaofstudy[-1].click()
        time.sleep(2)
        ##they make you choose from a list of preselcted schools
        inst_name_select = browser.find_elements_by_xpath("//label[text()='School/Institution Name']//following-sibling::div//child::select//child::option")
        inst_name_select[-1].click()
        time.sleep(2)

        #college******
        if details['col_name'] is not None:
            add[1].click()
            time.sleep(2)
            #edu type
            try:
                qual = browser.find_elements_by_xpath("//label[text()='Education Type']")[1]
                qual = qual.find_elements_by_xpath("parent::div//option")
                if details['bachelors'] == 0:
                    qual[4].click()
                elif details['bachelors'] == 1:
                    qual[5].click()
            except:
                pass
            time.sleep(2)
        # college country
            try:
                col_country = browser.find_elements_by_xpath("//label[text()='Country']")[1]
                col_country = col_country.find_elements_by_xpath("parent::div//option")
                col_country[1].click()
            except:
                pass
            time.sleep(2)
        # City
            try:
                scroll_fill("//label[text()='City']/parent::div//input", str_format(details['schl_city']), browser, 1)
            except:
                pass
            time.sleep(2)
        # name
            try:
                scroll_fill("//label[text()='If other, enter School/Institution Name']/parent::div//input", str_format(details['col_name']), browser, 1)
            except:
                pass
            time.sleep(2)
        #state
            try:
                col_state = browser.find_elements_by_xpath("//label[text()='State']")[1]
                col_state = col_state.find_elements_by_xpath("parent::div//option")
                for op in col_state:
                    if op.text == states[details['state']]:
                        op.click()
                        break
            except:
                pass
            time.sleep(2)
        #degree Status
            try:
                deg_status = browser.find_elements_by_xpath("//label[text()='Degree Status']")[1]
                deg_status = deg_status.find_elements_by_xpath("parent::div//option")
                deg_status[3].click()
            except:
                pass
        #area of study (drop down)
            try:
                area_of_study = browser.find_elements_by_xpath("//label[text()='Area of Study']")[1]
                area_of_study = area_of_study.find_elements_by_xpath("parent::div//option")
                for op in area_of_study:
                    if op.text == details['major']:
                        op.click()
                        break
                    else:
                        if op.text == "Other":
                            op.click()
                            break
            except:
                pass
        #other - specify
            try:
                scroll_fill("//label[text()='If other, enter Area of Study']/parent::div//input", str_format(details['major']), browser, 1)
            except:
                pass

        #preselected drop down menu
            try:
                schl_menu = browser.find_elements_by_xpath("//label[text()='School/Institution Name']")[1]
                schl_menu = schl_menu.find_elements_by_xpath("parent::div//option")
                schl_menu[-1].click()
            except:
                pass

        ##job-specific information
        #ssn
        try:
            ssn = browser.find_element_by_xpath("//label[text()='Social Security Number']//following-sibling::div//child::input")
            fill_simple(ssn, str(details['social']), browser)
        except:
            pass
        time.sleep(2)
        ##how did you learn
        try:
            learn = browser.find_elements_by_xpath("//label[contains(text(), 'How did you learn')]//following-sibling::div//child::select//child::option")
            learn[-1].click()
        except:
            pass
        time.sleep(2)
        ##currently attending class
        try:
            curr_attend = browser.find_elements_by_xpath("//label[contains(text(), 'Are you currently attending classes')]//following-sibling::div//child::select//child::option")
            curr_attend[-1].click()
        except:
            pass
        time.sleep(2)
        #highest level of education****
        try:
            highest_edu = browser.find_elements_by_xpath("//label[contains(text(), 'What is the highest level of education you have completed?')]//following-sibling::div//child::option")
            if details['col_name'] is None:
                highest_edu[1].click()
            elif details['bachelors'] == 0:
                highest_edu[4].click()
            elif details['bachelors'] == 1:
                highest_edu[5].click()
            time.sleep(2)
        except:
            pass
        ##relatives
        try:
            relatives = browser.find_elements_by_xpath("//label[contains(text(), 'Do you have any relatives')]//following-sibling::div//child::select//child::option")
            relatives[-1].click()
        except:
            pass
        time.sleep(2)
        #military
        try:
            usma = browser.find_elements_by_xpath("//label[contains(text(), 'Have you served in the')]//following-sibling::div//child::select//child::option")
            usma[-1].click()
        except:
            pass
        time.sleep(2)
        #18 or up
        try:
            eighteen = browser.find_elements_by_xpath("//label[contains(text(), 'Are you 18')]//following-sibling::div//child::select//child::option")
            eighteen[1].click()
        except:
            pass
        time.sleep(2)
        #tobacco
        try:
            eighteen = browser.find_elements_by_xpath("//label[contains(text(), 'Have you, or has anyone under your supervision')]//following-sibling::div//child::select//child::option")
            eighteen[-1].click()
        except:
            pass
        time.sleep(2)


        #preferences
        #first choice
        try:
            prefs_1 = browser.find_elements_by_xpath("//label[contains(text(), 'First Choice')]//following-sibling::div//child::select//child::option")
            prefs_1[1].click()
        except:
            pass
        time.sleep(2)
        #second Choice
        try:
            prefs_2 = browser.find_elements_by_xpath("//label[contains(text(), 'Second Choice')]//following-sibling::div//child::select//child::option")
            prefs_2[1].click()
        except:
            pass
        time.sleep(2)
        ##availability
        try:
            startwork = browser.find_element_by_xpath("//label[contains(text(), 'What date are you available to start work?')]//following-sibling::div//child::span//child::input")
            startwork.clear()
            fill_simple(startwork, datetime.datetime.today().strftime("%m/%d/%Y"), browser)
        except:
            pass
        time.sleep(2)
        try:
            evenings = browser.find_elements_by_xpath("//label[contains(text(), 'Are you able and willing to work evenings')]//following-sibling::div//child::option")
            evenings[1].click()
        except:
            pass
        time.sleep(2)
        try:
            weekends = browser.find_elements_by_xpath("//label[contains(text(), 'Are you able and willing to work weekends')]//following-sibling::div//child::option")
            weekends[1].click()
        except:
            pass
        time.sleep(2)
        try:
            holidays = browser.find_elements_by_xpath("//label[contains(text(), 'Will you be able and willing to work holidays')]//following-sibling::div//child::option")
            holidays[1].click()
        except:
            pass
        time.sleep(2)
        try:
            typeemp = browser.find_elements_by_xpath("//label[contains(text(), 'What type of employment is desired')]//following-sibling::div//child::option")
            typeemp[1].click()
        except:
            pass
        time.sleep(2)
        try:
            calltime = browser.find_elements_by_xpath("//label[contains(text(), 'Best Time to Call')]//following-sibling::div//child::option")
            calltime[1].click()
        except:
            pass
        time.sleep(2)
        ##availability each day of the week
        available = ['SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY']
        for date in available:
            try:
                day1 = browser.find_elements_by_xpath("//label[contains(text(), '{}')]//following-sibling::div//child::option".format(date))
                day1[1].click()
                time.sleep(2)
            except:
                pass
        ##previous employment information
        ##have you worked for kroger
        try:
            workkroger = browser.find_element_by_xpath("//label[contains(text(), 'Have you ever worked for the Kroger')]//following-sibling::div//child::textarea")
            fill_simple(workkroger, str_format(np.random.choice(['no', 'N/A', 'No', 'NO'])), browser)
        except:
            pass
        time.sleep(2)
        #worked in retail
        try:
            workretail = browser.find_element_by_xpath("//label[contains(text(), 'Have you ever worked for any other retail')]//following-sibling::div//child::textarea")
            fill_simple(workretail, str_format(np.random.choice(['no', 'N/A', 'No', 'NO'])), browser)
        except:
            pass
        time.sleep(2)
        ##terminated
        try:
            terminate = browser.find_elements_by_xpath("//label[contains(text(), 'Have you ever been terminated')]//following-sibling::div//child::option")
            terminate[-1].click()
        except:
            pass
        time.sleep(2)
        ##cash shortages
        try:
            cashshort = browser.find_elements_by_xpath("//label[contains(text(), 'In any prior employment have you ever had cash shortages')]//following-sibling::div//child::option")
            cashshort[-1].click()
        except:
            pass
        time.sleep(2)
        ##personal background info
        #signature for all
        try:
            for sign in browser.find_elements_by_xpath("//label[contains(text(), 'Signature')]//following-sibling::div//child::input"):
                scroll_fill_element(sign,
                        str_format(details['firstname'] + ' ' + details['lastname']), browser)
        except:
            print("No signing")
        #convicted
        try:
            convict = browser.find_elements_by_xpath("//label[contains(text(), 'Have you been convicted')]//following-sibling::div//child::option")
            convict[1].click()
        except:
            pass
        time.sleep(2)
        ##emergency contact info
        #contact first name
        gender = np.random.choice(["F", "M"])
        if gender == "F":
            #female first name
            try:
                emergencyfirst = browser.find_element_by_xpath("//label[contains(text(), 'Contact First Name')]//following-sibling::div//child::input")
                fill_simple(emergencyfirst, str_format(np.random.choice(common_female_first_name)), browser)
            except:
                pass

            #contact last name
            try:
                emergencylast = browser.find_element_by_xpath("//label[contains(text(), 'Contact Last Name')]//following-sibling::div//child::input")
                fill_simple(emergencylast, str_format(np.random.choice(common_last_names)), browser)
            except:
                pass

            #relationship
            try:
                relation = browser.find_elements_by_xpath("//label[contains(text(), 'Contact Relationship')]//following-sibling::div//child::option")
                relation[-2].click()
            except:
                pass

            #phone #
            try:
                phonenum = browser.find_element_by_xpath("//label[contains(text(), 'Contact Phone Number')]//following-sibling::div//child::input")
                fill_simple(phonenum, str(generate_fake_phone_number()), browser)
            except:
                pass
            time.sleep(2)
        else:
            #male first name
            try:
                emergencyfirst = browser.find_element_by_xpath("//label[contains(text(), 'Contact First Name')]//following-sibling::div//child::input")
                fill_simple(emergencyfirst, str_format(np.random.choice(common_male_first_names)), browser)
            except:
                pass

            #contact last name
            try:
                emergencylast = browser.find_element_by_xpath("//label[contains(text(), 'Contact Last Name')]//following-sibling::div//child::input")
                fill_simple(emergencylast, str_format(np.random.choice(common_last_names)), browser)
            except:
                pass

            #relationship
            try:
                relation = browser.find_elements_by_xpath("//label[contains(text(), 'Contact Relationship')]//following-sibling::div//child::option")
                relation[1].click()
            except:
                pass
            time.sleep(2)
            #phone #
            try:
                phonenum = browser.find_element_by_xpath("//label[contains(text(), 'Contact Phone Number')]//following-sibling::div//child::input")
                fill_simple(phonenum, str(generate_fake_phone_number()), browser)
            except:
                pass
            time.sleep(2)

        #acknowledgement
        try:
            acknowledge = browser.find_elements_by_xpath("//label[contains(text(), 'Acknowledgement')]//following-sibling::div//child::option")
            acknowledge[-1].click()
        except:
            pass
        time.sleep(2)
        #questions with radio buttons
        answer = browser.find_elements_by_xpath("//label[contains(text(), 'Yes')]")
        idx = 0
        for ans in answer:
            if idx >= 2:
                ans.click()
            idx += 1
            time.sleep(2)

# ::: UNCOMMENT HERE ::: #
        # # Click apply
        # time.sleep(3)
        # browser.find_element_by_xpath("//span[text()='Apply']").click()
        # try:
        #     time.sleep(3)
        #     browser.find_element_by_xpath("//span[text()='Apply']").click()
        # except:
        #     pass
        #
        # try:
        #     time.sleep(3)
        #     click_at(browser.find_element_by_xpath("//span[text()='Apply']"), browser)
        # except:
        #     pass
        #
        # # Final confirmation
        # wait_visible((By.XPATH, "//div[contains(text(), 'Your application has been sent')]"), browser)
        #
        # element = browser.find_element_by_tag_name('body')
        # element.screenshot(submit_path + "/{}_app{}_page_submit.png".format(firm,app_id))
        #
        # # Close window
        # browser.quit()
        #display.sendstop()
        #return None
    except Exception as e:
        print("Automation error for {} {} job {} {} {}: {}".format(details['firstname'], details['lastname'],
                    details['firm'], details['city'], details['state'], e))
        try:
            element = browser.find_element_by_tag_name('body')
            element.screenshot(error_path + "/{}_app{}_error.png".format(firm,app_id))
            #:::UNMARK HERE:::
            #browser.quit()
            #display.sendstop()
        except:
            print("Couldn't print error screen")
        print('\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a\a')

## ::: UNCOMMENT HERE ::: ##
# display = Display(visible=0, size=(1200, 900))
# display.start()
#browserpath = webdriver.Chrome(ChromeDriverManager().install())#'/accounts/projects/pkline/randres/randres/scraping/chromedriver_new'
chrome_options = chropopt()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1200x900")
chrome_options.add_argument("--no-sanbdox")
## ::: UNCOMMENT HERE ::: #
#chrome_options.add_argument('--user-agent="{}"'.format(ua))
## ::: UNCOMMENT HERE ::: #
# ::: on my computer i can't use the traiditional paths to install chromedriver method so change this how you see fit
# chrome_options.binary_location = '/accounts/projects/pkline/randres/chrome/opt/google/chrome/chrome'
browser = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#browser = webdriver.Chrome(browser_path, options=chrome_options)
browser.set_window_size(1300, 800)



# LINKS

details = details_example
#details['email'] = 'asdf23@mt2015.com'
link1 = "https://jobs.kroger.com/job/Monona-Night-Stocker-WI-53716/636597500/"
link2 = "https://jobs.kroger.com/marianos/job/Chicago-Grocery-Stocker-Team-Member-Mariano&apos;s-IL-60610/640958700/"
link3 = "https://jobs.kroger.com/job/Madison-Night-Stocker-WI-53719/646399400/"
stalelink1 = "https://jobs.kroger.com/marianos/job/Palatine-Grocery-Stocker-Team-Member-Mariano&apos;s-IL-60067/635952800/"

details['link'] = link3
submit_kroger(details)
