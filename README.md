# 360° Feedback System

A web-based employee feedback and performance reporting system built using Python, Flask, HTML, CSS, and SQLite.

## 📌 About the Project

The 360° Feedback System is designed to simplify employee feedback management by bringing manager feedback and peer feedback into one centralized platform.

The system supports three roles: **Admin, Manager, and Employee**. It allows users to submit ratings and comments, view received feedback, calculate overall ratings, and download feedback reports as PDF files.

## ✨ Features

- **Role-Based Login:** Separate dashboards for Admin, Manager, and Employee.
- **User Management:** Admin can add and manage users.
- **Manager Assignment:** Admin can assign employees to managers.
- **Manager Feedback:** Managers can rate assigned employees and provide written comments.
- **Peer Feedback:** Employees can provide feedback to other employees and managers.
- **Feedback History:** Users can view the feedback they receive.
- **Automatic Rating Calculation:** Calculates the average of received ratings.
- **PDF Report Generation:** Generates downloadable feedback reports.
- **Database Storage:** Stores user details, assignments, ratings, and comments.

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Frontend | HTML, CSS |
| Template Engine | Jinja2 |
| Database | SQLite |
| Database Connectivity | Python `sqlite3` |
| PDF Generation | ReportLab |

## 📂 Project Structure

```text
360-feedback-system/
├── app.py
├── README.md
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── admin_dashboard.html
│   ├── manage_users.html
│   ├── assignments.html
│   ├── admin_reports.html
│   ├── manager_dashboard.html
│   ├── manager_feedback.html
│   ├── employee_dashboard.html
│   ├── employee_feedback.html
│   └── my_feedback.html
└── static/
    └── style.css
```

*Note: The SQLite database is created or used by the application locally. The virtual environment and local database should not be uploaded to GitHub.*

## 🚀 Installation and Setup

### Prerequisites

- Python 3
- pip

### 1. Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd 360-feedback-system
```

Replace the placeholder URL with your repository's actual URL.

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

If you do not have a `requirements.txt` file, install the dependencies directly:

```bash
python -m pip install Flask reportlab
```

### 3. Run the Application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

The application initializes the SQLite database and creates a default Admin account if one does not already exist.

## 👥 User Roles

### Admin
- Add and manage users.
- Assign employees to managers.
- View feedback reports.

### Manager
- View assigned employees.
- Provide ratings and written feedback to assigned employees.
- View feedback received from colleagues.

### Employee
- Give feedback to other employees and managers.
- View received feedback and overall ratings.
- Download a feedback report as a PDF.

## 🧮 Rating Calculation

The system calculates the overall rating using the arithmetic mean of all ratings received.

**Example:**

If an employee receives ratings of 4 and 5:

```text
Overall Rating = (4 + 5) / 2
               = 4.5 / 5
```

## 🗄️ Database Design

The application uses three main SQLite tables.

| Table | Purpose |
|---|---|
| `users` | Stores user names, email addresses, passwords, and roles. |
| `manager_assignments` | Stores manager–employee assignment details. |
| `feedback` | Stores feedback sender, receiver, rating, comment, feedback type, and timestamp. |

## 📱 Access from a Phone on the Same Wi-Fi

For local testing, configure Flask to listen on your laptop's network interface:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

Find your laptop's local IPv4 address and open the following address on your phone:

```text
http://YOUR-LAPTOP-IP:5000
```

Both devices must be connected to the same Wi-Fi network.

**Security note:** This configuration is intended for local testing only. Do not expose Flask's development server to the public internet.

## 🔮 Future Enhancements

- Password hashing and improved security.
- Anonymous feedback and email notifications.
- Feedback categories for teamwork, communication, and leadership.
- Graphical analytics and advanced reports.
- Cloud deployment and support for larger databases.
- Improved access control and employee development recommendations.

## 🎯 Learning Outcomes

This project demonstrates:

- Web application development using Flask.
- Dynamic HTML rendering using Jinja2.
- Database operations using SQLite.
- Role-based access control and feedback validation.
- Average rating calculation.
- PDF report generation using ReportLab.

## 🔐 Security Considerations

This project is intended for learning and academic purposes.

- Implement password hashing before using real user accounts.
- Use a strong secret key stored in environment variables.
- Disable Flask debug mode outside local development.
- Add CSRF protection and stronger security controls before production use.
- Do not commit databases containing personal information or passwords.

## 📄 License

No license has been specified yet. Add a license file if you want others to reuse, modify, or distribute this project under defined terms.

---

**Developed as a college project to demonstrate a simple and centralized employee feedback management system.**
