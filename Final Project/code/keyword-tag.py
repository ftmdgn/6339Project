import MySQLdb


###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################

outFileName2="universities2.tsv"
outFileName1="universities1.tsv"
outFileName3="aff1_aff2_keyword.txt"
f2 = open(outFileName2, 'w')
f1 = open(outFileName1, 'w')
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
    

##################################SELECT FROM PAPER AFFILIATION TABLE AND INSERT INTO PAPER AFFILIATION KEYWORD TABLE###########
affSql="select paper_id, affiliation1, affiliation2 from collab_paper_aff1_aff2;"
cur.execute(affSql)
number=0
for row in cur.fetchall() :    
    paperId=row[0]
    aff1=row[1]
    aff2=row[2]
    if paperId in paperId_keywords:
        for keyword in paperId_keywords[paperId]:
            insertKeySql="insert into paper_aff1_aff2_keyword values("+str(paperId)+",'"+aff1+"','"+aff2+"','"+keyword+"');"
            number=number+1
            
            f3.write(insertKeySql+'\n')
            #print insertKeySql
print number
f3.close()

############################CONCATINATING DIFFERENT PRESENTATION OF AFFILIATIONS############################

##length=len(affliliationList)
###for i in range(length):
##for i in affliliationList:
##    affName=""
##    for item in  affliliationList[i]:
##        item=item.strip()
##        item=item.strip(',[]')
##        if item[:3]=="600" and item[:4]!="600 " and item[:6]!="60054 ":
##            if not item in paper_id_aff[i]:
##                paper_id_aff[i].append(item)
##                        
##            if item in affiliationDict:
##                if affName not in affiliationDict[item]:
##                    affiliationDict[item].append(affName)
##                    
##            else:
##                affiliationDict[item]=[affName]
##            affName=""
##
##            
##                
##            #print item
##        else:
##            affName=affName+","+item
##print len(affiliationDict)

###########################WRITING AFFILIATION NAMES AND IDS IN FILES#############################################

##moreThan1=0
##for item in affiliationDict:
##    if len(affiliationDict[item]) >1:
##        moreThan1=moreThan1+1
##        string= item
##        string2=""
##        for aff in affiliationDict[item]:
##            string2=string2+" | "+aff
##
##        string=string+"\t"+string2+'\n'
##        f2.write(string)
##    else:
##        string=item+"\t"+affiliationDict[item][0]+'\n'
##        f1.write(string)
##    
##print moreThan1
##f2.close()
##f1.close()
    


##print paper_id_aff

###################### COLLABORATION OF AFFILATION1 AND AFFILIATION2 ON PAPER-ID ####################################################3
##
##collab_paper_aff1_aff2=[]
##insertList=[]
##
##for paper_id in paper_id_aff:
##    for aff1 in paper_id_aff[paper_id]:
##        for aff2 in paper_id_aff[paper_id]:
##            if aff1!=aff2:
##                collab_paper_aff1_aff2.append([paper_id,aff1,aff2])
##                insertSql="insert into collab_paper_aff1_aff2 values ("+str(paper_id)+",'"+aff1+"','"+aff2+"');"
##                insertList.append(insertSql)
##                
##f3=open("insert.txt",'w')
##for q in insertList:
##    f3.write( q+'\n')
    #cur.execute(q)
    
##print collab_paper_aff1_aff2
                
    
        
    
    


