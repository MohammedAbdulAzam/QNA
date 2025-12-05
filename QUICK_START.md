# QNA Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Windows Users

1. **Setup (First Time Only):**
   ```batch
   setup.bat
   ```

2. **Run Application:**
   ```batch
   run.bat
   ```

3. **Open Browser:**
   ```
   http://localhost:5000
   ```

4. **Login as Admin:**
   - Username: `quizmaster`
   - Password: `123`

### Linux/Mac Users

1. **Make Scripts Executable:**
   ```bash
   chmod +x setup.sh run.sh
   ```

2. **Setup (First Time Only):**
   ```bash
   ./setup.sh
   ```

3. **Run Application:**
   ```bash
   ./run.sh
   ```

4. **Open Browser:**
   ```
   http://localhost:5000
   ```

5. **Login as Admin:**
   - Username: `quizmaster`
   - Password: `123`

## 📝 What the Scripts Do

### Setup Scripts (`setup.sh` / `setup.bat`)
- ✅ Check Python installation
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Initialize database with new schema
- ✅ Backup existing database (if any)

### Run Scripts (`run.sh` / `run.bat`)
- ✅ Activate virtual environment
- ✅ Check database exists
- ✅ Start Flask application
- ✅ Show access URL and credentials

## 🎯 First Steps After Setup

### 1. Add Teachers
- Navigate to **Teachers** menu
- Click **Add Teacher**
- Fill in: Name, Qualifications, Degree
- Submit

### 2. Create Subject with Teacher
- Go to **Dashboard**
- Click **Add New Subject**
- Enter subject name and description
- Select teacher from dropdown
- Submit

### 3. Create Sequential Quizzes
- Open the subject
- Click **Add Quiz**
- For Quiz 1:
  - Sequence Number: 1
  - Max Attempts: 2
  - Passing Score: 70
  - Prerequisite: None
- For Quiz 2:
  - Sequence Number: 2
  - Prerequisite: Quiz 1
- Repeat for Quiz 3

### 4. Add Questions
- Open a quiz
- Click **Add Question**
- Enter question text
- Add 4 options
- Select correct answer
- Submit

### 5. Test as Student
- Logout from admin
- Register new student account
- Browse subjects and see teacher info
- Attempt Quiz 1
- Pass with 70%+ to unlock Quiz 2

## 🔧 Troubleshooting

### "Python not found"
**Install Python 3.7+:**
- Windows: https://www.python.org/downloads/
- Linux: `sudo apt install python3`
- Mac: `brew install python3`

### "Virtual environment not found"
**Run setup again:**
```bash
# Windows
setup.bat

# Linux/Mac
./setup.sh
```

### "Port 5000 already in use"
**Edit run.py:**
```python
app.run(debug=True, port=5001)  # Change to 5001
```

### Database Issues
**Fresh start:**
```bash
# Delete database
rm qna.db  # Linux/Mac
del qna.db  # Windows

# Run migration
python migrate_database.py
```

## 📚 Documentation

- **Full README**: [README.md](README.md)
- **Migration Guide**: [MIGRATION_INSTRUCTIONS.md](MIGRATION_INSTRUCTIONS.md)
- **Implementation Plan**: [C:\Users\HP\.claude\plans\joyful-foraging-frog.md]

## 🎓 Key Features

✅ **Teacher Management** - Full CRUD with qualifications display
✅ **Sequential Quiz Unlocking** - Pass to unlock next
✅ **Attempt Limits** - 2 attempts per quiz (configurable)
✅ **Deadlines** - Optional due dates
✅ **Student ID Display** - On all pages
✅ **Percentage Scoring** - Automatic calculation
✅ **Performance Tracking** - Charts and statistics

## 📞 Need Help?

Check the full [README.md](README.md) for:
- Detailed feature documentation
- API endpoints
- Database schema
- Security features
- Contributing guidelines

---

**Ready to Learn! 🎓**
