import MySQLdb


###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################

outFileName="collab-keyword.tsv"
f = open(outFileName, 'w')

### Reading from table paper_aff1_aff2_keyword

keywordSql="select affiliation1,affiliation2,keyword,count(*) as count from paper_aff1_aff2_keyword group by affiliation1,affiliation2,keyword order by count desc;"
cur.execute(keywordSql)
for row in cur.fetchall() :
    aff1=row[0]
    aff2=row[1]
    keyword=row[2]
    count=row[3]
    string=aff1+","+aff2+","+keyword+","+str(count)+"\n"
    f.write(string)
   # print string
    #print keywords_tags_list[paperId]
f.close()
