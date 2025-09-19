1. Preparation: Sets up Python 3.13. Installs dependencies from requirements.txt.

2. Test Suite Execution:
    - Runs Behave tests for motion sensors, heat sensors, gas sensors: 
			behave --tags=@firmware,~@manual -f html-pretty -o reports/validation_report.html. 
			behave --tags=@firmware,~@manual -f allure_behave.formatter:AllureFormatter -o allure-results
			behavex --parallel-processes=2 --parallel-scheme=feature  -t @gas_sensor,@heat_sensor -f html-pretty -o reports/validation_report.html
			behave --tags=@firmware -f allure_behave.formatter:AllureFormatter -o reports/allure_report.html. 
    - Each test generates its HTML report in reports/.

3. GitHub CI/CD: Setting up a workflow file, defining the jobs, and running your Behave tests. GitHub Actions to automate this process.
    - Step1: Create a Workflow File .github/workflows/ci.yml
    - Step2: Define the Workflow .github/workflows/ci.yml
   
		# push to main
		# Whenever you commit and push code to the main branch, the workflow runs automatically.
		# pull_request to main
		# Whenever someone opens a pull request targeting the main branch, the workflow runs to check the code before merging.

		on:
		  push:
			branches:
			  - main
		  pull_request:
			branches:
			  - main

		jobs:
		  hil-tests:
			runs-on: windows-latest  # or ubuntu-latest if your tests run on Linux
			strategy:
			  matrix:
				python-version: [3.13]

			steps:
			  # 1. Checkout repository
			  - name: Checkout code
				uses: actions/checkout@v3

			  # 2️. Setup Python
			  - name: Set up Python ${{ matrix.python-version }}
				uses: actions/setup-python@v5
				with:
				  python-version: ${{ matrix.python-version }}

			  # 3.Install dependencies
			  - name: Install dependencies
				run: |
				  python -m pip install --upgrade pip
				  pip install -r requirements.txt

			  # 4.Create reports folder
			  - name: Prepare reports folder
				run: mkdir -p reports

			  # 5. Run Motion Sensor Tests
			  - name: Run Motion Sensor HIL Tests
				run: |
				  behave features/motion_sensor.feature \
					--tags=@acceptance \
					-f behave_html_formatter:HTMLFormatter \
					-o reports/motion_sensor_report.html

			  # 6. Run Heat Sensor Tests
			  - name: Run Heat Sensor HIL Tests
				run: |
				  behave features/heat_sensor.feature \
					--tags=@acceptance \
					-f behave_html_formatter:HTMLFormatter \
					-o reports/heat_sensor_report.html

			  # 7. Run Gas Sensor Tests
			  - name: Run Gas Sensor HIL Tests
				run: |
				  behave features/gas_sensor.feature \
					--tags=@acceptance \
					-f behave_html_formatter:HTMLFormatter \
					-o reports/gas_sensor_report.html

			  # 8. Upload Reports as Artifacts
			  - name: Upload HIL Test Reports
				uses: actions/upload-artifact@v3
				with:
				  name: HIL-Test-Reports
				  path: reports/*.html

			  # 9. Optional: Fail workflow if any test fails
			  - name: Fail on test errors
				if: failure()
				run: echo "One or more HIL sensor tests failed."

	- Step3: Commit and Push .github/workflows/ci.yml main branch on GitHub.
	- Step4: Monitor CI process at GitHub: After pushing, go to the "Actions" tab in your GitHub repository. The workflow will automatically start, 
	         and you can monitor its progress and view the test results and artifacts.