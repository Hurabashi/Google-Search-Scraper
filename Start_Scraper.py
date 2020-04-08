'''
By Dominykas Venclovas 2020
Intended only for website friendly scraping.

You need two files to use the scraper:
keywords.txt with a list of key words you would like to check
website.txt with your website
'''

import urllib
import requests
from bs4 import BeautifulSoup
import time
import re
import math


def daSearch(query, agent):
    '''Returns a list of urls find in a google search with specified query'''
    URL = f"https://google.com/search?q={query}"

    headers = {"user-agent": agent}
    resp = requests.get(URL, headers=headers)

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                item = link
                results.append(item)
        return results
    else:
        print('Search failed :(')


def findWhichLink(link_list,the_link):
    '''
    Returns a number which represents which link it is in 
    google search from top to bottom, 2nd page first link returning 11
    '''
    pattern = re.compile(the_link)
    link_number = 0
    for i in range(len(link_list)):
        if pattern.search(link_list[i]):
            link_number = i + 1
            break
    if link_number > 0:
        return link_number
    #This not recommend way of dealing with this but this method avoids dealing with errors later on
    #I will probably change it into something more appropriate in future.
    else:
        return 10000

#
def linkNumbToPage(link_numb):
    '''Returns page number based on number find with findWhichLink function'''
    page_numb = math.ceil(link_numb/10)
    return page_numb

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

#get keywords and website form txt files
keyword_list = [line.rstrip('\n') for line in open('keywords.txt', encoding='utf8')]
website = [line.rstrip('\n') for line in open('website.txt', encoding='utf8')]
website = website[0]

#wait time in seconds and number of pages +1 to go through
try:
    wait_time = int(input('Enter wait time in seconds (10 is highly recommended): '))
except:
    wait_time = 10
    print('That is not an integer wait time was set to 10 seconds by default')

try:
    pages = int(input('Enter number of the first pages you would like to search (25 is default): '))
except:
    pages = 25
    print('That is not an integer number of pages was set to 25 by default')

#calculates maximum wait time and displays it
number_of_hours = ((wait_time*pages+wait_time) *len(keyword_list)) / 360
print(f'This may take {number_of_hours} hours')

#creates file for results and writes it's head
file = open("results.txt","w",encoding='utf8')
file.write(f"We are looking at the first {pages + 1} pages of google search for {website} \n")
file.write("Keyword   Search Number   Google Page Number \n")

for query in keyword_list:
    #Makes query good for google if it has more than one word
    query = query.replace(' ', '+')
    
    #Checks the first google page for the website
    reziultatai = daSearch(query,USER_AGENT)
    numb_link = findWhichLink(reziultatai, website)
    if numb_link != 10000:
        result_page = 1
        file.write(f"{query.replace('+',' ')}   {numb_link}   {result_page} \n")
    #Checks other pages for the website
    else:
        for i in range(pages):
            #Needed to not overload google servers and not getting your ip banned
            time.sleep(wait_time)
            new_query = query
            kelintas_psl = (1+i)*10
            new_query += f'&start={kelintas_psl}'
            reziultatai += daSearch(new_query,USER_AGENT)
        numb_link = findWhichLink(reziultatai, website)
        result_page = linkNumbToPage(numb_link)
        if numb_link == 10000:
            file.write(f"{query.replace('+',' ')}   was not found \n")
            print(f"{query.replace('+',' ')}   was not found \n")
        else:
            file.write(f"{query.replace('+',' ')}   {numb_link}   {result_page} \n")
            print(f"{query.replace('+',' ')}   {numb_link}   {result_page} \n")
    #Needed to not overload google servers and not getting your ip banned
    time.sleep(wait_time)
print('Done')