import MySQLdb
import math
import operator


###############DB CONNECTION###########
db = MySQLdb.connect(host="localhost", user='root' ,  db='acm')
cur = db.cursor()

#########################################
#########################################

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
            affName=affName+"|"+item
print len(affiliationDict)

aff_paper_count={}
for paper_id in paper_id_aff:
    for aff_id in paper_id_aff[paper_id]:
        
        if aff_id not in aff_paper_count:
            aff_paper_count[aff_id]=[]
        if paper_id not in aff_paper_count[aff_id]:
            aff_paper_count[aff_id].append(paper_id)

paper_count_dict={}
for aff_id in aff_paper_count:
    paper_count=len(aff_paper_count[aff_id])
    paper_count_dict[aff_id]=paper_count
    
    

###########################################
#############################################
#########################################100 most collaborative affiliations#####

f1 = open("highest_collaboration.csv", 'w')

aff_collab_count_dict={}

sql="SELECT affiliation1,count(distinct paper_id) as count_paper from collab_paper_aff1_aff2 group by affiliation1 order by count_paper desc limit 100;"
cur.execute(sql)
for row in cur.fetchall() :
    aff1=row[0]
    collab_count=row[1]
    aff_collab_count_dict[aff1]=collab_count
    string=aff1+","+affiliationDict[aff1][0]+","+str(paper_count_dict[aff1])+","+str(collab_count)+'\n'
    f1.write(string)
f1.close()

####################################################

            ##papers published by each university##

####################################################

########################################################

                ##TF-IDF##

########################################################
outFileName3="tf-idf.txt"
f3 = open(outFileName3,'w')

### finding the total number of affiliations
countSql="select count( distinct affiliation) from affiliation_keyword_number;"
cur.execute(countSql)
for row in cur.fetchall() :
    count=row[0]
N=float(count)

keyword_affiliation={}
affiliation_keyword_frequency={}
tf_idf={}

### Reading from table affiliation-keyword-number

dataSql="select affiliation, keyword, number from affiliation_keyword_number;"
cur.execute(dataSql)
for row in cur.fetchall() :
    aff_id=row[0]
    keyword=row[1]
    frequency=row[2]
    if keyword not in keyword_affiliation:
        keyword_affiliation[keyword]=[]
    if aff_id not in keyword_affiliation[keyword]:
        keyword_affiliation[keyword].append(aff_id)
    if aff_id not in affiliation_keyword_frequency:
        affiliation_keyword_frequency[aff_id]={}
    if keyword not in affiliation_keyword_frequency[aff_id]:
        affiliation_keyword_frequency[aff_id][keyword]=frequency

for aff_id in affiliation_keyword_frequency:
    if aff_id not in tf_idf:
        tf_idf[aff_id]={}
    for keyword in affiliation_keyword_frequency[aff_id]:
        tf=math.log10(1+float(affiliation_keyword_frequency[aff_id][keyword]))
        doc_frequency=float(len(keyword_affiliation[keyword]))
        #print "doc freq:"+ str(doc_frequency)
        idf=N/doc_frequency
        #print "idf:"+str(idf)
        tf_idf_value=tf*idf
        tf_idf[aff_id][keyword]=tf_idf_value
##############################################################

            ##COSINE SIMLARITY##
        
##############################################################
f_similarity=open("similarity.csv",'w')
similarity_dict={}

for aff_id in aff_collab_count_dict:
    similarity_dict[aff_id]={}

a_product_b=0.0
a_denominator=0.0
b_denominator=0.0

iteration_count=0
for a_aff_id in aff_collab_count_dict:
    iteration_count=iteration_count+1
    print iteration_count
    #print tf_idf[a_aff_id]
    a_vector=tf_idf[a_aff_id]
    a_denominator=0.0
    for a_keyword in a_vector:
        a_denominator=a_denominator+(a_vector[a_keyword]*a_vector[a_keyword])
    for b_aff_id in tf_idf:
        if a_aff_id!=b_aff_id:
            b_vector=tf_idf[b_aff_id]
            b_denominator=0.0
            for a_keyword in a_vector:
                if a_keyword in b_vector:
                    a_product_b=a_product_b+(a_vector[a_keyword]*b_vector[a_keyword])
            for b_keyword in b_vector:
                b_denominator=b_denominator+(b_vector[b_keyword]*b_vector[b_keyword])
            similarity=a_product_b/(a_denominator+a_denominator+1)
            a_product_b=0.0
            similarity_dict[a_aff_id][b_aff_id]=similarity

for a_aff_id in similarity_dict:
    sorted_x = sorted(similarity_dict[a_aff_id].items(), key=operator.itemgetter(1),reverse=True) # returns tuple
    
    similarity_dict[a_aff_id]=sorted_x
    i=0
    for i in range(20):
        b_aff_id=similarity_dict[a_aff_id][i][0]
        string=a_aff_id+","+affiliationDict[a_aff_id][0]+","+similarity_dict[a_aff_id][i][0]+","+affiliationDict[b_aff_id][0]+","+str(similarity_dict[a_aff_id][i][1])+"\n"
        f_similarity.write(string)
        i=i+1
        
        
    
f_similarity.close()        


   
        
            
    
    

        
        

            
        

