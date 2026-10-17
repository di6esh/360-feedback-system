# 360° Feedback System

A lightweight web application for collecting, viewing, and reporting
employee feedback from managers and peers. Built with Python, Flask,
HTML, CSS, and SQLite.

## Overview

The 360° Feedback System brings feedback into one place. It supports
three roles---Admin, Manager, and Employee---with different permissions
for each role.

## Features

-   Role-based login with separate dashboards.
-   Admin can add/manage users and assign employees to managers.
-   Managers can rate assigned employees from 1--5 and add written
    comments.
-   Employees can give peer feedback to other employees and managers,
    but cannot rate themselves.
-   Users can view feedback they have received.
-   Calculates the average of received ratings.
-   Generates downloadable PDF feedback reports.

## Technology Stack

  Component               Technology
  ----------------------- ------------------
  Programming language    Python
  Backend                 Flask
  Frontend                HTML, CSS
  Template engine         Jinja2
  Database                SQLite
  Database connectivity   Python `sqlite3`
  PDF generation          ReportLab

## Project Structure

``` text
360-feedback-system/
├── app.py
├── database.db
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

Your local project may contain additional files. Keep the `templates`
and `static` folder names because Flask uses them to locate HTML and CSS
files.

## Getting Started

### 1. Install Python

Install Python 3 if it is not already installed.

### 2. Clone or download the repository

``` bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd 360-feedback-system
```

Or download the repository as a ZIP file and extract it.

### 3. Install dependencies

``` bash
python -m pip install Flask reportlab
```

### 4. Run the application

``` bash
python app.py
```

Open the URL shown in the terminal, usually:

``` text
http://127.0.0.1:5000
```

The application initializes the database and creates a default Admin
account if it does not already exist.

## User Roles

### Admin

-   Add and manage users.
-   Assign employees to managers.
-   View feedback reports.

### Manager

-   View assigned employees.
-   Submit ratings and written feedback for assigned employees.
-   View feedback received from colleagues.

### Employee

-   Give peer feedback to other employees and managers.
-   View received feedback and the overall rating.
-   Download a PDF feedback report.

## Rating Calculation

The overall rating is the arithmetic mean of the ratings received.

Example: if a person receives ratings of 4 and 5:

``` text
Overall rating = (4 + 5) / 2 = 4.5 out of 5
```

## Database Tables

  -----------------------------------------------------------------------
  Table                               Purpose
  ----------------------------------- -----------------------------------
  `users`                             Stores user names, email addresses,
                                      passwords, and roles.

  `manager_assignments`               Stores manager--employee
                                      assignments.

  `feedback`                          Stores sender, receiver, rating,
                                      comment, feedback type, and
                                      timestamp.
  -----------------------------------------------------------------------

## Access from a Phone on the Same Wi-Fi

For local testing, configure Flask to listen on your laptop's network
interface:

``` python
app.run(host="0.0.0.0", port=5000, debug=True)
```

Find your laptop's local IPv4 address and open
`http://YOUR-LAPTOP-IP:5000` on your phone while both devices are
connected to the same Wi-Fi network.

This is for local testing only. Do not expose Flask's development server
to the public internet.

## Security Notes

This is a learning/college project, not a production-ready HR system.

-   The current implementation uses simple password storage. Implement
    password hashing before using it with real users.
-   Use a strong secret key loaded from environment variables.
-   Turn off Flask debug mode outside local development.
-   Add CSRF protection, input validation, and stronger access controls
    before production use.
-   Do not publish a real `database.db` containing personal information
    or passwords to GitHub.

## Future Enhancements

-   Password hashing and improved security.
-   Anonymous feedback and email notifications.
-   Feedback categories such as communication, teamwork, and leadership.
-   Charts and advanced analytics.
-   Cloud deployment and support for a larger database.

## Learning Outcomes

This project demonstrates: - Building a web application with Flask. -
Creating HTML templates with Jinja2. - Connecting Python to SQLite. -
Implementing role-based access and validation checks. - Calculating
ratings from database records. - Generating PDF reports with ReportLab.

## License

No license has been specified yet. Add a license file if you want others
to reuse, modify, or distribute this project under defined terms.
