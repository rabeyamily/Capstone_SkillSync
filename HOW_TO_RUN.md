# How to Run SkillSync Locally

Follow these steps to run both the backend (FastAPI) and the frontend (Next.js) on your machine.

## 1. Prerequisites

- **Python 3.12** (required)
- **Node.js 20.x** and **npm 10.x** (required)
- **OpenAI API Key** (required for skill extraction)
- **Google OAuth Credentials** (optional, for Google login)
- **Gmail App Password** (optional for dev, required to send real verification emails)

## 2. Environment Variables

### Backend Environment Variables

1. Navigate to the `backend` directory
2. Create a `.env` file (copy from `.env.example` if it exists)
3. Add the following environment variables:

```env
# Required: OpenAI API Key for skill extraction
OPENAI_API_KEY=sk-...

# Optional: Google OAuth (for Google login)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...

# Optional: SMTP Settings (for email verification)
# If not set, verification codes will be logged to console
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=SkillSync

# Optional: Database (defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/skillsync

# Optional: JWT Secret (change in production!)
JWT_SECRET_KEY=your-secret-key-change-in-production
```

**Getting API Keys:**
- **OpenAI API Key**: Get from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Google OAuth**: Create OAuth 2.0 credentials in [Google Cloud Console](https://console.cloud.google.com/)
- **Gmail App Password**: Generate from Google Account → Security → 2-Step Verification → App passwords

> 💡 **Tip**: For quick testing without SMTP credentials, leave the SMTP values blank. The backend will log verification codes to the console instead of sending email.

### Frontend Environment Variables

1. Navigate to the `frontend` directory
2. Create a `.env.local` file (copy from `.env.local.example` if it exists)
3. Add the following environment variables:

```env
# Required: Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Google OAuth Client ID (for Google login)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=...
```

## 3. Install Dependencies

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note**: If you encounter issues with `pdfplumber` or other dependencies, you may need to install system dependencies:
- On macOS: `brew install poppler`
- On Ubuntu/Debian: `sudo apt-get install poppler-utils`
- On Windows: Install poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases)

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## 4. Initialize Database (First Time Only)

Before running the application for the first time, initialize the database:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment if not already active
python init_database.py
```

This creates the necessary database tables (users, user_profiles, user_cvs).

## 5. Run the Development Servers

You need to run both the backend and frontend servers simultaneously. Open **two separate terminal windows**:

### Terminal 1 – Backend Server

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
./dev.sh                  # Starts uvicorn on http://localhost:8000
```

**Alternative** (if `./dev.sh` doesn't work):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

### Terminal 2 – Frontend Server

```bash
cd frontend
npm run dev    # Serves Next.js on http://localhost:3000
```

You should see:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  ✓ Ready in X seconds
```

### Access the Application

1. Open your browser and navigate to: `http://localhost:3000`
2. The frontend will automatically connect to the backend API at `http://localhost:8000`
3. You can also access the API documentation at: `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc)

## 6. Production URLs

- **Backend API (Railway)**: `https://skillsync-production-d6f2.up.railway.app`
- **API Documentation**: `https://skillsync-production-d6f2.up.railway.app/docs`
- **Frontend**: Deploy to Vercel or other hosting platform

**To use production API locally:**
- Update `frontend/.env.local`: `NEXT_PUBLIC_API_URL=https://skillsync-production-d6f2.up.railway.app`
- Restart the frontend server: `npm run dev`

## 7. Common Tasks

### Database Operations

```bash
cd backend
source venv/bin/activate

# Initialize database (first time)
python init_database.py

# Run migrations
python migrate_add_email_verification.py

# Check a user in database
python check_user.py
```

### Testing

```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Run specific test file
pytest tests/test_skill_matching.py

# Frontend build (check for errors)
cd frontend
npm run build
```

### Development Commands

```bash
# Backend: Run with auto-reload
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend: Run development server
cd frontend
npm run dev

# Frontend: Lint code
cd frontend
npm run lint
```

## 8. Troubleshooting

### Common Issues

**1. Port Already in Use**
```
Error: Port 8000 is already in use
```
**Solution**: 
- Kill the process using the port: `lsof -ti:8000 | xargs kill -9` (macOS/Linux)
- Or change the port in `backend/dev.sh` or `uvicorn` command

**2. Google OAuth "Origin Not Allowed"**
```
Error: redirect_uri_mismatch
```
**Solution**: 
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Navigate to APIs & Services → Credentials
- Edit your OAuth 2.0 Client ID
- Add `http://localhost:3000` to "Authorized JavaScript origins"
- Add `http://localhost:3000` to "Authorized redirect URIs"

**3. Email Verification Not Working**
```
Verification emails not being sent
```
**Solution**:
- Check that SMTP environment variables are set correctly
- Verify Gmail app password is correct (not your regular password)
- Check backend logs for SMTP errors
- For development, leave SMTP blank - codes will be logged to console

**4. OpenAI API Errors**
```
Error: Invalid API key or rate limit exceeded
```
**Solution**:
- Verify `OPENAI_API_KEY` is set correctly in `backend/.env`
- Check your OpenAI account has sufficient credits
- Check API rate limits in OpenAI dashboard

**5. Database Connection Errors**
```
Error: Could not connect to database
```
**Solution**:
- For SQLite: Ensure `backend/data/` directory exists and is writable
- For PostgreSQL: Verify `DATABASE_URL` is correct and database exists
- Run `python init_database.py` to initialize tables

**6. Module Not Found Errors**
```
ModuleNotFoundError: No module named 'app'
```
**Solution**:
- Ensure you're in the `backend` directory
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

**7. Frontend Build Errors**
```
Error: Cannot find module
```
**Solution**:
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Clear Next.js cache: `rm -rf .next` (macOS/Linux) or `rmdir /s .next` (Windows)

### Getting Help

- Check backend logs for detailed error messages
- Check browser console (F12) for frontend errors
- Verify all environment variables are set correctly
- Ensure all dependencies are installed
- Check that both servers are running on correct ports

### Debug Mode

Backend debug endpoint (available in production):
- `http://localhost:8000/debug/config` - Check configuration status

This shows:
- OpenAI API key status
- Database connection status
- SMTP configuration status
- CORS settings


