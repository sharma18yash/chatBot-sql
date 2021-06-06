import spacy
import numpy
from word2number import w2n
nlp = spacy.load("en_core_web_md")
from spacy.vocab import Vocab
import mysql.connector
vocab = Vocab()

def NLPQuery(Nl_query):
    print(Nl_query)
    l = []
    if "names" in Nl_query:
        Nl_query  = Nl_query.replace("names", "name")
    if "students" in Nl_query:
        Nl_query = Nl_query.replace("students", "student")

    doc = nlp(Nl_query)
    synonymSel = ['select', 'show', 'display', 'exhibit', 'demonstrate', 'display', 'prove', 'evince', 'indicate',
               'show up', 'present', 'reveal', 'evidence', ' choice', 'choose', ' pick', ' take', 'elect', 'prime', 'chosen',
               'cull', 'pick out', 'exclusive', 'exhibit', 'show', 'expose', 'presentation', 'reveal', 'demonstration', 'flaunt',
               'demonstrate', 'exhibition', 'parade', 'give']
    synWher = ["where", "whither",  "whereabouts",  "wherein",  "wherever",  "location",  "locus",  "position",  "site",
               "spot",  "place", "having", "from", "whose", "teaching"]
    databases = ['student', 'teachers']
    fields = ['name', 'address', 'city', 'marks', 'subject']
    outField = []
    cndField = []
    cnd = []
    for word in synonymSel:
        if word in Nl_query:
            print("DDL")
            break
    """Breaking down NLP query to different parts"""
    m=0
    f1 = []
    t = Nl_query.split()
    ind=0

    for i in doc:
        if i.pos_ == "NOUN" and i.text in databases:
            database = i.text
        if i.text in synWher:
            ind = Nl_query.index(i.text)


    if ind!=0:
        print("inside ind")
        for i in doc:
            if i.pos_ == "NOUN" and i.text in fields:
                if Nl_query.index(i.text)<ind:
                    outField.append(i.text)
                elif Nl_query.index(i.text)>ind:
                    cndField.append(i.text)
                    m = max(m, t.index(i.text))
    if ind==0:
        for i in doc:
            if i.pos_ == "NOUN" and i.text in fields:
                outField.append(i.text)
    if m>0:
    #     print(t)
        for i in doc:
            z = i.text
            ind1 = t.index(z)
            if i.pos_ == "NUM" and t.index(z)>m:
                res = w2n.word_to_num(i.text)
                cnd.append(res)
    #             print("1")
            elif i.pos_ == "NOUN" and t.index(z)>m:
                cnd.append(i.text)
    #             print("2")
            elif i.pos_ == "ADJ" and t.index(z)>m:
                cnd.append(i.text)

    print("here2")

    print("out Field = ", outField)
    print("cnd Field = ", cndField)
    print("cnd = ", cnd)

    """Constructing SQL queries"""
    flag = 0
    query = ['Select']
    if len(outField) ==0:
        query.append(" *")
    else:
        for i in outField:
            flag=1
            query.append(i)
            query.append(",")
    if flag==1:
        query.pop()
    query.append("from")
    query.append(database)
    if len(cndField)>0:

        query.append("where")
        for i in cndField:
            query.append(i)
        query.append("=")
        query.append("'{}'".format(cnd[0]))
    # print(query)
    qu = ""
    for i in query:
        qu = qu+i+" "
    print("QUERY")
    print(qu)
    mydb = mysql.connector.connect(
    host="35.193.192.1",
    user="root",
    password="sacsdc23r435ytgerf",
    database="school"
    )
    print(mydb)
    mycursor = mydb.cursor()
    mycursor.execute(qu)
    result = mycursor.fetchall()
    out=""
    for x in result:
        out+=str(x)
        out+="<br>"
    print(out)
    return out

from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    try:
        # print(userText)
        out = NLPQuery(userText)
    except :
        out = "ERROR"
    return out

if __name__ == "__main__":
    app.run()
