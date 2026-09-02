# AI-Powered Job Application & Resume Tracker

A full-stack Flask application for tracking jobs and applications, managing resume versions, parsing resumes, generating AI-assisted resume insights, and calculating an explainable job-match score with skill-gap recommendations.

## Core Features

- Secure registration/login with password hashing
- Job CRUD, search and filtering
- Application tracking: Applied, Assessment, Interview, Offer, Rejected, Withdrawn
- Resume upload and PDF/DOCX text extraction
- AI resume analysis with a structured JSON result when an AI key is configured
- Local fallback analyzer so the project remains runnable without an API key
- Explainable hybrid job matching
- Skill-gap recommendations
- Deadline and interview reminders
- Dashboard statistics
- Automated tests

## Project Objective

The objective of this project is to provide a centralized platform for managing the job-search process.

Instead of keeping job information, resumes, application statuses, interview dates, and skill requirements in separate places, the application brings them together into a single platform.

The AI-assisted features help users understand:

- What skills are present in their resume
- How well their resume matches a particular job
- Which required or preferred skills are missing
- What skills they should improve
- Which applications require follow-up or interview preparation

## Application Workflow

```text
Register / Login
       ↓
Add Job
       ↓
Upload Resume
       ↓
Analyze Resume
       ↓
Match Resume with Job
       ↓
Identify Skill Gaps
       ↓
Create Application
       ↓
Track Application Status
       ↓
Schedule Interview
       ↓
Receive Reminder
       ↓
View Dashboard Statistics


---

## 🟦 BLOCK 5 — Job Matching System

This is one of the **most important sections** because it explains your actual matching logic.

```markdown
## Job Matching System

The project uses an explainable hybrid matching approach instead of generating an arbitrary percentage using an LLM.

The final job-match score is calculated using four components:

| Component | Weight |
|---|---:|
| Required Skills | 50% |
| Preferred Skills | 20% |
| Project/Experience Relevance | 15% |
| Keyword Relevance | 15% |
| **Total** | **100%** |

This approach makes the match score easier to understand and explain.

For example, the system can show:

- Skills matched
- Skills missing
- Required-skill score
- Preferred-skill score
- Project/experience relevance
- Keyword relevance
- Overall match score
- Explanation of the result

## Skill-Gap Analysis

After comparing a resume with a job description, the application identifies missing skills.

Each skill gap can be categorized according to its importance.

The system provides recommendations such as:

> Learn the fundamentals, build a small project, and then add truthful evidence to your resume.

The purpose is to help users understand what they need to improve rather than simply showing a percentage.

## AI Resume Analysis

When an AI API key is configured, the application can perform AI-assisted resume analysis.

The analysis can identify information such as:

- Skills
- Education
- Projects
- Experience
- Relevant keywords

The AI result is structured so that the application can use the extracted information for further processing.

### Local Fallback

The application also includes a deterministic local analyzer.

This means the core project can still run without an external AI API key.

The fallback analyzer uses the project's curated skill dictionary and local processing logic.

## Resume Processing

The application supports resume uploads and extracts text from supported document formats.

Supported formats include:

- PDF
- DOCX

Extracted resume content can then be used for:

- Resume analysis
- Job matching
- Skill-gap identification
- Keyword comparison

## Application Tracking

Users can create applications for jobs and track their progress using the following statuses:

- Applied
- Assessment
- Interview
- Offer
- Rejected
- Withdrawn

Applications can be updated as the candidate progresses through the recruitment process.

The dashboard provides an overview of application progress and statistics.

## Reminders

The application supports reminders for important job-search events, including:

- Job deadlines
- Interview dates

Upcoming reminders are displayed on the dashboard so that users can keep track of important dates.

## Dashboard

The dashboard provides a centralized overview of the user's job-search activity.

It displays information such as:

- Total jobs
- Total applications
- Interviews
- Offers
- Response rate
- Upcoming reminders
- Application status information

## Technologies Used

### Backend

- Python
- Flask
- SQLAlchemy
- Flask-Login

### Database

- SQLite
- PostgreSQL-compatible configuration through `DATABASE_URL`

### Frontend

- HTML
- CSS
- Bootstrap
- Jinja2

### AI and Resume Processing

- OpenAI Responses API
- PyMuPDF / PyPDF2
- python-docx
- Structured JSON AI output

### Testing

- Pytest

## Project Structure

```text
AI-Job-Application-Resume-Tracker-Final-Code/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── models/
│
├── routes/
│   ├── auth.py
│   ├── dashboard.py
│   ├── jobs.py
│   ├── applications.py
│   ├── resumes.py
│   └── ai.py
│
├── services/
│   ├── ai_analyzer.py
│   ├── job_matcher.py
│   ├── reminder_service.py
│   └── resume_parser.py
│
├── static/
│
├── templates/
│
├── uploads/
│
└── tests/
    ├── test_auth.py
    ├── test_jobs.py
    └── test_matcher.py


---

## 🟦 Run Locally

```markdown
## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/shaistha-r/AI-Job-Application-Resume-Tracker.git
cd AI-Job-Application-Resume-Tracker

2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment

Windows PowerShell:

.\venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Configure environment variables

Copy .env.example to .env.

Example:
SECRET_KEY=your-secret-key
AI_API_KEY=your-ai-api-key
AI_MODEL=gpt-5
DATABASE_URL=sqlite:///database.db

Keep .env private.

Never commit real API keys, passwords, or other secrets to GitHub.

6. Run the application
python app.py

Open the application in your browser:

http://127.0.0.1:5000


---

## 🟦AI Configuration

```markdown
## AI Configuration

The AI functionality is optional.

To enable live AI-assisted analysis:

1. Create an AI API key.
2. Add the key to your local `.env` file.
3. Configure the desired AI model.
4. Run the application.

Example:

```env
AI_API_KEY=your-ai-api-key
AI_MODEL=gpt-5

If no AI API key is configured, the application uses its local fallback analyzer.

Do not upload .env or your API key to GitHub.


---

## 🟦Testing

```markdown
## Testing

The project includes automated tests using Pytest.

Run:

```bash
pytest -q


---

## 🟦 Security

```markdown
## Security Notes

The project follows several basic security practices:

- Passwords are securely hashed
- Uploaded files are validated
- Uploaded files are stored outside the `static` directory
- API keys and secrets are stored in environment variables
- User-specific routes query records through the authenticated user's ID
- `.env` is excluded from version control
- Database files are excluded from version control
- Virtual environments are excluded from version control
- Uploaded files are excluded from version control

## Limitations

This project is a one-day MVP and therefore has some limitations.

The current version uses:

- A curated skill dictionary
- Simple deadline and interview reminder logic
- Basic form validation
- Local SQLite database by default
- Basic automated test coverage

For production deployment, the following improvements would be recommended:

- Stronger CSRF protection and form validation
- Rate limiting
- Background job processing
- PostgreSQL database
- Cloud/object storage for uploaded resumes
- More comprehensive automated tests
- Production-grade authentication configuration
- Production deployment configuration
- More advanced AI recommendations

## Future Enhancements

Possible future improvements include:

- AI-powered resume improvement suggestions
- AI-generated cover letters
- Personalized job recommendations
- Email notifications
- Calendar integration
- Job-board integrations
- Advanced application analytics
- Resume version comparison
- Interview preparation assistance
- Cloud deployment
- More advanced skill analysis

## Testing Summary

The application was tested through both manual testing and automated testing.

### Manual Testing

The following workflow was successfully tested:

```text
User Registration
       ↓
Login
       ↓
Add Job
       ↓
Upload Resume
       ↓
Resume Analysis
       ↓
Job Matching
       ↓
Skill-Gap Analysis
       ↓
Application Creation
       ↓
Application Status Update
       ↓
Interview Reminder
       ↓
Dashboard


---

## 🟦 BLOCK 21 — Author

```markdown
## Author

**Shaistha R**

Computer Science & Engineering  
Batch 2027

## Project Purpose

This project was developed as an academic and portfolio project to demonstrate practical skills in:

- Python development
- Flask web development
- Database management
- Authentication
- Web application routing
- Resume processing
- AI integration
- Algorithmic job matching
- Software testing
- Git and GitHub

## License

This project is developed for educational and academic purposes.

