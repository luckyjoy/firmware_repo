@echo off

REM Navigate to your repository root
rem cd C:\my_work\firmware_repo

rem echo %RANDOM% > test.txt
REM Add dummy file
git add .

REM Commit with message
rem echo.
rem echo Git pushed a dummy file for CI Demo
echo.
git commit -m "Initial Commit..."

REM Ensure branch is main
git branch -M main

REM Push to origin main
git push -u origin main

#curl -u "luckyjoy:11ce1755fa745c0bf522d169a9cac2ca11" -k -X POST "https://localhost:8443/job/firmware_repo/build"
sleep 10

start "" "https://github.com/luckyjoy/firmware_repo/actions"

echo.

rem echo A new build has been triggred at secured Jenkins server: https://localhost:8443/view/all/builds
echo.

rem echo A new build has been trigger at GitHub server: "https://github.com/luckyjoy/fimware_repo/actions"

echo.