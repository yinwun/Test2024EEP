@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Check if the path parameter is provided
IF "%~1"=="" (
    echo Usage: %0 "C:\path\to\your\repository"
    exit /b
)

:: Get the current date in YYYY-MM-DD format
FOR /F "tokens=2 delims==" %%I IN ('wmic os get localdatetime /value') DO SET datetime=%%I
SET today=!datetime:~0,4!-!datetime:~4,2!-!datetime:~6,2!_!datetime:~8,2!-!datetime:~10,2!-!datetime:~12,2!-!datetime:~15,3!

:: Set the branch name using the current date
SET BRANCH_NAME=AI_Documentation_!today!

:: Navigate to your Git repository
cd "%~1" || (echo Repository not found at %~1 & exit /b)

:: Create the new branch
"C:\Program Files\Git\bin\git.exe" checkout -b !BRANCH_NAME!

echo New branch created: !BRANCH_NAME!

:: Stage all files
"C:\Program Files\Git\bin\git.exe" add .

SET COMMIT_MESSAGE=Initial commit
:: Commit the changes
"C:\Program Files\Git\bin\git.exe" commit -m "%COMMIT_MESSAGE%"

:: Push the changes to the remote repository
"C:\Program Files\Git\bin\git.exe" push -u origin %BRANCH_NAME%

echo.
echo All operations completed successfully.

ENDLOCAL
::pause
