from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import csv

data=[]

def acm_crawler(max_pages):
    """data = ["journal_name,publisher_name,authors,title,date,volume,issue,issn,first_page,last_page,keywords,author_info, affiliation_info".split(",")]
    with open('deneme2.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for line in data:
            writer.writerow(line)"""
      
    page=1
    while max_pages >= 1:
        url='http://dl.acm.org/results.cfm?query=%22information%20filtering%22&querydisp=%22information%20filtering%22&start='+str(page)+'&slide=1&srt=score%20dsc&short=1&coll=DL&dl=ACM&source_disp=&source_query=Owner%3AACM&since_month=&since_year=&before_month=&before_year=&termshow=matchall&range_query=&dimval=4294670583&CFID=647969743&CFTOKEN=68893541'
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        source_code = urlopen(req).read()
        soup = BeautifulSoup(source_code)

        #get each paper url address
        for link in soup.find_all('a', {'class':'medium-text'}):
            href="http://dl.acm.org/"+link.get("href")
            get_paper_data(href)
            
        page+=50
        max_pages=max_pages-1

    #write collected data to the csv file
    with open('papers.csv', 'a', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        for line in data:
            writer.writerow(line)

#collect all paper related data
def get_paper_data(paper_url):
    req = Request(paper_url, headers={'User-Agent': 'Mozilla/5.0'})
    source_code = urlopen(req).read()
    soup = BeautifulSoup(source_code)

    data2=[]
    #journal name
    try:
        journalName=soup.find("meta", {"name":"citation_journal_title"})['content']
        data2.append(journalName)
    except TypeError:
        journalName='Null'
        data2.append(journalName)
    #publisher name
    try:
        publisherName=soup.find("meta", {"name":"citation_publisher"})['content']
        data2.append(publisherName)
    except TypeError:
        publisherName='Null'
        data2.append(publisherName)
    #authors name
    try:
        authorsName=soup.find("meta", {"name":"citation_authors"})['content']
        data2.append(authorsName)
    except TypeError:
        authorsName='Null'
        data2.append(authorsName)
    #paper title
    try:
        paperTitle=soup.find("meta", {"name":"citation_title"})['content']
        data2.append(paperTitle)
    except TypeError:
        paperTitle='Null'
        data2.append(paperTitle)
    #paper publication date
    try:
        date=soup.find("meta", {"name":"citation_date"})['content']
        data2.append(date)    
    except TypeError:
        date='Null'
        data2.append(date)
    #paper volume
    try:
        paperVolume=soup.find("meta", {"name":"citation_volume"})['content']
        data2.append(paperVolume)
    except TypeError:
        paperVolume='Null'
        data2.append(paperVolume)
    #paper issue
    try:
        paperIssue=soup.find("meta", {"name":"citation_issue"})['content']
        data2.append(paperIssue)
    except TypeError:
        paperIssue='Null'
        data2.append(paperIssue)
    #paper issn
    try:
        issn=soup.find("meta", {"name":"citation_issn"})['content']
        data2.append(issn)
    except TypeError:
        issn='Null'
        data2.append(issn)
    #paper first page
    try:
        firstpage=soup.find("meta", {"name":"citation_firstpage"})['content']
        data2.append(firstpage)
    except TypeError:
        firstpage='Null'
        data2.append(firstpage)
    #paper last page
    try:
        lastpage=soup.find("meta", {"name":"citation_lastpage"})['content']
        data2.append(lastpage)
    except TypeError:
        lastpage='Null'
        data2.append(lastpage)
    #paper keywords
    try:
        keywords=soup.find("meta", {"name":"citation_keywords"})['content']
        data2.append(keywords)
    except TypeError:
        keywords='Null'
        data2.append(keywords)
    #authors id and name   
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
    #authors affiliation name and id
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
    #paper tags
    tags=[]
    try:
        for link in soup.find_all('a'):
            for link2 in link.find_all('span'):
                tags.append(link2.get_text())
        data2.append(tags)  
    except TypeError:
        data2.append('Null')
        

    data.append(data2)
       
            
acm_crawler(1)

    



