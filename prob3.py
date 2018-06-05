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
        cur.execute(test2)
        x = cur.fetchmany(20)
        for i in x:
            print(i)
    
conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()


#proba(cur)
#probb(cur)
#probc(cur)

cur.close()
conn.close()

