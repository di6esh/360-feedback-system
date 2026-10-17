from flask import Flask, render_template, request, redirect, url_for, session, send_file
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from textwrap import wrap

app = Flask(__name__)

app.secret_key = "360-feedback-secret-key"

DATABASE = "database.db"


# =========================================================
# DATABASE
# =========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db_connection()

    # USERS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # MANAGER ASSIGNMENTS
    conn.execute("""
        CREATE TABLE IF NOT EXISTS manager_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            FOREIGN KEY (manager_id) REFERENCES users(id),
            FOREIGN KEY (employee_id) REFERENCES users(id)
        )
    """)

    # FEEDBACK
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            comment TEXT NOT NULL,
            feedback_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user_id) REFERENCES users(id),
            FOREIGN KEY (to_user_id) REFERENCES users(id)
        )
    """)

    # DEFAULT ADMIN
    admin = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, ("admin@gmail.com",)).fetchone()

    if admin is None:

        conn.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "HR Admin",
            "admin@gmail.com",
            "admin123",
            "admin"
        ))

    conn.commit()
    conn.close()


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    return redirect(url_for("login"))


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
            AND password = ?
        """, (email, password)).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))

            elif user["role"] == "manager":
                return redirect(url_for("manager_dashboard"))

            elif user["role"] == "employee":
                return redirect(url_for("employee_dashboard"))

        else:
            error = "Invalid email or password."

    return render_template("login.html", error=error)


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    return render_template(
        "admin_dashboard.html",
        name=session["name"]
    )


# =========================================================
# ADMIN - MANAGE USERS
# =========================================================

@app.route("/admin/users", methods=["GET", "POST"])
def manage_users():

    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    message = None

    conn = get_db_connection()

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        try:

            conn.execute("""
                INSERT INTO users
                (name, email, password, role)
                VALUES (?, ?, ?, ?)
            """, (name, email, password, role))

            conn.commit()

            message = "User added successfully."

        except sqlite3.IntegrityError:

            message = "Email already exists."

    users = conn.execute("""
        SELECT *
        FROM users
        ORDER BY id
    """).fetchall()

    conn.close()

    return render_template(
        "manage_users.html",
        users=users,
        message=message
    )


# =========================================================
# ADMIN - DELETE USER
# =========================================================

@app.route("/admin/delete-user/<int:user_id>")
def delete_user(user_id):

    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM users
        WHERE id = ?
        AND role != 'admin'
    """, (user_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("manage_users"))


# =========================================================
# ADMIN - ASSIGNMENTS
# =========================================================

@app.route("/admin/assignments", methods=["GET", "POST"])
def assignments():

    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    message = None

    conn = get_db_connection()

    if request.method == "POST":

        manager_id = request.form["manager_id"]
        employee_id = request.form["employee_id"]

        existing = conn.execute("""
            SELECT *
            FROM manager_assignments
            WHERE manager_id = ?
            AND employee_id = ?
        """, (manager_id, employee_id)).fetchone()

        if existing:

            message = "This employee is already assigned to this manager."

        else:

            conn.execute("""
                INSERT INTO manager_assignments
                (manager_id, employee_id)
                VALUES (?, ?)
            """, (manager_id, employee_id))

            conn.commit()

            message = "Employee assigned successfully."

    managers = conn.execute("""
        SELECT *
        FROM users
        WHERE role = 'manager'
        ORDER BY name
    """).fetchall()

    employees = conn.execute("""
        SELECT *
        FROM users
        WHERE role = 'employee'
        ORDER BY name
    """).fetchall()

    assignments = conn.execute("""
        SELECT
            manager_assignments.id,
            managers.name AS manager_name,
            employees.name AS employee_name

        FROM manager_assignments

        JOIN users AS managers
            ON manager_assignments.manager_id = managers.id

        JOIN users AS employees
            ON manager_assignments.employee_id = employees.id

        ORDER BY managers.name, employees.name
    """).fetchall()

    conn.close()

    return render_template(
        "assignments.html",
        managers=managers,
        employees=employees,
        assignments=assignments,
        message=message
    )


# =========================================================
# ADMIN - DELETE ASSIGNMENT
# =========================================================

@app.route("/admin/delete-assignment/<int:assignment_id>")
def delete_assignment(assignment_id):

    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM manager_assignments
        WHERE id = ?
    """, (assignment_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("assignments"))


# =========================================================
# MANAGER DASHBOARD
# =========================================================

@app.route("/manager")
def manager_dashboard():

    if "user_id" not in session or session["role"] != "manager":
        return redirect(url_for("login"))

    conn = get_db_connection()

    employees = conn.execute("""
        SELECT
            users.id,
            users.name,
            users.email

        FROM manager_assignments

        JOIN users
            ON manager_assignments.employee_id = users.id

        WHERE manager_assignments.manager_id = ?

        ORDER BY users.name
    """, (session["user_id"],)).fetchall()

    # Get feedback received by this manager
    feedback = conn.execute("""
        SELECT
            feedback.id,
            feedback.rating,
            feedback.comment,
            feedback.feedback_type,
            feedback.created_at

        FROM feedback

        WHERE feedback.to_user_id = ?

        ORDER BY feedback.created_at DESC
    """, (session["user_id"],)).fetchall()

    total_feedback = len(feedback)

    conn.close()

    return render_template(
        "manager_dashboard.html",
        name=session["name"],
        employees=employees,
        feedback=feedback,
        total_feedback=total_feedback
    )


# =========================================================
# MANAGER - GIVE FEEDBACK
# =========================================================

@app.route(
    "/manager/feedback/<int:employee_id>",
    methods=["GET", "POST"]
)
def manager_feedback(employee_id):

    if "user_id" not in session or session["role"] != "manager":
        return redirect(url_for("login"))

    conn = get_db_connection()

    employee = conn.execute("""
        SELECT
            users.id,
            users.name,
            users.email

        FROM manager_assignments

        JOIN users
            ON manager_assignments.employee_id = users.id

        WHERE manager_assignments.manager_id = ?
        AND manager_assignments.employee_id = ?
    """, (
        session["user_id"],
        employee_id
    )).fetchone()

    if employee is None:

        conn.close()

        return "You are not authorized to give feedback to this employee.", 403

    if request.method == "POST":

        rating = request.form["rating"]
        comment = request.form["comment"]

        existing = conn.execute("""
            SELECT *
            FROM feedback

            WHERE from_user_id = ?
            AND to_user_id = ?
            AND feedback_type = 'manager'
        """, (
            session["user_id"],
            employee_id
        )).fetchone()

        if existing:

            conn.close()

            return "You have already given feedback to this employee."

        conn.execute("""
            INSERT INTO feedback
            (
                from_user_id,
                to_user_id,
                rating,
                comment,
                feedback_type
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            employee_id,
            rating,
            comment,
            "manager"
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("manager_dashboard"))

    conn.close()

    return render_template(
        "manager_feedback.html",
        employee=employee
    )


# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================

@app.route("/employee")
def employee_dashboard():

    if "user_id" not in session or session["role"] != "employee":
        return redirect(url_for("login"))

    conn = get_db_connection()

    # Get all other employees
    # An employee can give feedback to other employees.

    employees = conn.execute("""
        SELECT
            id,
            name,
            email,
            role

        FROM users

        WHERE role IN ('employee', 'manager')
        AND id != ?

        ORDER BY name
    """, (
        session["user_id"],
    )).fetchall()

    conn.close()

    return render_template(
        "employee_dashboard.html",
        name=session["name"],
        employees=employees
    )


# =========================================================
# EMPLOYEE - GIVE PEER FEEDBACK
# =========================================================

@app.route(
    "/employee/feedback/<int:employee_id>",
    methods=["GET", "POST"]
)
def employee_feedback(employee_id):

    if "user_id" not in session or session["role"] != "employee":
        return redirect(url_for("login"))

    # Prevent employee from giving feedback to themselves

    if employee_id == session["user_id"]:

        return "You cannot give feedback to yourself.", 403

    conn = get_db_connection()

    employee = conn.execute("""
        SELECT
            id,
            name,
            email,
            role

        FROM users

        WHERE id = ?
        AND role IN ('employee', 'manager')
    """, (
        employee_id,
    )).fetchone()

    if employee is None:

        conn.close()

        return "Employee not found.", 404

    if request.method == "POST":

        rating = request.form["rating"]
        comment = request.form["comment"]

        # Check duplicate peer feedback

        existing = conn.execute("""
            SELECT *
            FROM feedback

            WHERE from_user_id = ?
            AND to_user_id = ?
            AND feedback_type = 'peer'
        """, (
            session["user_id"],
            employee_id
        )).fetchone()

        if existing:

            conn.close()

            return "You have already given feedback to this employee."

        conn.execute("""
            INSERT INTO feedback
            (
                from_user_id,
                to_user_id,
                rating,
                comment,
                feedback_type
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            employee_id,
            rating,
            comment,
            "peer"
        ))

        conn.commit()
        conn.close()

        return redirect(url_for("employee_dashboard"))

    conn.close()

    return render_template(
        "employee_feedback.html",
        employee=employee
    )


# =========================================================
# EMPLOYEE - MY FEEDBACK
# =========================================================

@app.route("/employee/my-feedback")
def my_feedback():

    if "user_id" not in session or session["role"] not in ("employee", "manager"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    feedback = conn.execute("""
        SELECT
            feedback.id,
            feedback.rating,
            feedback.comment,
            feedback.feedback_type,
            feedback.created_at

        FROM feedback

        WHERE feedback.to_user_id = ?

        ORDER BY feedback.created_at DESC
    """, (
        session["user_id"],
    )).fetchall()

    # Calculate overall average

    result = conn.execute("""
        SELECT
            AVG(rating) AS average_rating,
            COUNT(*) AS total_feedback
        FROM feedback
        WHERE to_user_id = ?
    """, (
        session["user_id"],
    )).fetchone()

    conn.close()

    average_rating = result["average_rating"]
    total_feedback = result["total_feedback"]

    return render_template(
        "my_feedback.html",
        feedback=feedback,
        average_rating=average_rating,
        total_feedback=total_feedback,
        name=session["name"]
    )


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@app.route("/employee/download-report")
def download_report():

    if "user_id" not in session or session["role"] not in ("employee", "manager"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    feedback = conn.execute("""
        SELECT
            feedback.rating,
            feedback.comment,
            feedback.feedback_type,
            feedback.created_at

        FROM feedback

        WHERE feedback.to_user_id = ?

        ORDER BY feedback.created_at DESC
    """, (
        session["user_id"],
    )).fetchall()

    result = conn.execute("""
        SELECT
            AVG(rating) AS average_rating,
            COUNT(*) AS total_feedback

        FROM feedback

        WHERE to_user_id = ?
    """, (
        session["user_id"],
    )).fetchone()

    conn.close()

    # Create PDF in memory

    pdf_file = BytesIO()

    pdf = canvas.Canvas(pdf_file)

    width, height = 595, 842

    y = height - 50

    # Title

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawString(
        50,
        y,
        "360 Degree Feedback Report"
    )

    y -= 35

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        y,
        "Name: " + session["name"]
    )

    y -= 25

    average = result["average_rating"]

    if average is None:
        average_text = "No ratings yet"
    else:
        average_text = f"{average:.2f} / 5"

    pdf.drawString(
        50,
        y,
        "Overall Rating: " + average_text
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        "Total Feedback: " + str(result["total_feedback"])
    )

    y -= 40

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(
        50,
        y,
        "Feedback Received"
    )

    y -= 30

    pdf.setFont("Helvetica", 10)

    if not feedback:

        pdf.drawString(
            50,
            y,
            "No feedback has been received yet."
        )

    else:

        for item in feedback:

            if y < 100:

                pdf.showPage()

                y = height - 50

                pdf.setFont("Helvetica", 10)

            pdf.setFont("Helvetica-Bold", 11)

            pdf.drawString(
                50,
                y,
                "From: Anonymous"
            )

            y -= 18

            pdf.setFont("Helvetica", 10)

            pdf.drawString(
                50,
                y,
                "Type: " + item["feedback_type"]
            )

            y -= 18

            pdf.drawString(
                50,
                y,
                "Rating: " + str(item["rating"]) + " / 5"
            )

            y -= 18

            pdf.drawString(
                50,
                y,
                "Date: " + str(item["created_at"])
            )

            y -= 18

            pdf.drawString(
                50,
                y,
                "Comment:"
            )

            y -= 15

            # Wrap long comments

            for line in wrap(item["comment"], 85):

                if y < 60:

                    pdf.showPage()

                    y = height - 50

                    pdf.setFont("Helvetica", 10)

                pdf.drawString(
                    60,
                    y,
                    line
                )

                y -= 14

            y -= 20

    pdf.save()

    pdf_file.seek(0)

    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="360_feedback_report.pdf",
        mimetype="application/pdf"
    )

@app.route("/admin/reports")
def admin_reports():
    if "user_id" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db_connection()

    employees = conn.execute("""
        SELECT
            users.id,
            users.name,
            users.email,
            COALESCE(AVG(feedback.rating), 0) AS average_rating,
            COUNT(feedback.id) AS total_feedback
        FROM users
        LEFT JOIN feedback
            ON users.id = feedback.to_user_id
        WHERE users.role = 'employee'
        GROUP BY users.id
        ORDER BY users.name
    """).fetchall()

    feedback = conn.execute("""
        SELECT
            feedback.id,
            feedback.rating,
            feedback.comment,
            feedback.feedback_type,
            feedback.created_at,
            receiver.name AS employee_name,
            sender.name AS from_name
        FROM feedback
        JOIN users AS receiver
            ON feedback.to_user_id = receiver.id
        JOIN users AS sender
            ON feedback.from_user_id = sender.id
        WHERE receiver.role = 'employee'
        ORDER BY feedback.created_at DESC
    """).fetchall()

    conn.close()

    return render_template(
        "admin_reports.html",
        employees=employees,
        feedback=feedback
    )
# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    init_db()

    app.run(host="0.0.0.0", port=5000, debug=True)