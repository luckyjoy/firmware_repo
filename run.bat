@echo off
echo Running Sensor Firmware Update Tests...
echo behave --tags=@firmware,~@manual -f html-pretty -o reports\validation_report.html

if not exist reports mkdir reports

behave --tags=@firmware,~@manual -f html-pretty -o reports\validation_report.html

rem behavex --t @smoke -t @regression --parallel-processes 2 --exclude @manual -f html-pretty -o reports\validation_report.html
rem behave --tags=@firmware -f behave_html_formatter:HTMLFormatter -o reports\report.html
rem behave -t @smoke -t @regression --exclude @manual -f html-pretty -o reports\validation_report.html

rem behavex --tags @motion_sensor,@gas_sensor,@heat_sensor --parallel-processes 3 --exclude @manual 

python scenarios_auto_pertcentage.py
echo  * Validation Report Generated At: reports\report.html

python test_coverage.py reports/sensor_firmware_requirements.csv