# 🧑‍💼 Job Portal Web Application (Flask)

A role-based Job Portal built with **Flask**, supporting **Job Seekers**, **Employers**, and **Admins**. Users can register, post jobs, search/filter openings, and apply directly through the platform.

---

## 🚀 Features

- 🧍‍♂️ **Job Seeker**: Search & apply to jobs, filter by title/location/company
- 🧑‍💼 **Employer**: Post and manage job listings
- 👨‍💼 **Admin**: View all users, jobs, and applications
- 🛡️ Role-based login system using Flask-Login
- 🗃️ SQLite database with SQLAlchemy ORM
- 💻 Fully responsive frontend with Bootstrap

---

## 🛠️ Tech Stack

- Backend: Flask (Python)
- Database: SQLite (via SQLAlchemy)
- Forms: Flask-WTF
- Frontend: HTML, CSS, Bootstrap
- Authentication: Flask-Login

---

## 📂 Folder Structure

job_portal/
├── static/
│   ├── uploads/                 # Folder for uploaded files (e.g., resumes, logos)
│   ├── script.js                # JavaScript for client-side interactivity
│   └── style.css                # Custom CSS styling
│
├── templates/                   # All HTML Jinja2 templates
│   ├── admin_dashboard.html     # Admin panel view
│   ├── admin.html               # Possibly login or detail page for admin
│   ├── api_jobs.html            # JSON/API view of jobs?
│   ├── base.html                # Base template extended by other pages
│   ├── dashboard.html           # Possibly general or role-based dashboard
│   ├── employer_dashboard.html  # Employer's main dashboard
│   ├── home.html                # Landing page for the site
│   ├── job_detail.html          # Detailed view of a single job
│   ├── jobs.html                # List of all jobs (if separate from seeker view)
│   ├── login.html               # Login page
│   ├── post_job.html            # Form to post a job (employer)
│   ├── register.html            # Registration form
│   ├── seeker_dashboard.html    # Jobseeker dashboard with filters
│   └── view_applications.html   # View job applications (for admin/employer)
│
├── app.py                       # Main Flask app with routes
├── forms.py                     # WTForms (LoginForm, RegisterForm etc.)
├── models.py                    # SQLAlchemy Models (User, Job, Application)
├── README.md                    # Setup instructions, project overview
├── requirements.txt             # Python dependencies
