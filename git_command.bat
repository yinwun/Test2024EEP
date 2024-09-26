@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Get the current date in YYYY-MM-DD format
FOR /F "tokens=2 delims==" %%I IN ('wmic os get localdatetime /value') DO SET datetime=%%I
SET today=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!

:: Set the branch name using the current date
SET BRANCH_NAME=branch_!today!

:: Navigate to your Git repository
cd C:\Users\Test\Documents\GitHub\Test2024EEP

:: Create the new branch
git checkout -b !BRANCH_NAME!

echo New branch created: !BRANCH_NAME!

:: Stage all files
git add .

SET COMMIT_MESSAGE=Initial commit
:: Commit the changes
git commit -m "%COMMIT_MESSAGE%"

:: Push the changes to the remote repository
git push -u origin %BRANCH_NAME%

echo.
echo All operations completed successfully.

ENDLOCAL
pause
