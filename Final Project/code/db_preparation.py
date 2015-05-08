import MySQLdb

###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################

outFileName2="universities2.tsv"
outFileName1="universities1.tsv"
f2 = open(outFileName2, 'w')
f1 = open(outFileName1, 'w')


affiliationDict={}
affliliationList={}
paper_id_aff={}
### Reading from table data

dataSql="select id, title, affiliation_info from data ;"
cur.execute(dataSql)
for row in cur.fetchall() :
    aff=row[2]
    paperId=row[0]
    affliliationList[paperId]=aff.split(',')
    paper_id_aff[paperId]=[]
    

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
                        
            if item in affiliationDict:
                if affName not in affiliationDict[item]:
                    affiliationDict[item].append(affName)
                    
            else:
                affiliationDict[item]=[affName]
            affName=""

            
                
            #print item
        else:
            affName=affName+","+item
print len(affiliationDict)

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

collab_paper_aff1_aff2=[]
insertList=[]

for paper_id in paper_id_aff:
    for aff1 in paper_id_aff[paper_id]:
        for aff2 in paper_id_aff[paper_id]:
            if aff1!=aff2:
                collab_paper_aff1_aff2.append([paper_id,aff1,aff2])
                insertSql="insert into collab_paper_aff1_aff2 values ("+str(paper_id)+",'"+aff1+"','"+aff2+"');"
                insertList.append(insertSql)
                
f3=open("insert.txt",'w')
for q in insertList:
    f3.write( q+'\n')
    #cur.execute(q)
    
##print collab_paper_aff1_aff2
                
    
        
    
    


