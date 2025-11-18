# python_solution.py
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Create connection to SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to SQLite database successfully")
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
    return conn


def create_tables(conn):
    """Create tables according to Homework 1 structure"""
    try:
        cursor = conn.cursor()

        # Create groups table (using quotes because "group" is a keyword)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "group" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create students table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES "group" (id)
            )
        ''')

        # Create lecturers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecturer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create subjects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subject (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')

        # Create schedule table (linking subjects and lecturers)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER,
                lecturer_id INTEGER,
                FOREIGN KEY (subject_id) REFERENCES subject (id),
                FOREIGN KEY (lecturer_id) REFERENCES lecturer (id)
            )
        ''')

        print("Tables created successfully")

    except Error as e:
        print(f"Error creating tables: {e}")


def insert_sample_data(conn):
    """Insert sample data with English values"""
    try:
        cursor = conn.cursor()

        # Add groups
        groups = [
            ('Group A',),
            ('Group B',),
            ('Group C',)
        ]
        cursor.executemany('INSERT INTO "group" (name) VALUES (?)', groups)

        # Add students
        students = [
            ('John Smith', 1),
            ('Maria Johnson', 1),
            ('Peter Brown', 2),
            ('Anna Davis', 2),
            ('Michael Wilson', 3),
            ('Sarah Miller', 3)
        ]
        cursor.executemany('INSERT INTO student (name, group_id) VALUES (?, ?)', students)

        # Add lecturers
        lecturers = [
            ('Dr. Robert Taylor',),
            ('Prof. Elizabeth White',),
            ('Dr. James Anderson',),
            ('Prof. Patricia Thomas',)
        ]
        cursor.executemany('INSERT INTO lecturer (name) VALUES (?)', lecturers)

        # Add subjects
        subjects = [
            ('Mathematics',),
            ('Physics',),
            ('Computer Science',),
            ('Chemistry',),
            ('Biology',)
        ]
        cursor.executemany('INSERT INTO subject (name) VALUES (?)', subjects)

        # Add schedule (subject-lecturer relationships)
        schedule_data = [
            (1, 1),  # Mathematics - Dr. Robert Taylor
            (2, 2),  # Physics - Prof. Elizabeth White
            (3, 3),  # Computer Science - Dr. James Anderson
            (4, 4),  # Chemistry - Prof. Patricia Thomas
            (5, 1),  # Biology - Dr. Robert Taylor
            (1, 3),  # Mathematics - Dr. James Anderson (additional)
        ]
        cursor.executemany('INSERT INTO schedule (subject_id, lecturer_id) VALUES (?, ?)', schedule_data)

        conn.commit()
        print("Sample data inserted successfully")

    except Error as e:
        print(f"Error inserting data: {e}")


def execute_homework_queries(conn):
    """Execute SELECT queries from Homework 2"""
    try:
        cursor = conn.cursor()

        print("\n" + "=" * 70)
        print("QUERY 1: Students and Their Groups")
        print("=" * 70)

        # Your first query from Homework 2
        cursor.execute('''
            SELECT student.name AS student_name, "group".name AS group_name
            FROM student
            INNER JOIN "group" ON student.group_id = "group".id;
        ''')

        results = cursor.fetchall()
        print(f"{'Student Name':<20} | {'Group Name':<10}")
        print("-" * 35)
        for row in results:
            print(f"{row[0]:<20} | {row[1]:<10}")

        print(f"\nTotal students: {len(results)}")

        print("\n" + "=" * 70)
        print("QUERY 2: Subjects and Lecturers from Schedule")
        print("=" * 70)

        # Your second query from Homework 2
        cursor.execute('''
            SELECT subject.name AS subject_name, lecturer.name AS lecturer_name
            FROM schedule
            INNER JOIN subject ON subject.id = schedule.subject_id
            INNER JOIN lecturer ON lecturer.id = schedule.lecturer_id;
        ''')

        results = cursor.fetchall()
        print(f"{'Subject Name':<20} | {'Lecturer Name':<25}")
        print("-" * 50)
        for row in results:
            print(f"{row[0]:<20} | {row[1]:<25}")

        print(f"\nTotal schedule entries: {len(results)}")

    except Error as e:
        print(f"Error executing queries: {e}")


def update_records(conn):
    """Update records in the database"""
    try:
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("UPDATING RECORDS")
        print("=" * 60)

        # Update student's group
        cursor.execute('''
            UPDATE student 
            SET group_id = 3 
            WHERE name = 'John Smith'
        ''')
        print("✓ Updated group for John Smith (Group A → Group C)")

        # Update lecturer for a subject
        cursor.execute('''
            UPDATE schedule 
            SET lecturer_id = 4 
            WHERE subject_id = 1 AND lecturer_id = 3
        ''')
        print("✓ Updated lecturer for Mathematics (Dr. James Anderson → Prof. Patricia Thomas)")

        # Add new student
        cursor.execute('''
            INSERT INTO student (name, group_id) 
            VALUES ('David Moore', 2)
        ''')
        print("✓ Added new student: David Moore to Group B")

        conn.commit()
        print("\nRecords updated successfully!")

    except Error as e:
        print(f"Error updating records: {e}")


def verify_changes(conn):
    """Verify the changes made by UPDATE operations"""
    try:
        cursor = conn.cursor()

        print("\n" + "=" * 70)
        print("VERIFICATION OF CHANGES")
        print("=" * 70)

        # Verify group change
        cursor.execute('''
            SELECT s.name, g.name 
            FROM student s 
            JOIN "group" g ON s.group_id = g.id 
            WHERE s.name = "John Smith"
        ''')
        result = cursor.fetchone()
        print(f"✓ John Smith is now in group: {result[1]}")

        # Verify lecturer change
        cursor.execute('''
            SELECT sub.name, lect.name 
            FROM schedule s
            JOIN subject sub ON s.subject_id = sub.id
            JOIN lecturer lect ON s.lecturer_id = lect.id
            WHERE sub.name = "Mathematics" AND lect.name = "Prof. Patricia Thomas"
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ Mathematics is now taught by: {result[1]}")

        # Verify new student
        cursor.execute('''
            SELECT s.name, g.name 
            FROM student s 
            JOIN "group" g ON s.group_id = g.id 
            WHERE s.name = "David Moore"
        ''')
        result = cursor.fetchone()
        if result:
            print(f"✓ New student added: {result[0]} in {result[1]}")

        # Show updated student list
        print("\n" + "-" * 40)
        print("UPDATED STUDENT LIST:")
        print("-" * 40)
        cursor.execute('''
            SELECT s.name, g.name 
            FROM student s 
            JOIN "group" g ON s.group_id = g.id 
            ORDER BY g.name, s.name
        ''')
        students = cursor.fetchall()
        for student in students:
            print(f"{student[0]:<20} | {student[1]:<10}")

        print(f"Total students after update: {len(students)}")

    except Error as e:
        print(f"Error verifying changes: {e}")


def get_sqlite_version():
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute('SELECT sqlite_version()')
        version = cursor.fetchone()[0]
        conn.close()
        return version
    except:
        return "Unknown"


def main():
    """Main function to execute all steps"""
    database = "homework.db"

    print("STARTING HOMEWORK EXECUTION")
    print("=" * 50)
    print(f"SQLite version: {get_sqlite_version()}")

    # Step 1: Create database and tables
    conn = create_connection(database)
    if conn is not None:
        create_tables(conn)

        # Step 2: Insert sample data
        insert_sample_data(conn)

        # Step 3: Execute SELECT queries (before update)
        print("\nCHECKING DATA BEFORE UPDATE:")
        execute_homework_queries(conn)

        # Step 4: Update records
        update_records(conn)

        # Step 5: Execute SELECT queries (after update)
        print("\n📈 CHECKING DATA AFTER UPDATE:")
        execute_homework_queries(conn)

        # Step 6: Verify changes
        verify_changes(conn)

        conn.close()
        print("\nHomework completed successfully!")
        print(f"Database saved as: {database}")
    else:
        print("Error! Cannot create database connection.")


if __name__ == '__main__':
    main()