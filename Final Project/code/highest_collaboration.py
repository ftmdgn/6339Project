import MySQLdb

###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor() 
#########################################

f1 = open("highest_collaboration.csv", 'w')

collab_count_dict={}

sql="SELECT affiliation1,count(distinct paper_id) as count_paper from collab_paper_aff1_aff2 group by affiliation1 order by count_paper desc limit 100;"
cur.execute(sql)
for row in cur.fetchall() :
    aff1=row[0]
    collab_count=row[1]
    collab_count_dict[aff1]=collab_count
    string=aff1+","+str(collab_count)+'\n'
    f1.write(string)
f1.close()
