from flask import Flask, render_template, request, url_for, redirect, session
from flask_pymongo import pymongo
from django.template.defaulttags import register
import bcrypt
import dns
import os
from datetime import date
from flask_simple_captcha import CAPTCHA

app = Flask(__name__)
app.secret_key = "tattoo"

client = pymongo.MongoClient(
    "mongodb+srv://Jamie:mrwood@cluster0.knsvc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
)

db = client.get_database('users')
records = db.register

CAPTCHA_CONFIG = {
    'SECRET_CSRF_KEY': 'wMmeltW4mhwidorQRli6Oijuhygtfgybunxx9VPXldz'
}
CAPTCHA = CAPTCHA(config=CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)

#STATIC VARIABLES
def get_Class(period):
    return disw[weekdayint].get(period)

def get_TimetableColor(subject):
    return timetablecolors.get(subject)


daysinweek = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday"
]

#STATIC timetable
monday = {
    "p1": "Math",
    "p2": "English",
    "p3": "Geography",
    "p4": "Science",
    "p5": "PE"
}
tuesday = {
    "p1": "DT",
    "p2": "Music",
    "p3": "Dance",
    "p4": "English",
    "p5": "Art"
}
wednesday = {
    "p1": "Math",
    "p2": "Music",
    "p3": "Geography",
    "p4": "Science",
    "p5": "DT"
}
thursday = {
    "p1": "English",
    "p2": "English",
    "p3": "Geography",
    "p4": "Art",
    "p5": "Science"
}
friday = {
    "p1": "Dance",
    "p2": "Dance",
    "p3": "Geography",
    "p4": "Art",
    "p5": "Science"
}

#sample timetable colors
timetablecolors = {
    "Math": "#800080",
    "English": "#0080ff",
    "Geography": "#00cc00",
    "Science": "#ff9900",
    "PE": "#ff0000",
    "DT": "#663300",
    "Dance": "#000000",
    "Art": "#ff00ff",
    "Music": "#808080"
}

#disw:days in school week
#dictionarys' above nestled in disw
disw = [monday, tuesday, wednesday, thursday, friday]

username = "Jamie"

my_date = date.today()
weekdayint = 2
#weekdayint = my_date.weekday()
dateformat = my_date.strftime("%B %d %Y")

weekdayword = daysinweek[weekdayint]
numclasses = 0

if weekdayint > 4:
    numclasses = 0
else:
    numclasses = len(disw[weekdayint])

#period 1
tsubject1 = get_Class("p1")
tcolor1 = get_TimetableColor(tsubject1)

#period 2
tsubject2 = get_Class("p2")
tcolor2 = get_TimetableColor(tsubject2)

#period 3
tsubject3 = get_Class("p3")
tcolor3 = get_TimetableColor(tsubject3)

#period 4
tsubject4 = get_Class("p4")
tcolor4 = get_TimetableColor(tsubject4)

#period 5
tsubject5 = get_Class("p5")
tcolor5 = get_TimetableColor(tsubject5)

#END of STATIC VARIABLES

#PYTHON ---> HTML
@app.route('/')
def index():
    if "uname" in session:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("signup"))


@app.route('/dashboard')
def dashboard():
    if "uname" in session:
        uname = session["uname"]
        return render_template('dashboard.html',
                               user=uname,
                               #
                               # STATIC VARIABLES
                               # \/
                               classes=numclasses,
                               dateformat=dateformat,
                               day=weekdayword,
                               period1=tsubject1,
                               color1=tcolor1,
                               period2=tsubject2,
                               color2=tcolor2,
                               period3=tsubject3,
                               color3=tcolor3,
                               period4=tsubject4,
                               color4=tcolor4,
                               period5=tsubject5,
                               color5=tcolor5)
    else:
        return redirect(url_for("signup"))


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if "uname" in session:
        uname = session["uname"]
        userdata = db.users.find_one({'username': uname})
        fname = userdata.get('firstname')
        lname = userdata.get('lastname')

        if request.method == "POST":
            message = ''

            cpassword = request.form.get("cpassword")
            npassword = request.form.get("npassword")

            passwordcheck = userdata.get('password')

            if bcrypt.checkpw(cpassword.encode('utf-8'), passwordcheck):
                #Encrypting new password
                hashed = bcrypt.hashpw(npassword.encode('utf-8'),
                                       bcrypt.gensalt())
                #Updating database

                userdata.update({'password': hashed})
                db.users.updateUser(uname, [userdata])

                message = 'Password successfully changed'

                return render_template('profile.html',
                                       user=uname,
                                       fname=fname,
                                       lname=lname,
                                       message=message)

        else:
            return render_template('profile.html',
                                   user=uname,
                                   fname=fname,
                                   lname=lname)
    else:
        return redirect(url_for("signup"))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if "uname" in session:
        return redirect(url_for("/"))
    else:
        message = ''

        if request.method == "POST":
            #Failed to introduce CAPTCHA due to time constraints
            # ------
            #c_hash = request.form.get('captcha-hash')
            #c_text = request.form.get('captcha-text')
            #if CAPTCHA.verify(c_text, c_hash):
            #return 'success'
            #else:
            #message = 'CAPTCHA Failed'
            #return render_template('signup.html', message=message)
            # ------

            uname = request.form.get("username")
            fname = request.form.get("fname")
            lname = request.form.get("lname")

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            user_found = db.users.find_one({"username": uname})

            if user_found:
                message = 'There already is a user by that name'
                return render_template('signup.html', message=message)
            if password1 != password2:
                message = 'Passwords should match!'
                return render_template('signup.html', message=message)
            else:
                hashed = bcrypt.hashpw(password2.encode('utf-8'),
                                       bcrypt.gensalt())
                user_input = {
                    'username': uname,
                    'firstname': fname,
                    'lastname': lname,
                    'password': hashed
                }
                db.users.insert_one(user_input)

                message = 'Account successfully created'
                return render_template('signup.html', message=message)

        if request.method == 'GET':
            captcha = CAPTCHA.create()
            return render_template('signup.html', captcha=captcha)
        else:
            return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "uname" in session:
        return redirect(url_for("/"))
    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("password")

        user_found = db.users.find_one({"username": uname})

        if user_found:
            user_val = user_found['username']
            passwordcheck = user_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["uname"] = user_val
                return redirect(url_for('dashboard'))
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Username does not exist'
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')

@app.route("/timetable", methods=["POST", "GET"])
def timetable():
    if "uname" in session:
        uname = session["uname"]
        createdtimetable = db.timetable.find({"username":uname}).count() > 0;
        if createdtimetable == True:
            record = db.timetable.find_one({"username": uname})
            timetable = record["timetable"]

            return render_template('timetable.html', timetable=timetable)

        else:
            return redirect(url_for("timetablesetup"))
            
            


@app.route('/timetablesetup', methods=['GET', 'POST'])
def timetablesetup():
    if "uname" in session:
        if request.method == "POST":
            info = {}

            classnum = request.form.get("classnum")
            try:
              int(classnum)
            except:
              message = 'An error occured with classnum'
              return render_template('createtimetable1.html', message=message)
            
            classlen = request.form.get("classlength")
            try:
              int(classlen)
            except:
              message = 'An error occured with classlen'
              return render_template('createtimetable1.html', message=message)
            
            periodsperday = request.form.get("subjectsperday")
            try:
              int(periodsperday)
            except:
              message = 'An error occured with periodsperday'
              return render_template('createtimetable1.html', message=message)

            weekrotation = request.form.get("rotation")
            if weekrotation == "lettered":
                weekrotation = ["A","B"]
            elif weekrotation == "numbered":
                weekrotation = ["1","2"]
            elif weekrotation == "single":
                weekrotation = [" "]
            else:
                message = "Error with weekrotation var"
            
            weekend = request.form.get("weekend")
            if weekend == "sat-sun":
                workweek = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
            elif weekend == "fri-sat":
                workweek = ["Sunday","Monday","Tuesday","Wednesday","Thursday"]
            elif weekend == "sun-only":
                workweek = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
            else:
                message = "Error with weekend var"
            

            info["classnum"] = classnum
            info["classlen"] = classlen
            info["periodsperday"] = periodsperday
            info["weekrotation"] = weekrotation
            info["workweek"] = workweek

            session["info"] = info
            return redirect(url_for("timetablesetup2"))

        else:
            return render_template('createtimetable1.html')
    else:
        return redirect(url_for("/signup"))

@app.route('/timetablesetup2', methods=['GET', 'POST'])
def timetablesetup2():
    if "info" in session:

        uname = session["uname"]
        info = session["info"]

        classnum = info["classnum"]
        classnum = int(classnum)
        classlen = info["classlen"]
        classlen = int(classlen)


        if request.method == "POST":

            newrecord = {"username":uname,
                          "info":info}

            def insert_Subject(x):
                x = str(x)
                subject = "s" + x
                color = "s" + x + "col"
                subjectnamevalue = request.form.get(subject)
                subjectcolorvalue = request.form.get(color)
                subjectmaster = {"name":subjectnamevalue,"color":subjectcolorvalue}
                return subjectmaster

            subjects = {}
            x = 1
            while x != classnum + 1:
                subjectkey = "subject" + str(x)
                subjects[subjectkey] = insert_Subject(x)
                x = int(x)
                x += 1
            
            newrecord["subjects"] = subjects
            session.pop("info", None)
            session["newrecord"] = newrecord
            return redirect(url_for("timetablesetup3"))
            
        else:
            def new_Record(x):
              if x <= classnum:
                  return "block"
              else:
                  return "none"

            return render_template('createtimetable2.html', 
                                  ifs1 = new_Record(1), 
                                  ifs2 = new_Record(2), 
                                  ifs3 = new_Record(3), 
                                  ifs4 = new_Record(4), 
                                  ifs5 = new_Record(5), 
                                  ifs6 = new_Record(6), 
                                  ifs7 = new_Record(7), 
                                  ifs8 = new_Record(8), 
                                  ifs9 = new_Record(9), 
                                  ifs10 = new_Record(10), 
                                  ifs11 = new_Record(11), 
                                  ifs12 = new_Record(12))
    else:
        return redirect(url_for("/timetablesetup"))

@app.route("/timetablesetup3", methods=["POST", "GET"])
def timetablesetup3():
    if "newrecord" in session:
        newrecord = session["newrecord"]

        periodsperday = int(newrecord["info"]["periodsperday"])
        classnum = int(newrecord["info"]["classnum"])
        workweek = newrecord["info"]["workweek"]
        weekrotation = newrecord["info"]["weekrotation"]

        periodarray = [0,0,0]
        timetable = {}

        if request.method == "POST":
            #Getting values & inserting into Mongo from table
            for week in range(len(weekrotation)):
                weekdic = {}

                for day in range(len(workweek)):
                    weekdic[workweek[day]] = {}

                    for period in range(periodsperday):
                            
                        periodstr = str(periodarray[0]) + "-" + str(periodarray[1]) + "-" + str(periodarray[2])
                        newperiod = request.form.get(periodstr)
                        if newperiod is not None and (newperiod != " --- "):
                            u = "period" + str(period)
                            weekdic[workweek[day]][u] = newperiod
                        
                        period += 1
                        periodarray[2] = period
                    day += 1
                    periodarray[1] = day
                
                weekname = "week" + weekrotation[week]
                timetable[weekname] = weekdic

                week += 1
                periodarray[0] = week
            

            newrecord["timetable"] = timetable
            db.timetable.insert_one(newrecord)
            
            return redirect(url_for("dashboard"))
        else:
            subjectsinarray = [" --- "]
            for i in range(classnum):
                i += 1
                s = "subject" + str(i)
                subjectsinarray.append(newrecord["subjects"][s]["name"])
            
            if weekrotation == ['A', 'B'] or ['1','2']:
                weekrotationid = ['0','1']
            elif weekrotation == [' ']:
                weekrotationid = ['0']

            return render_template('createtimetable3.html',
                                    periodsperday = periodsperday,
                                    subjectsinarray = subjectsinarray,
                                    workweek = workweek,
                                    weekrotation = weekrotation,
                                    weekrotationid = weekrotationid)
    
    else:
        return redirect(url_for("/timetablesetup"))


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "uname" in session:
        session.pop("uname", None)
        return render_template('logout.html')
    else:
        return redirect(url_for("signup"))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


app.run('0.0.0.0', 8080)