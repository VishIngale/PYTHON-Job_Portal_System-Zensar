import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import mysql.connector
from datetime import date, datetime
from decimal import Decimal
import smtplib
from email.mime.text import MIMEText

with open("config.json", "r") as config_file:
    DB_CONFIG = json.load(config_file)

SMTP_CONFIG = {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "your-email@gmail.com",
    "password": "your-email-password"
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def send_email(to_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SMTP_CONFIG["user"]
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
        server.starttls()
        server.login(SMTP_CONFIG["user"], SMTP_CONFIG["password"])
        server.sendmail(SMTP_CONFIG["user"], to_email, msg.as_string())

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        conn, cursor = None, None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            if self.path == "/jobs":
                cursor.execute("SELECT * FROM Jobs")
            elif self.path == "/candidates":
                cursor.execute("SELECT * FROM Candidates")
            elif self.path == "/applications":
                cursor.execute("SELECT * FROM Applications")
            elif self.path.startswith("/match/job/"):
                job_id = self.path.split("/")[-1]
                cursor.execute("""
                    SELECT Candidates.CandidateID, Candidates.FirstName, Candidates.LastName
                    FROM Candidates
                    WHERE Skills LIKE (
                        SELECT CONCAT('%', RequiredSkills, '%') FROM Jobs WHERE JobID = %s
                    )
                """, (job_id,))
            else:
                self.send_error(404, "Endpoint not found")
                return

            result = cursor.fetchall()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result, cls=CustomJSONEncoder).encode())
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def do_POST(self):
        conn, cursor = None, None
        try:
            length = int(self.headers["Content-Length"])
            data = json.loads(self.rfile.read(length))
            conn = get_db_connection()
            cursor = conn.cursor()

            if self.path == "/jobs":
                sql = """INSERT INTO Jobs (JobTitle, CompanyName, Location, Salary, RequiredSkills, JobDescription)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (data["JobTitle"], data["CompanyName"], data["Location"],
                                     data["Salary"], data["RequiredSkills"], data["JobDescription"]))
            elif self.path == "/candidates":
                sql = """INSERT INTO Candidates (FirstName, LastName, Email, PhoneNumber, Skills)
                         VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (data["FirstName"], data["LastName"], data["Email"],
                                     data["PhoneNumber"], data["Skills"]))
            elif self.path == "/applications/update":
                sql = """UPDATE Applications SET Status = %s WHERE ApplicationID = %s"""
                cursor.execute(sql, (data["Status"], data["ApplicationID"]))
                cursor.execute("""
                    SELECT Candidates.Email FROM Candidates
                    JOIN Applications ON Candidates.CandidateID = Applications.CandidateID
                    WHERE Applications.ApplicationID = %s
                """, (data["ApplicationID"],))
                candidate = cursor.fetchone()
                if candidate:
                    send_email(candidate["Email"], "Application Update", f"Your application status is now {data['Status']}")
            else:
                self.send_error(404, "Endpoint not found")
                return

            conn.commit()
            self.send_response(201)
            self.end_headers()
            self.wfile.write(b"Record added successfully")
        except Exception as e:
            self.send_error(500, str(e))
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
