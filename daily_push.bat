@echo off
echo Starting daily push to GitHub...

:: Add all changes
git add .

:: Get current date and time
for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a:%%b)

:: Commit with timestamp
git commit -m "Daily update - %mydate% %mytime%"

:: Push to GitHub
git push origin main

echo Daily push completed!
pause