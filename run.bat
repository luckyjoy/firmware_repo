@echo off
echo Sensor Firmware Automation by Bang Thien Nguyen, ontario1998@gmail.com ...
echo behave --tags=@all --exclude "features/manual_tests/.*" -f html-pretty -o reports\automation_report.html

if not exist reports mkdir reports 
del /q reports\*.html 2>nul
behave --tags=@all --exclude "features/manual_tests" -f html-pretty -o reports\automation_report.html

rem Set the source file name.
set "source_file=reports\automation_report.html"

rem Get the current date and time.
set "current_date=%date%"
set "current_time=%time%"

rem Fix the date format (MM-DD-YYYY or system locale dependent).
set "current_date=%current_date:~4%"
set "current_date=%current_date:/=-%"
set "current_date=%current_date: =%"

rem Fix the time format for filename.
set "current_time=%current_time::=-%"
set "current_time=%current_time: =%"
set "current_time=%current_time:.=-%"

rem Build new filename (without path).
set "new_filename=automation_report_%current_date%_%current_time%.html"

rem Full destination path.
set "destination_file=reports\%new_filename%"

rem Rename if source exists.
if exist "%source_file%" (
    pushd reports
    ren "automation_report.html" "%new_filename%"
    popd
    echo * Automation Report Generated At: "%destination_file%".
) else (
    echo "%source_file%" was not found.
)

python test_coverage.py reports\sensor_firmware_requirements.csv

python prd2html.py reports\product.json reports\sensor_firmware_requirements.csv

python automation_rate.py

for %%f in (reports\*.html) do (
    start "" "%%~f"
)


pause

