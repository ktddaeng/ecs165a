import psycopg2

def proba(cur):
    cur.execute("select count(distinct SID) from student;")
    total_students = cur.fetchone()[0]
    for i in range(20):
        unit_compare = str(i+1)
        print(unit_compare)
        cur.execute("""
            SELECT unitSum, COUNT(SID) countSID FROM (
                SELECT CEIL(SUM(units)) unitSum, SID, Term
                FROM enrollment NATURAL JOIN Course
                WHERE Subject IN ('ABC','DEF')
                GROUP BY (Term, SID)
            ) StudentUnitSum
            GROUP BY unitSum
            HAVING unitSum = %s;""" %unit_compare)
        unit, count = cur.fetchone()
        print(count * 100 / total_students)

        
def probb(cur):
    min_query = """
    SELECT Instructor, avgGrade
    FROM (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) GradeInstr
    WHERE avgGrade = (SELECT MIN(avgGrade) FROM 
        (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) g2)
    ;
    """
    
    cur.execute(min_query)
    x = cur.fetchall()
    print("Hardest professor: ")
    for entry in x:
        print(entry)
    
    max_query = """
    SELECT Instructor, avgGrade
    FROM 
        (SELECT AVG(Number) avgGrade, Instructor
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) GradeInstr
    WHERE avgGrade = (SELECT MAX(avgGrade) FROM 
        (SELECT Instructor, AVG(Number) avgGrade
        FROM Meeting NATURAL JOIN (Enrollment INNER JOIN NumGrade on Enrollment.grade = NumGrade.letter)
        GROUP BY Instructor) g2)
    ;
    """    
    
    cur.execute(max_query)
    y = cur.fetchall()
    print("\nEasiest professor: ")
    for entry in y:
        print(entry)
    
def probc(cur):
    for i in range(20):
        q = """
        SELECT sumUnits, (SUM(GPA * sumUnits) / SUM(sumUnits)) weighedGPA
        FROM
            (SELECT SID, TERM, SUM(UNITS) sumUnits, GPA
            FROM ENROLLMENT NATURAL LEFT JOIN NUMGRADE
            GROUP BY SID, TERM, GPA) StudentGPA
        WHERE sumUnits > 0
        GROUP BY sumUnits
        HAVING sumUnits = %s
        ;
        """ %(str(i+1))
                                              
        cur.execute(q)
        x = cur.fetchone()
        for i in x:
            print(i)
            
            
def probe(cur):
    q = """
    SELECT DISTINCT(Meet1.Subject, Meet1.CRSE), 
        Meet2.Subject, Meet2.CRSE
    FROM (Meeting NATURAL JOIN Course) Meet1, 
        (Meeting NATURAL JOIN Course) Meet2
    WHERE Meet1.Term::text NOT LIKE '%03'
        AND Meet2.Term::text NOT LIKE '%03' 
        AND Meet1.Time NOT LIKE '%NA%' AND Meet2.Time NOT LIKE '%NA%'
        AND Meet1.Days NOT LIKE '%NA%' AND Meet2.Days NOT LIKE '%NA%'
        AND Meet1.Building NOT LIKE '%NA%' AND Meet2.Building NOT LIKE '%NA%'
        AND Meet1.Room NOT LIKE '%NA%' AND Meet2.Room NOT LIKE '%NA%'
        AND Meet1.CRSE < Meet2.CRSE
        AND Meet1.Time = Meet2.Time
        AND Meet1.Term = Meet2.Term
        AND Meet1.Days = Meet2.Days
        AND Meet1.Room = Meet2.Room 
        AND Meet1.Building = Meet2.Building
        AND Meet1.Instructor = Meet2.Instructor
    ORDER BY (Meet1.Subject, Meet1.CRSE)
    ;
    """
                                              
    cur.execute(q)
    x = cur.fetchall()
    for i in x:
        print(i)

            
conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()


#proba(cur)
#probb(cur)
#probc(cur)
probe(cur)

cur.close()
conn.close()

