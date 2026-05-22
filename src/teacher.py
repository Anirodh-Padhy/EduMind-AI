from src.database import (
    conn,
    cursor
)

# ---------------------------------------------------
# CREATE COURSE
# ---------------------------------------------------

def create_course(

    teacher,

    course_name,

    course_description
):

    cursor.execute(

        """

        INSERT INTO courses (

            teacher,
            course_name,
            course_description

        )

        VALUES (?, ?, ?)

        """,

        (
            teacher,
            course_name,
            course_description
        )
    )

    conn.commit()

# ---------------------------------------------------
# GET ALL COURSES
# ---------------------------------------------------

def get_courses():

    cursor.execute(

        """

        SELECT teacher,
               course_name,
               course_description

        FROM courses

        """
    )

    return cursor.fetchall()

# ---------------------------------------------------
# GET STUDENT COUNT
# ---------------------------------------------------

def get_student_count():

    cursor.execute(

        """

        SELECT COUNT(*)

        FROM users

        WHERE role='student'

        """
    )

    return cursor.fetchone()[0]

# ---------------------------------------------------
# GET TEACHER COUNT
# ---------------------------------------------------

def get_teacher_count():

    cursor.execute(

        """

        SELECT COUNT(*)

        FROM users

        WHERE role='teacher'

        """
    )

    return cursor.fetchone()[0]