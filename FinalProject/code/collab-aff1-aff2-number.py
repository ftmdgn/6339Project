import MySQLdb

###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################

f1 = open("collaboration-paper.csv", 'w')

sql="select affiliation1, affiliation2, count(paper_id) as c from collab_paper_aff1_aff2 group by affiliation1, affiliation2  order by c desc;"
cur.execute(sql)
for row in cur.fetchall() :
    aff1=row[0]
    aff2=row[1]
    count=str(row[2])
    string=aff1+","+aff2+","+count+'\n'
    f1.write(string)
