#from flask import Flask, escape, request, url_for
import flask as fl 
import random

app = fl.Flask(__name__)
app.config.update(
    #
    SESSION_COOKIE_HTTPONLY=True,
    #SESSION_COOKIE_SECURE=True,
    #SESSION_COOKIE_SMAESITE=True,
)

db = [['admin','123','123']]
tokens={}
   
def valid_userinfo(s):
    for i in range(len(s)):
        if (not ((s[i]>='A' and s[i] <= 'Z') or (s[i] >= 'a' and s[i] <= 'z') or (s[i]>='0' and s[i] <='9'))):
            return False
    return True
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
        if (not (valid_userinfo(username) and valid_userinfo(password) and valid_userinfo(twofa) ) ):
            return fl.render_template('register.html',error="username/password/twofa syntax error, should only contains letters and numerics")
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
            if (not(valid_userinfo(username) and valid_userinfo(password) and valid_userinfo(twofa))):
                return fl.render_template('login.html',error="username/password/twofa syntax error, should only contains letters and numerics")
            if (username == a[0] and password == a[1]):
                if (twofa != a[2]):
                    failinfo = "Two-factor failure"
                    break
                resp = fl.make_response(fl.render_template('login_success.html'))
                resp.set_cookie('username', str(hash(username)))
                return resp
        
        return fl.render_template('login_failure.html')
    else:    
        return fl.render_template('login.html')

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
        import os
        os.system("./a.out to_check.txt wordlist.txt > res.txt")
        fr = open("res.txt","r")
        content = fr.read()
        fr.close()
        print(content)
        if (content):
            content = content.replace("\n",",")[:-1]
        print(fl.escape(content))
        return fl.render_template("spell_check_result.html",text=text,result=content)
    else:
        token = random.randint(0, 10000000)
        print(token)
        tokens[resp] = str(token)
        print(tokens[resp])
        
        return fl.render_template('spell_check.html', csrftoken=token)
