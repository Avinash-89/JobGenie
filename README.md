# 🧞 JobGenie Workspace

### AI-Powered Talent Acquisition, Interview Intelligence & Analytics Platform

JobGenie Workspace is an enterprise-grade recruitment intelligence platform built with Python and Streamlit. It streamlines the hiring lifecycle through AI-powered resume analysis, ATS scoring, interview simulation, business intelligence dashboards, and automated reporting.

The platform enables recruiters, HR teams, hiring managers, and interviewers to evaluate candidates more efficiently using intelligent automation and analytics-driven decision-making.

---

## 🚀 Features

### 🔐 Authentication & Access Control

- Secure Login & Registration
- Password Hashing
- Role-Based Access Control (RBAC)
- Admin, Recruiter, and Interviewer Roles
- Session Management

---

### 📄 AI Resume Processing Engine

Upload candidate resumes and automatically:

- Extract text from PDF resumes
- Analyze resume against Job Description
- Calculate ATS Match Score
- Identify matching skills
- Detect missing skills
- Generate candidate suitability insights
- Store candidate records in the database

---

### 🎭 Live Interview Simulator

Interactive AI-powered interview experience:

- Dynamic interview question generation
- Job-specific interview configuration
- Real-time interview workflow
- Candidate response collection
- AI performance evaluation
- Technical interview scoring
- Personalized feedback generation

---

### 📊 Executive Analytics Dashboard

Monitor hiring performance through:

- Resume Processing Metrics
- Interview Analytics
- ATS Match Statistics
- Candidate Tracking
- Recruitment KPIs

---

### 📈 Business Intelligence Dashboard

Advanced recruitment analytics:

- Candidate Pipeline Analytics
- Hiring Performance Metrics
- ATS Score Distribution
- Recruitment Trends
- Interactive Data Visualization

---

### 📁 Automated Reporting System

Generate professional PDF reports including:

- Candidate Assessment Reports
- ATS Evaluation Reports
- Audit Reports
- Interview Performance Summaries

---

## 🏗️ System Architecture

```text
JobGenie Workspace

├── Authentication Layer
│   ├── Login
│   ├── Registration
│   └── Role Management
│
├── Resume Intelligence Engine
│   ├── PDF Parser
│   ├── ATS Analyzer
│   ├── Skill Matcher
│   └── Candidate Database
│
├── Interview Intelligence Engine
│   ├── Question Generator
│   ├── Conversation Simulator
│   ├── Performance Evaluator
│   └── Feedback Generator
│
├── Business Intelligence Layer
│   ├── Recruitment Analytics
│   ├── Dashboard Metrics
│   ├── KPI Tracking
│   └── Visualization Engine
│
└── Reporting Layer
    ├── PDF Reports
    ├── Candidate Reports
    └── Audit Documentation
```

---

## 📂 Project Structure

```text
jobgenie/

├── app.py
│
├── core/
│   ├── database.py
│   ├── auth.py
│   └── models.py
│
├── services/
│   ├── parser.py
│   ├── ats_engine.py
│   ├── interview.py
│   ├── bi_analytics.py
│   └── report_engine.py
│
├── utils/
│   └── reporter.py
│
├── database/
│   └── talent_suite.db
│
├── assets/
│
└── requirements.txt
```

---

## 🛠️ Technology Stack

### Frontend

- Streamlit

### Backend

- Python

### Database

- SQLite

### Data Processing

- Pandas
- NumPy

### NLP & AI

- Custom ATS Matching Engine
- Skill Extraction
- Interview Evaluation Logic

### Document Processing

- PyMuPDF
- PDF Parsing

### Reporting

- PDF Report Generation

### Analytics

- Plotly
- Recruitment BI Dashboards

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/jobgenie-workspace.git

cd jobgenie-workspace
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application starts at:

```text
http://localhost:8501
```

---

## 🔑 Default Admin Credentials

For first-time deployment:

```text
Username: admin
Password: admin123
```

> Change default credentials immediately after deployment.

---

## 📊 Core Modules

### Executive Analytics Matrix

Provides hiring and recruitment KPIs:

- Total Resumes Processed
- Interview Statistics
- ATS Match Scores
- Candidate Tracking Metrics

---

### BI Analytics Dashboard

Business Intelligence module for:

- Recruitment analytics
- Candidate performance trends
- ATS insights
- Organizational hiring metrics

---

### Resume Analyzer

Features:

- Resume Parsing
- ATS Evaluation
- Skill Matching
- Candidate Ranking

---

### Interview Simulator

Supports:

- Technical Interviews
- Behavioral Interviews
- Role-Based Questions
- AI Evaluation

---

### Reporting Terminal

Generate:

- Candidate Reports
- ATS Reports
- Recruitment Audit Reports
- PDF Documentation

---

## 🔒 Security Features

- Password Hashing
- Session Protection
- Role-Based Authorization
- Secure Database Access
- Input Validation
- Protected Administrative Functions

---

## 📈 Future Enhancements

### AI Enhancements

- Gemini API Integration
- OpenAI Integration
- LLM-Based Resume Analysis
- Intelligent Candidate Ranking

### Interview Enhancements

- Voice Interviews
- Speech-to-Text
- AI Avatar Interviewer
- Video-Based Assessment

### Recruitment Enhancements

- LinkedIn Profile Analysis
- Job Board Integration
- Automated Candidate Screening
- Recruitment Workflow Automation

### Enterprise Features

- PostgreSQL Support
- Docker Deployment
- Multi-Tenant Architecture
- Cloud Deployment
- REST API Layer

---

## 🎯 Use Cases

### Recruiters

- Resume Screening
- Candidate Evaluation
- Hiring Analytics

### HR Teams

- Recruitment Management
- ATS Optimization
- Hiring Insights

### Interviewers

- Technical Assessments
- Interview Evaluation
- Candidate Feedback

### Organizations

- Talent Acquisition
- Recruitment Intelligence
- Workforce Analytics

---

## 📸 Screenshots

Add screenshots here:

### Login Portal

```text
/screenshots/login.png
```

### Executive Dashboard

```text
/screenshots/dashboard.png
```

### Resume Analysis Engine

```text
/screenshots/resume-analysis.png
```

### Interview Simulator

```text
/ screenshots/interview-simulator.png
```

### Reporting Terminal

```text
/screenshots/reporting.png
```

---

## 👨‍💻 Author

### Avinash Kumar Gupta

BCA (Data Science & AI)

- Python Developer
- Data Analyst
- AI Enthusiast

GitHub: https://github.com/yourusername

LinkedIn: https://linkedin.com/in/yourprofile

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Project Highlights

✅ Enterprise Recruitment Platform

✅ AI Resume Analysis

✅ ATS Match Scoring

✅ Interactive Interview Simulator

✅ Recruitment Analytics Dashboard

✅ Automated PDF Reporting

✅ Role-Based Authentication

✅ Database-Driven Architecture

---

# 🧞 JobGenie Workspace

### Smarter Hiring Through Artificial Intelligence
