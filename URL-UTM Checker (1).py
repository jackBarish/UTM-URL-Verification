#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Importing Lib
import requests, urllib
import pandas as pd
from lxml.html import fromstring
from datetime import date, datetime, time
import re 
import sys
from bs4 import BeautifulSoup
import webbrowser as wb
import os


# In[ ]:


#setting Display Options for Print_Statements
width = 300

pd.set_option('display.width', width*10)
pd.set_option('display.max_colwidth', width)


#used for color text
class fcolors:
    COMPLETED    =  "\033[32m"


# In[ ]:


#loading in file
file = './files/TODAY.xlsx'    #Change File Name to reflect Which UTM's You want to Read in

#reading in file
df = pd.read_excel(io = file,
                   sheet_name = 0,
                   header = 0)

#shape of the Dataframe
shape = df.shape

#setting the 1 value of the shape (length) to variable 'l'
l = shape[0]
print(l)

df.tail()


# In[ ]:


#Set empty array to store languagues
lang_list = []

#Set empty array to store Content ID
content_id = []

#variable to store the regular expression to be used
# English, German, Japanese, Spanish, French, Korean
regexp= 'EN.*?|DE.*?|JP.*?|SP.*?|FR.*?|KO.*?'
#regular expression looking for Content ID 
regexp_2 = '[_.*?]{1}[0-9]{4}'

#Creating a UDF
def Languagues(lang_list):
    """
    Intended to be used with URL's. Loops through the DataFrame, UDF uses regualr expression to parse
    out the language content from the URL.
    
    required LIB: Pandas, re
    
     PARAMETERS
    ----------
    df    | DataFrame from excel that stores all the URL's
    lang  | Empty array where the parsed text will be stored"""
    
    
    for i, value in df.iterrows():
        text = value
        text_2 = value
#Forces the Text variable to a char/str Datatype
        text = str(text)
        text_2 = str(text_2)
#Finds all the matches with the regular expression inside the text
        search = re.findall((regexp),text)
        search = search[0:1]
        id_search = re.findall((regexp_2),text_2)
        id_search = id_search[0:1]
        
#Appends each result to the empty lang array
        td = lang_list.append(search[0:1])
    
#Appends each result to the empty Content ID array
        id_td = content_id.append(id_search[0:1])

    
#prints the array
    print(f"{lang_list}{content_id}")

    

#Takes the array and changes it to a data frame for so we can loop through it easier & Checks the shape
    lang = pd.DataFrame(lang_list)
    url_lang_shape =lang.shape
    print(f"{df.shape}{url_lang_shape}")

#Ensures that if the URL shape and amount of languagues parsed are the same (Simple sanity check)
    if url_lang_shape[0] != df.shape[0]:
        print("Error: Lengths of URL and Language Index ")

#Executes the UDF
Languagues(lang_list)


# In[ ]:


#setting date and time to variable 'today'
today = datetime.now()

#converting the date time into a different format
time = today.strftime("%m/%d/%y   %H:%M")

#create empty array to store the final results
fin = []


#looping through the first column of the data frame
def Results(lang_list):
    
    #setting varibale num to 0
    num = 0
    
    for x in range(0,l):      
        r = requests.get(df['URL'][x])
        
#Gets the title from the URL        
        title = fromstring(r.content)
        title = title.findtext('.//title')
        
#Getting the Language that the WebPage is
        try:
            html = requests.get(df['URL'][x]).content
            soup = BeautifulSoup(html, 'html.parser',from_encoding = 'UTF-8')
            page_lang = soup.html["lang"]
        except:
            page_lang = "NULL"
        
#printing the final results of all the URL Data
        print(f" URL-> {x}   Status={r.ok}   HTTPCode={r.status_code} Page_Title:{title}  Encoding:{r.encoding} UTM_LANG:{lang_list[x]} | PAGE_LANG:{page_lang}   ContentID:{content_id[x]} \n")

#Saving all the data inside a variable to be used to write to a file
        fina = [f"URL:{x} Status:{r.ok} HTTP_Code:{r.status_code} Title:{title} Encoding:{r.encoding} UTM_LANG:{lang_list[x]} | PAGE_LANG:{page_lang} ContentID:{content_id[x]}"]

        
#increment the num variable
        num +=1
    
#appending each final data line into the array
        fin.append(fina)

#When loop is finished print completed with current date and time
        if num == l:
            print(fcolors.COMPLETED +f"""~~~DONE:  {time}""")
            
#If loop is completed force quit script
            sys.exit()
        else:
            pass
            


# ## Code Execution: Print Results
# 

# In[ ]:


Results(lang_list)


# ## Code Execution: Write Results
# 

# In[ ]:


#saving the array length of the final results
L = len(fin)

#saving day and Year in Variables
name_day = today.day
name_year = today.year

#Changing Data Type of day and year in order to use str for file name
name_day = str(name_day)
name_year = str(name_year)

#Combine Day & Year'

full_date = (f"{name_day}.{name_year}")


file_count = 0
dir_path = './files/UTM_Results/'

#Checking number of files inside folder & adding it to count
for path in os.scandir(dir_path):
    if path.is_file():
        file_count += 1
print('file count:', file_count)


#creating a UDF to write to a txt file
def write_file():
    with open(f'./files/UTM_Results/{file_count}_UTM_Checker_Results_{full_date}.txt', 'w',encoding="utf-8") as f:
        for x in range(0,L):
            f.write(f"{fin[x]}\n")
        f.write(f"\n\n~~~Completed:{time}")
        f.write(f"\n~~~URL'S Analyzed:{L}")

    f = open(file)
    print(fcolors.COMPLETED +f"""~File Created~""")



# In[ ]:


#Execute UDF to write File
write_file()

