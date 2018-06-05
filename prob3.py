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
	
def probd(cur):
	print
	print("Results for 3d")
	query1 ="""
	SELECT PassRate, Subject, CRSE FROM (
		SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
			(
			SELECT COUNT(SID) totalS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S', 		'F', 'U', 'NS', 'NP')
			GROUP BY (Subject, CRSE)
			) Total
		NATURAL JOIN
			(
			SELECT COUNT(SID) PassS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P')
			GROUP BY (Subject, CRSE)
			) Pass
		) Rate
		ORDER BY PassRate DESC
	) N
	WHERE PassRate = (SELECT MIN(PassRate) FROM
	(
		SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
			(
			SELECT COUNT(SID) totalS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S', 		'F', 'U', 'NS', 'NP')
			GROUP BY (Subject, CRSE)
			) Total
		NATURAL JOIN
			(
			SELECT COUNT(SID) PassS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P')
			GROUP BY (Subject, CRSE)
			) Pass
		) Rate
	) X
	)
	;
	"""
	query2 = """
	SELECT PassRate, Subject, CRSE FROM (
		SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
			(
			SELECT COUNT(SID) totalS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S', 		'F', 'U', 'NS', 'NP')
			GROUP BY (Subject, CRSE)
			) Total
		NATURAL JOIN
			(
			SELECT COUNT(SID) PassS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S')
			GROUP BY (Subject, CRSE)
			) Pass
		) Rate
		ORDER BY PassRate DESC
	) N
	WHERE PassRate = (SELECT MAX(PassRate) FROM
	(
		SELECT ((PassS * 100.0)/ totalS) AS PassRate, Subject, CRSE FROM (
			(
			SELECT COUNT(SID) totalS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S', 		'F', 'U', 'NS', 'NP')
			GROUP BY (Subject, CRSE)
			) Total
		NATURAL JOIN
			(
			SELECT COUNT(SID) PassS, Subject, CRSE
			FROM Enrollment NATURAL JOIN Course
			WHERE Grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B+', 'C-', 'C', 'C+', 'D', 'D+', 'D-', 'P', 'S')
			GROUP BY (Subject, CRSE)
			) Pass
		) Rate
	) X
	)
	;
	"""
	print("Lowest Pass Rate:")
	cur.execute(query1)
	y = cur.fetchall()
	for row in y:
		print(row)
	print("Highest Pass Rate: ")
	cur.execute(query2)
	z = cur.fetchall()
	for row in z:
		print(row)
    

def probe(cur):
	print
	print("Results for 3e")
	print("Draft")

def probf(cur):	
	print
	print("Results for 3f")
	query1 = """SELECT Major, AvgGrade FROM
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'ABC'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	WHERE AvgGrade = (SELECT MAX(AvgGrade) FROM		
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'ABC'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	)
	;
	"""
	query2 = """SELECT Major, AvgGrade FROM
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'ABC'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	WHERE AvgGrade = (SELECT MIN(AvgGrade) FROM		
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'ABC'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	)
	;
	"""
	query3 = """SELECT Major, AvgGrade FROM
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'DEF'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	WHERE AvgGrade = (SELECT MAX(AvgGrade) FROM		
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'DEF'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	)
	;
	"""
	query4 = """SELECT Major, AvgGrade FROM
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'DEF'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	WHERE AvgGrade = (SELECT MIN(AvgGrade) FROM		
	(
		SELECT Major, AVG(GPA) AvgGrade FROM
		(
			SELECT Major, Subject, CRSE, Grade, GPA
			FROM NumGrade NATURAL JOIN
			(
				SELECT Major, Subject, CRSE, Grade
				FROM Enrollment NATURAL JOIN Course
				WHERE Subject = 'DEF'
			) EnCr
			WHERE Letter = Grade
		) EnCrGr
		GROUP BY Major
		ORDER BY AvgGrade
	) EnCrGrSelect
	)
	;
	"""
	
	print("Best Majors in ABC Courses")
	cur.execute(query1)
	y = cur.fetchall()
	for row in y:
		print(row)
	print("Worst Majors in ABC Courses")
	cur.execute(query2)
	y = cur.fetchall()
	for row in y:
		print(row)
	print("Best Majors in DEF Courses")
	cur.execute(query3)
	y = cur.fetchall()
	for row in y:
		print(row)
	print("Worst Majors in DEF Courses")
	cur.execute(query4)
	y = cur.fetchall()
	for row in y:
		print(row)

conn = psycopg2.connect("dbname=FakeUData")
cur = conn.cursor()

#proba(cur)
#probb(cur)
#probd(cur)
#probe(cur)
#probf(cur)

cur.close()
conn.close()

