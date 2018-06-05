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
    SELECT Instructor, MIN(avgGrade)
    FROM 
        (SELECT AVG(Number) avgGrade, Instructor
        FROM Meeting NATURAL JOIN Enrollment NATURAL JOIN NumGrade
        GROUP BY Instructor) GradeInstr
    GROUP BY Instructor
    ;
    """    
    
    cur.execute(min_query)
    x = cur.fetchone()
    print("Hardest professor: " + str(x))
    
    max_query = """
    SELECT Instructor, MAX(avgGrade)
    FROM 
        (SELECT AVG(Number) avgGrade, Instructor
        FROM Meeting NATURAL JOIN Enrollment NATURAL JOIN NumGrade
        GROUP BY Instructor) GradeInstr
    GROUP BY Instructor    
    ;
    """    
    
    
    cur.execute(max_query)
    y = cur.fetchone()
    print("Easiest professor: " + str(y))
    
    
    
conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()

proba(cur)
probb(cur)

cur.close()
conn.close()

