import imapclient
import imaplib
import pyzmail
import pprint
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

print('\n'
	'\n'
	'\n'



	"""**********************Process Start**********************"""


	)

# This logs into my email server via IMAP connection
# ==============================================================

imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login('EMAIL', 'PASSWORD')
imapObj.select_folder('FRI Rental Leads', readonly=False)
# ==============================================================


# This parses through the results and grabs the relevant UIDs
# ==============================================================

UIDs = imapObj.search(['SUBJECT "SEARCH STRING"', 'SEEN', 'SINCE 27-Feb-2017'])
UIDs
rawMessages = imapObj.fetch(UIDs,['BODY[]', 'FLAGS'])
browser = webdriver.Firefox()
for UID in UIDs:
	imaplib._MAXLINE = 10000000
	message = pyzmail.PyzMessage.factory(rawMessages[UID][b'BODY[]'])
	message.html_part.get_payload().decode(message.html_part.charset)
	messagehtml = message.html_part.get_payload().decode(message.html_part.charset)
	BeautifulSoup(messagehtml, "html.parser").find_all("a", text="View the guest card for this lead.")
# ==============================================================


# Lead Name stored
# ==============================================================


	leadName = BeautifulSoup(messagehtml, "html.parser").findAll('a')[0].string
	leadEmail = BeautifulSoup(messagehtml, "html.parser").findAll('a')[1].string
	leadPhone = BeautifulSoup(messagehtml, "html.parser").findAll('a')[2].string
	if leadPhone == "Reply":
		leadPhone = "no phone number provided in lead email"

	
# ==============================================================

	UID = str(UID)
	print("********************** Working on " + UID + "**********************")
	print("Lead Info:", '\n')
	print(leadName)
	print(leadEmail)
	print(leadPhone, '\n')

	
	#Storing in leadLink variable
	# ==============================================================

	leadLink = BeautifulSoup(messagehtml, "html.parser").find_all("a", text="View the guest card for this lead.")
	for link in leadLink:
		leadLink = link.get('href')
		print("~~~~~~~~ I found the guest card link! ~~~~~~~~")

		blank = []
		if leadLink == blank:
			print("--------------------- Could not find the Guest Card link ---------------------")
			continue
	# ==============================================================

		
    

	# Opens Firefox Browser
		browser = webdriver.Firefox()
		type(browser)
	# ==============================================================

		# Opens FL Realty Homepage
		# ==============================================================

		try:
			browser.get(leadLink)
		except AttributeError:
			print("I got something but it wasnt a link")
			browser.quit()
			continue

		emailElem = browser.find_element_by_id('user_email')
		emailElem.send_keys('EMAIL')

		passwordElem = browser.find_element_by_id('user_password')
		passwordElem.send_keys('PASSWORD')
		passwordElem.submit()
		# ==============================================================


		##Waiting for action log to become visible
		# ==============================================================

		try:
			actionLog_ready = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.js-activity-log-row")))
		except TimeoutException:
			print("Weird...that link took me to the wrong page", '\n')
			browser.get('DESIRED URL')
			browser.quit()
			continue
		# ==============================================================


		## Parsing through actions log to make sure we are first to claim lead
		browser.find_elements(By.CSS_SELECTOR, "div.js-activity-log-row")

		actions = browser.find_elements(By.CSS_SELECTOR, "div.js-activity-log-row")
		times_contacted = str(len(actions))
		if len(actions) > 1:
		    print("This lead has already been contacted " + times_contacted + " times recently", '\n')
		    browser.get('DESIRED URL')
		    browser.quit()
		    continue
		else:
			pass
		# ==============================================================


		##Locating Text Area
		# ==============================================================
		try:
			sms_area = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".js-inline-texting-body")))

		except TimeoutException:
			print("A phone number was not included with this lead")
			browser.get('DESIRED URL')
			browser.quit()
			continue
		except:
		    raise Exception("Couldn't find the Text Area").with_traceback(tracebackobj)
		else:
			sms_area.send_keys("Lorem ipsum dolor, lorem ipsum dolor")
			browser.find_element_by_css_selector('.text-history-block__submit')
			submit = browser.find_element_by_css_selector('.text-history-block__submit')
			submit.click()
			pass

		
		print("I just contacted " + leadName + " via SMS at " + leadPhone)
		logging.basicConfig(filename='contacted.log',level=logging.DEBUG)
		logging.info(" " + leadName + " was just contacted via the FRI portal")
		# ==============================================================



		# Recording Communication
		# ==============================================================

		browser.find_element_by_css_selector('.js-record-contact-task')
		recordcomlink = browser.find_element_by_css_selector('.js-record-contact-task')
		recordcomlink.click()

		# Record Communication Pop up
		# ==============================================================

		browser.find_element_by_css_selector('form.js-record-contact-form:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > textarea:nth-child(1)')
		recordcompopuptextarea = browser.find_element_by_css_selector('form.js-record-contact-form:nth-child(1) > div:nth-child(6) > div:nth-child(2) > div:nth-child(1) > textarea:nth-child(1)')
		recordcompopuptextarea.click()
		recordcompopuptextarea.send_keys('Made a call to the number provided. Left VM')
		recordcompopuptextarea.submit()



		

		#FRI Logout and Browser Quit
		browser.quit()

#IMAP Logout
imapObj.logout()
print(



	"""**********************Process Complete**********************"""
	'\n'
	'\n'
	'\n'


	)
