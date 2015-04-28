"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

import sqlite3 # to use sql with python...

db_connection = sqlite3.connect("hackbright.db", check_same_thread=False)
# connecting to database
# we commit changes to the db over the db_connection 

db_cursor = db_connection.cursor()
# creating a cursor (similar to file_handle) to interact with the db
# we can use the cursor to execute a query
# its kind of like the command line--the cursor--its sending commands to SQL from python


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    # QUERY is uppercase like a constant, because we will never change the value of the Query string
    QUERY = """
        SELECT first_name, last_name, github
        FROM Students
        WHERE github = ? 
        """ 
        # don't need a semicolon at the end 
        # instead of a filter on the WHERE clause =...we put a "?"
        # the only thing we will change is the query "?"
        # it is acting like % in python strings, placeholder

    # executing the query with the cursor
    db_cursor.execute(QUERY, (github,))
    # second arg is a tuple (as insisted upon by SQLite) 
    # remember in python, 1-item tuples end with the comma 

    row = db_cursor.fetchone()
    # fetchone() method returns one row of data, as a (tuple)

    print "Student: %s %s\nGithub account: %s" % (
        row[0], row[1], row[2])
    # row is a tuple, fetched by fetchone
    # each item in the tuple corresponds to the SELECT statement above
    # first_name, last_name, github = row[0], row[1], row[2]

def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation 
    Given first_name, last_name, and github account"""

    QUERY = """INSERT INTO Students VALUES (?, ?, ?)"""
    # Query...all caps as a constant here, a string that will not change, (and only in the scope of this function!)
    db_cursor.execute(QUERY, (first_name, last_name, github))
    db_connection.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def project_by_title(project_title):
    """User inputs project_title, function queries DB for that project"""

    QUERY = """SELECT title, description 
            FROM Projects 
            WHERE title = ?"""

    db_cursor.execute(QUERY, (project_title,))

    answer = db_cursor.fetchone() 
    
    print answer[0], ":", answer[1]
    # print "Title: %s, Description: %s" % answer[0], answer[1]



def student_grade(github, project_title):
    """list a student's grade for the project, by github name
    JOINing Project table and Grades table"""

    QUERY= """SELECT grade
        FROM Grades 
        WHERE student_github = ? AND project_title = ?"""
    

    db_cursor.execute(QUERY, (github, project_title))

    grade_value = db_cursor.fetchone()

    print "%s's grade for %s: %s" % (github, project_title, grade_value)

def set_grade(github, project_title, grade_value):
    """...Update with a grade
    This would go in the grades table"""
    
    QUERY = """INSERT INTO Grades VALUES (?, ?, ?)"""
   
    db_cursor.execute(QUERY, (github, project_title, grade_value))
    db_connection.commit()

   
    # print "%s %s's grade: %s" % (first_name, last_name, grade)
    print "Successfully graded %s on Project %s: %s" % (github, project_title, grade_value)


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
                project_by_title(args[0]) 

        elif command == "gradequery":
            github, project_title = args
            student_grade(github, project_title)

        elif command == "entergrade":
            github, project_title, grade_value = args
            set_grade(github, project_title, grade_value)


if __name__ == "__main__":
    handle_input()

    # To be tidy, we'll close our database connection -- though, since this
    # is where our program ends, we'd quit anyway.

    db_connection.close() 
