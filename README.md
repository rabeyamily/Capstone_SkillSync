# SkillSync: Bridging the Competency Gap

## A Data-Driven Skill Analysis of Emerging Computer Science Roles and SkillSync, an AI-Powered Tool for Resume–Job Matching and Upskilling Recommendations

---

## 📋 Overview

**SkillSync** is an AI-powered web application that analyzes skill alignment between resumes and job descriptions. It helps job seekers understand how their skills match job requirements and provides personalized upskilling recommendations to bridge competency gaps.

### Key Features

- 🤖 **AI-Powered Skill Extraction**: Uses OpenAI GPT-4 to extract technical skills, soft skills, education, and certifications from resumes and job descriptions
- 📊 **Skill Gap Analysis**: Compares resume skills with job requirements to identify matches, gaps, and extra skills
- 🎯 **Match Score Calculation**: Calculates a percentage score (0-100%) based on technical skills alignment
- 💡 **Personalized Recommendations**: Generates actionable suggestions with Coursera course links for missing skills
- 🔐 **User Authentication**: Google OAuth and email/password authentication with email verification
- 👤 **Profile Management**: Save multiple resumes/CVs and manage your profile
- 📄 **PDF Report Generation**: Downloadable reports with visual charts and breakdowns
- 📝 **Multiple Input Formats**: Accepts PDF, DOCX files, or plain text input

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **AI/ML**: OpenAI GPT-4o for skill extraction
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens, Google OAuth, bcrypt for password hashing
- **File Processing**: pdfplumber, python-docx for PDF/DOCX parsing
- **Report Generation**: WeasyPrint for PDF generation
- **Deployment**: Railway

### Frontend
- **Framework**: Next.js 16 (React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Authentication**: Google OAuth (@react-oauth/google)
- **HTTP Client**: Axios
- **Deployment**: Vercel

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12
- Node.js 20 / npm 10
- OpenAI API key
- Google OAuth credentials (optional, for Google login)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rabeyamily/Capstone_SkillSync.git
   cd Capstone_SkillSync
   ```

2. **Set up Backend**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up Frontend**
   ```bash
   cd frontend
   npm install
   ```

4. **Configure Environment Variables**
   
   Backend (`backend/.env`):
   ```env
   OPENAI_API_KEY=sk-...
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   SMTP_FROM_EMAIL=your-email@gmail.com
   SMTP_FROM_NAME=SkillSync
   ```
   
   Frontend (`frontend/.env.local`):
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_GOOGLE_CLIENT_ID=...
   ```

5. **Run the Application**
   
   Terminal 1 (Backend):
   ```bash
   cd backend
   source venv/bin/activate
   ./dev.sh  # Starts on http://localhost:8000
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev  # Starts on http://localhost:3000
   ```

6. **Access the Application**
   - Open `http://localhost:3000` in your browser

For detailed setup instructions, see [HOW_TO_RUN.md](./HOW_TO_RUN.md)

---

## 📚 Project Structure

```
Capstone_SkillSync/
├── backend/
│   ├── app/
│   │   ├── api/           # API route handlers
│   │   ├── models/        # Database models and schemas
│   │   ├── services/      # Business logic services
│   │   └── utils/         # Utility functions
│   ├── tests/             # Unit and integration tests
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── services/          # API client services
│   └── utils/             # Utility functions
└── README.md
```

---

## 🔗 Links

- **GitHub Repository**: [https://github.com/rabeyamily/Capstone_SkillSync](https://github.com/rabeyamily/Capstone_SkillSync)
- **Backend API (Production)**: [https://skillsync-production-d6f2.up.railway.app](https://skillsync-production-d6f2.up.railway.app)
- **API Documentation**: [https://skillsync-production-d6f2.up.railway.app/docs](https://skillsync-production-d6f2.up.railway.app/docs)

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Build
```bash
cd frontend
npm run build
```

---

## 📖 How It Works

1. **Upload or Paste**: Users upload a resume (PDF/DOCX) or paste text, and provide a job description
2. **Skill Extraction**: AI extracts technical skills, soft skills, education, and certifications from both documents
3. **Gap Analysis**: System compares skills and identifies matches, gaps, and extra skills
4. **Match Score**: Calculates a Match Score based on technical skills: `(Matched Technical Skills / Total JD Technical Skills) × 100`
5. **Recommendations**: Generates personalized recommendations with Coursera course links for missing skills
6. **Report**: Users can download a PDF report with all analysis results

---

## 🎯 Match Score Calculation

The Match Score is calculated using only **technical skills** (11 categories):
- Programming Languages
- Frameworks/Libraries
- Tools/Platforms
- Databases
- Cloud Services
- DevOps
- Software Architecture
- Machine Learning
- Blockchain
- Cybersecurity
- Data Science

**Excluded from Match Score** (shown separately):
- Soft Skills (Leadership, Communication, Collaboration, Problem Solving, Analytical Thinking)
- Methodologies (Agile, Scrum, CI/CD, Design Thinking)
- Domain Knowledge (Fintech, Healthcare IT, E-Commerce)
- Education and Certifications

---

## 🔒 Security Features

- JWT-based authentication with 30-day token expiration
- Password hashing using bcrypt
- Email verification for account activation
- CORS configuration for allowed origins only
- Input validation and sanitization
- File upload size and type restrictions (max 10MB, PDF/DOCX only)

---

## 📝 License

This project is part of a capstone research project.

---

## 👥 Contributing

This is a capstone project. For questions or issues, please open an issue on GitHub.

---

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI and Next.js communities
- All open-source libraries used in this project
