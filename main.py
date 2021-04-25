from flask import Flask, render_template, request

app = Flask(__name__)
from datetime import date

#timetable
def get_Class(period):
    disw[weekdayint].get(period)

def get_TimetableColor(subject):
  timetablecolors.get(subject)


daysinweek = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday"
]

#sample timetable
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
    "Music":"#808080"
}

#disw:days in school week
#dictionarys' above nestled in disw
disw = [monday, tuesday, wednesday, thursday, friday]

username = "Jamie"

my_date = date.today()
weekdayint = 1
#weekdayint = my_date.weekday()
dateformat = my_date.strftime("%B %d %Y")

weekdayword = daysinweek[weekdayint]
numclasses = 0

if weekdayint > 4:
    numclasses = 0
else:
    numclasses = len(disw[weekdayint])

#period 1
tsubject1 = disw[weekdayint].get("p1")
tcolor1 = timetablecolors.get(tsubject1)

#period 2
tsubject2 = disw[weekdayint].get("p2")
tcolor2 = timetablecolors.get(tsubject2)

#period 3
tsubject3 = disw[weekdayint].get("p3")
tcolor3 = timetablecolors.get(tsubject3)

#period 4
tsubject4 = disw[weekdayint].get("p4")
tcolor4 = timetablecolors.get(tsubject4)

#period 5
tsubject5 = disw[weekdayint].get("p5")
tcolor5 = timetablecolors.get(tsubject5)



@app.route('/')
def index():
    return render_template('index.html',
                           user=username,
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
                           color5=tcolor5
                           )


app.run('0.0.0.0', 8080)