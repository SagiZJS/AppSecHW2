import requests
import re
url ="http://localhost:5000/"
cookies = {}
def test_admin():
    # admin 
    admindata={"username":"admin", "password":"123","twofa":"123"}
    resp = requests.post(url+"login",admindata)

    cookies = resp.cookies.get_dict()
    f = open("test1.txt","r")
    s = f.read()
    f.close()
    spelldata = {"input":s}
    resp = requests.get(url+"spell_check",cookies=cookies)
    content = resp.content.decode("utf-8")
    assert r'id="inputtext"' in content
    m = re.search(r'id="csrftoken" value = ([\w]+)',content)
    token=m.group(1)
    spelldata['CSRFToken']=token
    resp = requests.post(url+"spell_check",spelldata,cookies=cookies)
    content = resp.content.decode("utf-8")
    assert r'id="textout"' in content
    assert r'id="misspelled"' in content

def test_register():
    resp = requests.get(url+"register")
    content = resp.content.decode("utf-8")
    #print(content)
    assert r'id="uname"' in content
    assert r'id="pword"' in content
    assert r'id="2fa"' in content
    data = {"username":"Sagi","password":"Sagi","twofa":"2340000000"}
    resp = requests.post(url+"register",data)
    content = resp.content.decode("utf-8")
    #print(content)
    assert r'id="success"' in content
    assert r'success' in content


def test_login():
    resp = requests.get(url+"login")
    content = (resp.content).decode("utf-8")
    assert r'id="uname"' in content
    assert r'id="pword"' in content
    assert r'id="2fa"' in content
    
    data = {"username":"Sagi","password":"Sagi","twofa":"2340000000"}
    resp = requests.post(url+"login",data)
    content = resp.content.decode("utf-8")
    cookies = resp.cookies.get_dict()
    assert r'id="result"' in content
    assert r'success' in content
    data['password']="sagi"
    resp = requests.post(url+"login",data)
    content = resp.content.decode("utf-8")
    assert r'id="result"' in content
    assert r'Incorrect' in content



test_register()
test_login()
test_admin()
