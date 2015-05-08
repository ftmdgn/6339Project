from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
#import urllib
import csv
import time


def acm_crawler(max_pages):
    print ("Sona")
    
    """data = ["journal_name,publisher_name,authors,title,date,volume,issue,issn,first_page,last_page,keywords,author_info, affiliation_info".split(",")]
    with open('paper.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for line in data:
            writer.writerow(line)"""
     
    page=1
    while max_pages >= 1:
        #here you need to give the program the url and you need to remove number 1 after start and add str(page)
        url='http://dl.acm.org/results.cfm?query=&querydisp=&start='+str(page)+'&slide=1&srt=score%20dsc&short=1&coll=DL&dl=ACM&source_disp=&source_query=Owner%3AACM&since_month=&since_year=&before_month=&before_year=&termshow=matchall&range_query=&dimval=4294963359&CFID=647969743&CFTOKEN=68893541'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        source_code = urlopen(req).read()
        print ("Sona crawler")
        #print (source_code)
        soup = BeautifulSoup(source_code)

        #get each paper url address
        for link in soup.find_all('a', {'class':'medium-text'}):
            href="http://dl.acm.org/"+link.get("href")
            time.sleep(8) #timer
            get_paper_data(href)
            
        page+=50
        max_pages=max_pages-1


#collect all paper related data
def get_paper_data(paper_url):
    req = Request(paper_url, headers={'User-Agent': 'Mozilla/5.0'})
    source_code = urlopen(req).read()
    soup = BeautifulSoup(source_code)

    data2=[]
    try:
        journalName=soup.find("meta", {"name":"citation_conference"})['content']
        data2.append(journalName)
    except TypeError:
        journalName='Null'
        data2.append(journalName)
    try:
        publisherName=soup.find("meta", {"name":"citation_publisher"})['content']
        data2.append(publisherName)
    except TypeError:
        publisherName='Null'
        data2.append(publisherName)
    try:
        authorsName=soup.find("meta", {"name":"citation_authors"})['content']
        data2.append(authorsName)
    except TypeError:
        authorsName='Null'
        data2.append(authorsName)
    try:
        paperTitle=soup.find("meta", {"name":"citation_title"})['content']
        data2.append(paperTitle)
    except TypeError:
        paperTitle='Null'
        data2.append(paperTitle)
    try:
        date=soup.find("meta", {"name":"citation_date"})['content']
        data2.append(date)    
    except TypeError:
        date='Null'
        data2.append(date)
    try:
        paperVolume=soup.find("meta", {"name":"citation_volume"})['content']
        data2.append(paperVolume)
    except TypeError:
        paperVolume='Null'
        data2.append(paperVolume)
    try:
        paperIssue=soup.find("meta", {"name":"citation_issue"})['content']
        data2.append(paperIssue)
    except TypeError:
        paperIssue='Null'
        data2.append(paperIssue)
    try:
        isbn=soup.find("meta", {"name":"citation_isbn"})['content']
        data2.append(isbn)
    except TypeError:
        isbn='Null'
        data2.append(isbn)
    try:
        firstpage=soup.find("meta", {"name":"citation_firstpage"})['content']
        data2.append(firstpage)
    except TypeError:
        firstpage='Null'
        data2.append(firstpage)
    try:
        lastpage=soup.find("meta", {"name":"citation_lastpage"})['content']
        data2.append(lastpage)
    except TypeError:
        lastpage='Null'
        data2.append(lastpage)
    try:
        keywords=soup.find("meta", {"name":"citation_keywords"})['content']
        data2.append(keywords)
    except TypeError:
        keywords='Null'
        data2.append(keywords)
        
    author=[]
    try:
        for link in soup.find_all('a', {'title':'Author Profile Page'}):
            link=str(link)
            #name
            nameBeg=link.find('>')+1
            nameEnd=link.find('</a>')
            nameAuthor=link[nameBeg:nameEnd]
            #id
            idBeg=link.find('cfm?id=')+7           
            idEnd=link.find('&amp;coll')
            idAuthor=link[idBeg:idEnd]
            author.append(nameAuthor)
            author.append(idAuthor)
        data2.append(author)
    except TypeError:
        data2.append('Null')
        
    institution=[]
    try:
        for link in soup.find_all('a', {'title':'Institutional Profile Page'}):
            link=str(link)
            #name
            nameBeg=link.find('<small>')+7
            nameEnd=link.find('</small>')
            nameInstitution=link[nameBeg:nameEnd]
            #id
            idBeg=link.find('cfm?id=')+7           
            idEnd=link.find('&amp;')
            idInstitution=link[idBeg:idEnd]
            institution.append(nameInstitution)
            institution.append(idInstitution)
        data2.append(institution)
    except TypeError:
        data2.append('Null')

    tags=[]
    try:
        for link in soup.find_all('a'):
            for link2 in link.find_all('span'):
                tags.append(link2.get_text())
        data2.append(tags)  
    except TypeError:
        data2.append('Null')

    #write collected data to the csv file    
    with open('paper.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data2)

       
#here you need to give the total number of pages            
acm_crawler(1)

#Reading csv file
"""
    with open('paper.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

"""
    



