#from flask import Flask, escape, request, url_for
import flask as fl 
import random

app = fl.Flask(__name__)

db = [['admin','123','123']]
tokens={}
   
def auth_cookie():
    
    cookie = None
    try:
        print("getting cookie")
        cookie = fl.request.cookies.get('username')
        print("cookie",cookie)
        for a in db:
            if (str(hash(a[0])) == cookie):
                print("cookie get")
                return a[0]
    except:
        pass
    return False
@app.route('/register',methods=['POST', 'GET'])
def register():
    print ("register")
    resp = auth_cookie()
    if (resp):
        return fl.render_template('login_success.html')
    if (fl.request.method == 'POST'):
        username = fl.request.form['username']
        password = fl.request.form['password']
        twofa = fl.request.form['twofa']
        if ((not username) or (not password) or (not twofa)):
            return fl.render_template('register_failure.html')
        for a in db:
            if username == a[0]:
                return fl.render_template('register_failure.html')
        db.append([username,password,twofa])
        return fl.render_template('register_success.html')
    else:
        
        return fl.render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    print ("login")
    if (auth_cookie()):
        return fl.render_template('login_success.html')

    if fl.request.method == 'POST':
        for a in db:
            username = fl.request.form['username']
            password = fl.request.form['password']
            twofa = fl.request.form['twofa'] 
            if (username == a[0] and password == a[1]):
                if (twofa != a[2]):
                    failinfo = "Two-factor failure"
                    break
                resp = fl.make_response(fl.render_template('login_success.html'))
                resp.set_cookie('username', str(hash(username)))
                return resp
        
        return fl.render_template('login_failure.html')
    else:    
        return fl.render_template('login.html', )

@app.route('/spell_check',methods=['GET','POST'])
def spell_check():
    resp = auth_cookie()
    if (not resp):
        return fl.render_template('login_failure.html')
    if fl.request.method == 'POST':
        token = fl.request.form['CSRFToken']
        print("POST",token)
        print("POST tokens",tokens[resp])
        print(type(token),len(token))
        print(type(tokens[resp]),len(tokens[resp]))
        if (tokens[resp] != token): 
            return fl.render_template('login_failure.html')
        text = fl.request.form['input']
        fw = open("to_check.txt","w")
        fw.write(text)
        fw.close()
        fr = open("res.txt","r")
        import os
        os.system("./a.out to_check.txt wordlist.txt > res.txt")
        content = fr.read()
        fr.close()
        print(content)
        if (content):
            content = content.replace("\n",",")[:-1]
        print(content)
        return "<h2>text:</h2><br><p id=\"textout\">"+text+"<h2>misspelled:</h2><br></p><br>"+"<p id=\"misspelled\">"+content+"</p>"
        
    else:
        token = random.randint(0, 10000000)
        print(token)
        tokens[resp] = str(token)
        print(tokens[resp])
        
        return fl.render_template('spell_check.html', csrftoken=token)
