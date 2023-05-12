from xml.etree import ElementTree as ET
from urllib.parse import unquote,unquote_plus
import base64
import csv
log_path='bad_requests.log'
def parse_log(log_path):
    result={}
    try:
        with open(log_path): pass
    except IOError as e:
        print("Error ",log_path,"doesn't exist")
        exit()
    try:
        tree=ET.parse(log_path)
    except Exception as e:
        print("Please make sure binary data is not present in log")
        exit()
    root = tree.getroot()
    for reqs in root.findall('item'):
        raw_req = reqs.find('request').text
        raw_req = unquote(raw_req)
        raw_resp = reqs.find('response').text
        result[raw_req] = raw_resp
    return result

def parseRawHTTPReq(rawreq):   
    try:
        raw = rawreq.decode('utf8')
    except:
        raw = rawreq
    global headers,method,body,path
    headers = {}
    sp = raw.split('\r\n\r\n',1)
    if sp[1]!="":
        head=sp[0]
        body=sp[1]
    else:
        head = sp[0]
        body=""
    c1 = head.split('\n',head.count('\n'))
    method = c1[0].split(' ',2)[0]
    path = c1[0].split(' ',2)[1]
    for i in range(1, head.count('\n')+1):
        slice1 = c1[i].split(': ',1)
        if slice1[0] != "":
            try:
                headers[slice1[0]] = slice1[1]
            except:
                pass
    return headers,method,body,path

badwords = ['sleep','drop','uid','uname','select','waitfor','delay','system','union','order by','group by']
category = "bad"
def ExtractFeatures(method,path_enc,body_enc,headers):
    badwords_count = 0
    path = unquote_plus(path_enc)
    body = unquote(body_enc)
    single_q = path.count("'") + body.count("'")
    double_q = path.count("\"") + body.count("\"")
    dashes = path.count("--") + body.count("--")
    braces = path.count("(") + body.count("(")
    spaces = path.count(" ") + body.count(" ")
    for word in badwords:
        badwords_count += path.count(word) + body.count(word)
    for header in headers:
        badwords_count += headers[header].count(word)
    #if badwords_count-path.count('uid')-body.count('uid')-path.count('passw')-body.count('passwd')>0:
    #    category = 0
    return [method,path_enc.encode('utf-8').strip(),body_enc.encode('utf-8').strip(),single_q,double_q,dashes,braces,spaces,badwords_count,category]
    raw_input('>>>')
#Open the log file
f=open('demo_bad_responses.csv',"w")
c = csv.writer(f)
c.writerow(["method","path","body","single_q","double_q","dashes","braces","spaces","badwords","class"])
f.close()
#print(parse_log(log_path))
result = parse_log(log_path)

f = open('demo_bad_responses.csv','a')
c = csv.writer(f)
for items in result:
    #data = []
    raw = base64.b64decode(items)
    headers,method,body,path = parseRawHTTPReq(raw)
    #data.append(method)
    #data.append(body)
    #data.append(path)
    #data.append(headers)
    #f = open('httplog.csv','a')
    #c = csv.writer(f)
    data = ExtractFeatures(method,path,body,headers)
    c.writerow(data)
f.close()
