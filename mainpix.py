import requests
from io import BytesIO
from PIL import Image
from RPA.Browser.Selenium import Selenium
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import datetime


class crawl():
    
    def __init__(self, nMonths, phrase, section, Types):
        self.nMonths = nMonths
        self.phrase = phrase
        self.section = section
        self.Types = Types
        self.wd = None

    def openURL(self):

        #OPENS URL
        url = 'https://www.nytimes.com/'
        self.wd = Selenium()
        self.wd.open_available_browser(url)
        #self.wd = webdriver.Chrome()
        #self.wd.get(url)

        #maximizes window to see full site information
        self.wd.driver.maximize_window()
        #self.wd.maximize_window()
        time.sleep(1)

        #clicks accept cookies if it appears
        try:
            self.wd.click_button('//*[@id="dock-container"]/div[2]/div/div/div[2]/button[1]')
        except: print('no cookies shown')
        time.sleep(2)


        return self.wd

    def defineDateSearch(self):

        # CLICK SEARCH BUTTON
        self.wd.click_button('//*[@id="app"]/div[2]/div/header/section[1]/div[1]/div[2]/button')
        time.sleep(0.5)

        #INSERTS SEARCH PHRASE ON THE SEARCH FIELD
        self.wd.input_text('//*[@id="search-input"]/form/div/input', self.phrase)

        #CLICK OK BUTTON TO EXECUTE SEARCH
        self.wd.click_button('//*[@id="search-input"]/form/button')
        time.sleep(1)


        ######################################
        #### DATE SELECTION STEP BEGIN ####
        ######################################

        #DEFINE THE DATA RANGE FOR THE SEARCH BASED ON INIT DATE AND SEARCH PERIOD
        now = datetime.datetime.today().strftime('%m/%d/%Y')
        searchPeriod = (datetime.datetime.today() - datetime.timedelta(days=self.nMonths * 30)).strftime('%m/%d/%Y')

        # CLICKS THE DATA RANGE BUTTON
        self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[1]/div/div/button')
        time.sleep(0.5)
        # CLICK ON CUSTOM DATES
        self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[1]/div/div/div/ul/li[6]/button')
        time.sleep(0.5)
        # INSERTS INITIAL DATE
        self.wd.input_text('//*[@id="startDate"]', now)
        time.sleep(0.5)
        # INSERTS FINAL DATE
        self.wd.input_text('//*[@id="endDate"]', searchPeriod)
        time.sleep(0.5)
        # CLICKS THE DATA RANGE BUTTON TO HIDE THE MENU
        self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[1]/div/div/button')
        time.sleep(0.5)

        ######################################
        #### DATE SELECTION STEP ENDS ####
        ######################################
        
    def defineSection(self):

            ######################################
            #### SECTION SELECTION STEP BEGIN ####
            ######################################

            ## OPEN SECTION DROPDOWN
            self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[2]/div/div/button')             
            time.sleep(1)

            #options list on the section dropdown
            sectionElements = self.wd.find_elements("//*[@id='site-content']/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li")
            time.sleep(1)

            # Iterate over the list of elements to find the desired one
            for i, element in enumerate(sectionElements):

                elementText = element.text
                #first string treatment, removing numbers
                elementText = re.sub(r'\d', '', elementText)
                #second string treatment, removing special characters
                elementText = re.sub(r'[^\w\s]', '', elementText)
                # Verifies the partial string match 
                for s in self.section:
                    if s == elementText:
                        # Clicks the element to continue search
                        self.wd.click_button(element)
            time.sleep(1)

            #CLICK SECTION AGAIN TO HIDE THE MENU
            self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[2]/div/div/button')    
            time.sleep(1)

        ####################################
        #### SECTION SELECTION STEP END ####
        ####################################
            
    def defineType(self):

        ######################################
        #### TYPE SELECTION STEP BEGIN ####
        ######################################

        ## OPEN TYPE DROPDOWN
        self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[3]/div/div/button')
        time.sleep(1)

        #list of options on the types menu
        typeElements = self.wd.find_elements('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[3]/div/div/div/ul/li')
        time.sleep(1)

        # Iterate over the list of elements to find the desired one
        for i, element in enumerate(typeElements):

            elementText = element.text
            #first string treatment, removing numbers
            elementText = re.sub(r'\d', '', elementText)
            #second string treatment, removing special characters
            elementText = re.sub(r'[^\w\s]', '', elementText)
            # Verifies the partial string match 
            for t in self.Types:
                if t == elementText:
                    # Clicks the element to continue search
                    self.wd.click_button(element)
        time.sleep(1)

        #CLICK TYPE AGAIN TO HIDE THE MENU
        self.wd.click_button('//*[@id="site-content"]/div/div[1]/div[2]/div/div/div[3]/div/div/button')
        time.sleep(1)

        ####################################
        #### TYPE SELECTION STEP END ####
        ####################################
    
    def sortByNewest(self):
        ##########################    
        ## SORT BY NEWEST BEGIN ##
        ##########################

        #clicks on the sort button
        self.wd.click_element('//*[@id="site-content"]/div/div[1]/div[1]/form/div[2]/div/select')
        time.sleep(0.5)
        self.wd.click_element('//*[@id="site-content"]/div/div[1]/div[1]/form/div[2]/div/select/option[2]')
        time.sleep(0.5)
        self.wd.click_element('//*[@id="site-content"]/div/div[1]/div[1]/form/div[2]/div/select')
        time.sleep(0.5)

        ##########################    
        ## SORT BY NEWEST END   ##
        ##########################

    def chooseDateRelevantNews(self):
        ## CLICKS THE BUTTON TO SHOW MORE RESULTS UNTIL THE DESIRED PERIOD IS REACHED

        #new def for search period
        searchPeriod = (datetime.datetime.today() - datetime.timedelta(days=self.nMonths * 30)).strftime('%m/%d/%Y')
        #creation of soup
        soup= BeautifulSoup(self.wd.driver.page_source, 'html.parser')
        #### dates handling block to ensure comparison between site dates and system date
        finDate = soup.find('ol').findAll('li')[-1].find('div').find('span').get('aria-label')
        try:
            finDate = datetime.datetime.strptime(finDate, '%B %d, %Y').strftime('%m/%d/%Y')
        except: 
            finDate = f'{finDate}, {str(datetime.datetime.now().year)}'
            finDate = datetime.datetime.strptime(finDate, '%B %d, %Y').strftime('%m/%d/%Y')
        ####   
        finDateAux = datetime.datetime.strptime(finDate, '%m/%d/%Y')
        searchPeriodAux = datetime.datetime.strptime(searchPeriod, '%m/%d/%Y')
        while finDateAux > searchPeriodAux:
            ### CLICK SHOW MORE ###
            try:
                self.wd.click_button('//*[@id="site-content"]/div/div[2]/div[2]/div/button')
            except: pass
            time.sleep(3)
            #Refresh finDate to get recently loaded news
            soup=BeautifulSoup(self.wd.driver.page_source, 'html.parser')
            finDate = soup.find('ol').findAll('li')[-1].find('div').find('span').get('aria-label')
            try:
                finDate = datetime.datetime.strptime(finDate, '%B %d, %Y').strftime('%m/%d/%Y')
            except: 
                finDate = finDate + ', ' + str(datetime.datetime.now().year)
                finDate = datetime.datetime.strptime(finDate, '%B %d, %Y').strftime('%m/%d/%Y')
            ####   
            finDateAux = datetime.datetime.strptime(finDate, '%m/%d/%Y')

    def captureInfo(self):

        #DICT TO INITIALLY HOLD THE INFORMATION
        resultsDict = {'title': [],
                    'date' : [],
                    'description': [],
                    'count': [],
                    'monetaryTitle': [],
                    'image': []
                    }
        
        soup = BeautifulSoup(self.wd.driver.page_source, 'html.parser')
        searchResults = soup.find('ol').findAll('li')
        for i,element in enumerate(searchResults, start = 2):
            try:
                title = element.find('h4').text
                resultsDict['title'].append(title)
            except:
                resultsDict['title'].append('Não encontrado')
            try:
                resultsDict['date'].append(element.find('div').find('span').get('aria-label'))
            except:
                resultsDict['date'].append('Não encontrado')
            try:
                description = element.find('div').find('div').find('div').find('a').find('p').text
                resultsDict['description'].append(description)
            except:
                resultsDict['description'].append('Não encontrado')
            try: 
                #COUNT HOW MANY TIMES A SUBSTRING IS PRESENT IN THE MAIN STRING
                countTitle = title.count(self.phrase)
                countDescription = description.count(self.phrase)
                count = countTitle + countDescription
                resultsDict['count'].append(count)
            except:
                resultsDict['count'].append('Não encontrado')
            
            # GET IMAGE URL FROM PAGE HTML
            try:
                imagem_url = element.find('div').find('div').find('figure').find('div').find('img').get('src')

                # DOWNLOAD IMAGE USING REQUESTS LIB
                response = requests.get(imagem_url)
                imagem_bytes = BytesIO(response.content)

                # SAVE IMAGE LOCALLY
                imagem = Image.open(imagem_bytes)
                imgName = f"imageCellD{i}.jpg"
                imagem.save(imgName)
                # APPEND IMAGE LOCATION TO THE TABLE
                resultsDict['image'].append(imgName)
            except: 
                resultsDict['image'].append('Não encontrado')
                pass

            ## MONETARY DETECTION ON TITLE AND DESCRIPTION
            # string pattern for money recognition
            stringPattern = r'\$(\d{1,3}(,\d{3})*(\.\d+)?)|\b\d+\s*(dollars?|USD)\b'
            # IF THE stringPattern matches title or destiption, set monetaryTitle to True, else False
            if re.search(stringPattern, title) or re.search(stringPattern, description):
                resultsDict['monetaryTitle'].append('True')
            else: 
                resultsDict['monetaryTitle'].append('False')
            

        # RESULTANT DATAFRAME
        df = pd.DataFrame(resultsDict)
        df = df.drop_duplicates()
        df = df[df['title'] != 'Não encontrado'].to_excel('NY_CollectResults.xlsx', index=False)

    def run(self):
    #METHOD TO EXECUTE COMMANDS
    
        self.openURL()
        self.defineDateSearch()
        self.defineSection()
        self.defineType()
        self.sortByNewest()
        self.chooseDateRelevantNews()
        self.captureInfo()