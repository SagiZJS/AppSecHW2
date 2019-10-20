#from flask import Flask, escape, request, url_for
import flask as fl 

app = fl.Flask(__name__)

db = [['admin','123','123']]
   
def auth_cookie():
    
    cookie = None
    try:
        print("getting cookie")
        cookie = fl.request.cookies.get('username')
        print("cookie",cookie)
        for a in db:
            if (str(hash(a[0])) == cookie):
                print("cookie get")
                return fl.redirect(fl.url_for('spell_check'))
    except:
        pass
    return None
@app.route('/register',methods=['POST', 'GET'])
def register():
    print ("register")
    resp = auth_cookie()
    if (resp):
        return resp
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
    resp = auth_cookie()
    if (resp != None):
        return resp

    if fl.request.method == 'POST':
        failinfo = "Incorrect"
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
        
        return "<p id=\"result\">"+failinfo+"</p>"
    else:    
        return fl.render_template('login.html')

@app.route('/spell_check',methods=['GET','POST'])
def spell_check():
    resp = auth_cookie()
    if (not resp):
        return fl.redirect(fl.url_for("login"))
    if fl.request.method == 'POST':
        
        text = fl.request.form['input']
        fw = open("to_check.txt","w")
        fw.write(text)
        fw.close()
        fr = open("res.txt","r")
        import os
        os.system("./a.out to_check.txt wordlist.txt > res.txt")
        content = fr.read()
        if (content):
            content = content.replace("\n",",")[-1]
        fr.close()
        return "<h2>text:</h2><br><p id=\"textout\">"+text+"<h2>misspelled:</h2><br></p><br>"+"<p id=\"misspelled\">"+content+"</p>"
        
    else:
        return fl.render_template('spell_check.html')
