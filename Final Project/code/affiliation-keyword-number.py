import MySQLdb


###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################
outFileName3="aff_keyword_number.txt"

f3 = open(outFileName3,'w')


affiliationDict={}
affliliationList={}
keywords_tags_list={}
paperId_keywords={}
paper_id_aff={}
### Reading from table data

dataSql="select id, title, affiliation_info,keywords,tags from data;"
cur.execute(dataSql)
for row in cur.fetchall() :
    aff=row[2]
    paperId=row[0]
    title=row[1]
    keywords=row[3]
    tags=row[4]
    affliliationList[paperId]=aff.split(',')
    paper_id_aff[paperId]=[]
    string=keywords+','+tags
    string=string.lower()
    string=string.replace(";",",")
    keywords_tags_list[paperId]=(string).split(',')
    #print keywords_tags_list[paperId]

############SEPARATING KEYWORDS AND TAGS ########################
for paperId in keywords_tags_list:
    paperId_keywords[paperId]=[]
    for item in keywords_tags_list[paperId]:
       
        item=item.strip(',[];')
        item=item.strip()
        
        if item!="null" and len(item)!=0:
            if item not in paperId_keywords[paperId]:
                paperId_keywords[paperId].append(item)
#print paperId_keywords

#############################################################
length=len(affliliationList)
#for i in range(length):
for i in affliliationList:
    affName=""
    for item in  affliliationList[i]:
        item=item.strip()
        item=item.strip(',[]')
        if item[:3]=="600" and item[:4]!="600 " and item[:6]!="60054 ":
            if not item in paper_id_aff[i]:
                paper_id_aff[i].append(item)                        
            
print len(affiliationDict)
    

##################################SELECT FROM PAPER AFFILIATION TABLE AND INSERT INTO PAPER AFFILIATION KEYWORD TABLE###########
aff_keyword_number={}
for paper_id in paper_id_aff:
    for aff_id in paper_id_aff[paper_id]:
        if aff_id not in aff_keyword_number:
            aff_keyword_number[aff_id]={}
for paper_id in paperId_keywords:
    for keyword in paperId_keywords[paper_id]:
        for aff_id in paper_id_aff[paper_id]:
            if keyword not in aff_keyword_number[aff_id]:
                aff_keyword_number[aff_id][keyword]=1
            else:
                aff_keyword_number[aff_id][keyword]=aff_keyword_number[aff_id][keyword]+1

count_all=0
sqlArray=[]
for aff_id in aff_keyword_number:
    for keyword in aff_keyword_number[aff_id]:
        number=aff_keyword_number[aff_id][keyword]
        insertKeySql="insert into affiliation_keyword_number values("+str(aff_id)+",'"+keyword+"','"+str(number)+"');"
        sqlArray.append(insertKeySql)
        f3.write(insertKeySql+'\n')
        count_all=count_all+1
print count_all
f3.close()
for q in sqlArray:
    cur.execute(q)

