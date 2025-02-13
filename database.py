import psycopg2
from psycopg2.extensions import connection
from config import DB_CONFIG
from typing import Optional, List, Tuple
from datetime import date


def connect_db() -> Optional[connection]:
    """
    Function to connect to the database.

    This function does not receive any parameters directly; it uses the global variable
    DB_CONFIG, which should be a dictionary containing the necessary connection parameters
    (e.g., host, user, password, database).

    Returns:
        A psycopg2 connection object if the connection is successfully established.
        None if an error occurs during the connection attempt.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def insert_record(
    company: str,
    job_title: str,
    application_date: date,
    had_interview: bool,
    is_there_feedback: bool,
    feedback_date: Optional[date],
    application_website: str,
    is_remote: bool,
    linkedin_access: bool
) -> None:
    """
    Function to insert records into the database.

    Args:
        company (str): Name of the company.
        job_title (str): Job title.
        application_date (date): Date of application.
        had_interview (bool): Whether the interview was conducted.
        is_there_feedback (bool): Whether feedback is available.
        feedback_date (Optional[date]): Date of feedback, if available.
        application_website (str): URL of the application website.
        is_remote (bool): Whether the job is remote.
        linkedin_access (bool): Whether LinkedIn access is granted.

    Returns:
        None
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO applications (
                company, job_title, application_date, is_there_feedback, feedback_date, application_website, is_remote, linkedin_access, had_interview
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (company, job_title, application_date, is_there_feedback,
                       feedback_date if feedback_date else None, application_website, is_remote, linkedin_access, had_interview))
        conn.commit()
        cursor.close()
        conn.close()

def update_record(
    company: str,
    job_title: str,
    had_interview: bool,
    is_there_feedback: bool,
    feedback_date: Optional[date],
    application_website: str,
    is_remote: bool,
    linkedin_access: bool
) -> None:
    """
    Function to update records in the database.

    Args:
        company (str): Name of the company.
        job_title (str): Job title.
        had_interview (bool): Whether the interview was conducted.
        is_there_feedback (bool): Whether feedback is available.
        feedback_date (Optional[date]): Date of feedback, if available.
        application_website (str): URL of the application website.
        is_remote (bool): Whether the job is remote.
        linkedin_access (bool): Whether LinkedIn access is granted.

    Returns:
        None
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = """
            UPDATE applications
            SET had_interview = %s, is_there_feedback = %s, feedback_date = %s, application_website = %s, is_remote = %s, linkedin_access = %s
            WHERE company = %s AND job_title = %s
        """
        cursor.execute(query, (had_interview, is_there_feedback, feedback_date if feedback_date else None,
                       application_website, is_remote, linkedin_access, company, job_title))
        conn.commit()
        cursor.close()
        conn.close()

def get_all_records() -> List[Tuple]:
    """
    Function to retrieve all records from the database.

    Returns:
        List[Tuple]: A list of tuples, each containing a record from the database.
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = "SELECT * FROM applications"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

def search_record(company: str) -> Optional[List[Tuple]]:
    """
    Function to search for records in the database based on the company name.

    Args:
        company (str): Name of the company to search for in the database.

    Returns:
        Optional[List[Tuple]]: A list of tuples containing the matching records, 
        or None if no matching records are found.
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT * FROM applications
            WHERE company = %s
        """
        cursor.execute(query, (company,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

def delete_record(job_title: str) -> None:
    """
    Function to delete records from the database based on the job title.

    Args:
        job_title (str): The job title of the record to be deleted.

    Returns:
        None: This function performs a deletion operation and does not return any value.
    """
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = "DELETE FROM applications WHERE job_title = %s"
            cursor.execute(query, (job_title,))
            conn.commit()
            print(f"Record with job title '{job_title}' deleted successfully.")
        except Exception as e:
            print(f"Error when excluding from Database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
