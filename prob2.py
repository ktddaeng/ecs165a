
# coding: utf-8

# In[51]:
import sys
import csv
import os
import glob
import tarfile
import io
import psycopg2
import pandas as pd
from collections import OrderedDict

# In[55]:

class Course:
    def __init__(self, cid, term):
        self.cid = cid
        self.term = term
        self.info = OrderedDict()
        self.meetings = []
        self.enrollment = pd.DataFrame(columns=['SEAT', 'SID', 'SURNAME', 'PREFNAME', 'LEVEL', 'UNITS', 'CLASS', 'MAJOR', 'GRADE', 'STATUS', 'EMAIL'])
    
    def add_meeting(self, meeting):
        if type(meeting) == dict:
            self.meetings.append(meeting)
        elif type(meeting) == list:
            self.meetings.extend(meeting)
            
    def add_enrollment(self, df):
        self.enrollment = df
            
    def add_course_info(self, course_info):
        self.info = course_info


# In[56]:

def determine_row_type(big_list):
    if big_list[0][0] == "CID":
        return("CID")
        # class information
        # read one more line to get class information
        
    elif big_list[0][0] == "INSTRUCTOR(S)":
        return("meet")
        
    elif big_list[0][0] == "SEAT":
        return("enroll")
    else:
        print("Don't know how to handle " + str(big_list[0][0]))


# In[99]:

def parse_CID(big_list):
    d = OrderedDict()
    
    if len(big_list) > 2:
            print("List longer than 2 " + str(big_list))
            
    if len(big_list) == 1:
        d = OrderedDict()
        d["CID"] = None
        d["TERM"] = None
        d["SUBJ"] = None
        d["CRSE"] = None
        d["SEC"] = None
        d["UNITS"] = None
        return(d)
    else:
        try:
            li = big_list[1]
            if len(li) != 6:
                print("Length of Course is not 6. Re-evaluate " + str(li))
            li = ['NULL' if j == '' else j for j in li]
            d["CID"] = li[0]
            d["TERM"] = li[1]
            d["SUBJ"] = li[2]
            d["CRSE"] = li[3]
            d["SEC"] = li[4]
            d["UNITS"] = li[5]
            return(d)

        except:
            print("Error when parsing CID")


# In[118]:

def parse_meeting(big_list):
    d = OrderedDict()
    if len(big_list) == 1: # no listings
        d["INSTR"] = None
        d["TYPE"] = None
        d["DAYS"] = None
        d["TIME"] = None
        d["BUILD"] = None
        d["ROOM"] = None
        return d
    
    try:
        meeting_list = []
        for idx, li in enumerate(big_list):
        
            duplicate = False
            if idx == 0: # skip over header
                continue
            d = OrderedDict()
            if idx == 1:
                first_instructor = li[0].replace("'", "''")
                
            if len(big_list) > 1 and idx > 1 and li[0] == '' and li[2] == '' and li[3] == '' and li[4] == '' and li[5] == '':
                continue
                
            if li[0] == '' and idx > 1:
                d["INSTR"] = first_instructor
                li[0] = first_instructor
            else:
                d["INSTR"] = li[0].replace("'", "''")
                
            if idx > 1 and li[1] == '' and li[2] == '' and li[3] == '' and li[4] == '' and li[5] == '' and li[0] != '':
                temp_instructor = li[0].replace("'", "''")
                w = dict(meeting_list[-1])
                w["INSTR"] = temp_instructor
                meeting_list.append(w)
                continue
                
            if li[3] == '':
                d["TIME"] = "NA"
            else:
                d["TIME"] = li[3]
                
            if li[4] == '':
                d["BUILD"] = "NA"
            else:
                d["BUILD"] = li[4]
                
            if li[2] == '':
                d["DAYS"] = "NA"
            else:
                d["DAYS"] = li[2]
            
            if li[5] == '':
                d["ROOM"] = "NA"
            else:
                d["ROOM"] = li[5]
                
            for i in range(idx):
                #print("Big list: " + str(big_list[i]) + "\t" + "li: " + str(li) + "\n")
                if big_list[i] == li:
                    #print(big_list)
                    duplicate = True
                    break
                    
            if duplicate == True:
                continue
                
            if len(li) != 6:
                print("Length of meeting is not 6. Re-evaluate " + str(li))

            li = ['NULL' if j == '' else j for j in li]
            
            d["TYPE"] = li[1]
            #d["DAYS"] = li[2]
            #d["TIME"] = li[3]
            #d["BUILD"] = li[4]
            #d["ROOM"] = li[5]
            
            meeting_list.append(d)
            
            
        return(meeting_list)
    
    except:
        print("Error when parsing Meeting " + str(big_list))


# In[121]:

def parse_enrollment(big_list):
    cols = ['SEAT', 'SID', 'SURNAME', 'PREFNAME', 'LEVEL', 'UNITS', 'CLASS', 'MAJOR', 'GRADE', 'STATUS', 'EMAIL']
    df = pd.DataFrame(columns=cols)
    
    if len(big_list) == 0: # no listings
        return df
    
    #try:
    for li in big_list[1:]:
        if len(li) != 11:
            print("Length of enrollment is not 11. Re-evaluate " + str(li))
        li = ['NULL' if j == '' else j for j in li]
        d = {}
        d["SEAT"] = li[0]
        d["SID"] = li[1]
        d["SURNAME"] = li[2].replace("'", "''")
        d["PREFNAME"] = li[3].replace("'", "''")
        d["LEVEL"] = li[4]
        d["UNITS"] = li[5]
        d["CLASS"] = li[6]
        d["MAJOR"] = li[7]
        d["GRADE"] = li[8]
        d["STATUS"] = li[9]
        d["EMAIL"] = li[10].replace("'", "''")
        df = df.append(d, ignore_index=True)
    return(df)
    
    
def extract_meeting_from_class(course):
    rows = []
    cid = course.cid
    term = course.term
    for meet in course.meetings:
        rows.append((cid, term, meet['TYPE'], meet['DAYS'], meet['INSTR'], meet['TIME'], meet['BUILD'], meet['ROOM']))
    values = ", ".join(map(str, rows))
    return values

def extract_enrollment_from_class(course):
    rows = []
    cid = course.cid
    term = course.term
    for index, enroll in course.enrollment.iterrows():
        rows.append((enroll['SID'], cid, term, enroll['GRADE'], enroll['MAJOR'], enroll['UNITS'], enroll['CLASS'], \
                    enroll['SEAT'], enroll['STATUS'], enroll['LEVEL']))
    values = ", ".join(map(str, rows))
    return values

def extract_student_from_class(course):
    rows = []
    for index, enroll in course.enrollment.iterrows():
        rows.append((enroll['SID'], enroll['SURNAME'], enroll['PREFNAME'], enroll['EMAIL']))
    values = ", ".join(map(str, rows))
    return values
    
conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()


cur.execute('CREATE TABLE Course(CID integer, Term INTEGER, Subject CHAR(3), Section INTEGER, CRSE INTEGER, UnitRange CHAR(18), PRIMARY KEY(CID, Term));')

cur.execute('CREATE TABLE Meeting(CID integer, Term INTEGER, Type CHAR(25), \
Days CHAR(5), Instructor CHAR(30), Time CHAR(20), Building CHAR(4), \
Room CHAR(7), PRIMARY KEY(CID, Term, Instructor, Type, Time, Days, Building, Room));')
#, PRIMARY KEY(CID, Term, Instructor, Type)

cur.execute('CREATE TABLE Enrollment(RN serial, SID integer, CID integer, Term INTEGER, Grade CHAR(4), Major CHAR(5), Units FLOAT, Class CHAR(5), Seat INTEGER, Status CHAR(5), Level CHAR(5), PRIMARY KEY(CID, Term, SID));')

cur.execute('CREATE TABLE Student(SID integer, Surname CHAR(20), \
Prefname CHAR(20), Email CHAR(40), PRIMARY KEY(SID));')

cur.execute('CREATE TABLE NumGrade(Letter CHAR(4), Number FLOAT, GPA FLOAT, PRIMARY KEY(Letter));')

lgrades = ["A+","A","A-","B+","B","B-","C+","C","C-","D+","D","D-","F"]
ngrades = [99,95,91,89,85,81,79,75,71,69,65,61,59]
gpa = [4.0,4.0,3.67, 3.33,3.0,2.67, 2.33,2.0,1.67, 1.33, 1.0, 0.67,0]
gradevals = ', '.join(map(str, [(lgrades[i], ngrades[i],gpa[i]) for i in range(len(lgrades))]))

sql = "INSERT INTO NumGrade(Letter, Number, GPA) VALUES {};".format(gradevals)
cur.execute(sql)


#tar = tarfile.open("Grades.tgz", "r:gz")

courses = {}

direc = sys.argv[1]
extension = 'csv'
os.chdir(direc)

files = [i for i in glob.glob('*.{}'.format(extension))]
#files = os.listdir(direc) # change this to be working directory

i = 0
courses = {}
for f in files:
    #print(f)

    with open(f, 'r') as csv_file:
        big_list = []
        #csv_file = io.StringIO(f.read().decode('ascii'))
        reader = csv.reader(csv_file)
        try:
            content = list(reader)
        except:
            print("Couldn't do file " + f)
            continue
        csv_length = len(content)

        for idx, row in enumerate(content):
            if row != [''] and idx < csv_length:
                big_list.append(row)
                if idx < csv_length - 1:
                    continue
                
            if big_list != []:
                row_type = determine_row_type(big_list)
                if row_type == "CID":
                    info = parse_CID(big_list)
                    (cid, term) = big_list[1][0], big_list[1][1]
                    x = Course(big_list[1][0], big_list[1][1])
                    x.add_course_info(info)
                    
                if row_type == "meet":
                    meeting = parse_meeting(big_list)
                    x.add_meeting(meeting)
                    
                if row_type == "enroll":
                    enroll = parse_enrollment(big_list)
                    x.add_enrollment(enroll)
                    courses[(cid, term)] = x
                    
            if row == ['']:
                big_list = []

    c_rows = [tuple(d.info.values()) for d in list(courses.values()) if d.enrollment.empty == False]
    values = ", ".join(map(str, c_rows))
    sql = "INSERT INTO Course(CID, Term, Subject, CRSE, Section, UnitRange) VALUES {};".format(values).replace("'NULL'","NULL")
    cur.execute(sql)

    m_rows = [extract_meeting_from_class(course) for course in courses.values() if course.enrollment.empty == False]
    values = ", ".join(map(str, m_rows))
    something = ['44095', '198906', 'Discussion', None, 'Sullivan, Jordan H.', None, None, None]
    #cur.execute("INSERT INTO Meeting(CID, Term, Type, Days, Instructor, Time, Building, Room) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (tuple(something)))
    sql = "INSERT INTO Meeting(CID, Term, Type, Days, Instructor, Time, Building, Room) VALUES {};".format(values).replace("'NULL'","NULL").replace('"', "'")
    cur.execute(sql)

    e_rows = [extract_enrollment_from_class(course) for course in courses.values() if course.enrollment.empty == False]
    values = ", ".join(map(str, e_rows))
    sql = "INSERT INTO Enrollment(SID, CID, Term, Grade, Major, Units, Class, Seat, Status, Level) VALUES {};".format(values).replace("'NULL'","NULL").replace('"', "'")
    cur.execute(sql)

    s_rows = [extract_student_from_class(course) for course in courses.values() if course.enrollment.empty == False]
    values = ", ".join(map(str, s_rows))
    sql = "INSERT INTO Student(SID, Surname, Prefname, Email) VALUES {} ON CONFLICT(SID) DO NOTHING;".format(values).replace("'NULL'","NULL").replace('"', "'")
    courses = {}
    cur.execute(sql)


conn.commit()


# In[ ]:

cur.close()
conn.close()

