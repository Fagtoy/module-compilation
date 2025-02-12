#  MODULE COMPILATION TESTS

---

## HOW TO RUN
- Attach to the ```yc-module-compilation``` container
- Set all the needed environment variables using: ```export PYTHONPATH="$PWD":$PYTHONPATH && export VIRTUAL_ENV="$PWD" && export TESTS_RESOURCES_DIR="$PWD"/tests/resources && export YANGCATALOG_CONFIG_PATH="$TESTS_RESOURCES_DIR"/test.conf && sed -i "s|<TESTS_RESOURCES_DIR>|${TESTS_RESOURCES_DIR}|g" "$YANGCATALOG_CONFIG_PATH"```
- Now you're able to run all the tests locally:
  - To run all the tests: ```pytest```
  - To run the tests in a particular file: ```pytest tests/test_file_name.py```
  - To run the particular test class or the method of the test class: ```pytest tests/test_file_name.py::TestClass::test_method```

---

## COVERAGE
For test coverage we are using [Coverage.py](https://coverage.readthedocs.io/en/6.5.0/).
To see all the information about the tests coverage locally follow these steps:
- Attach to the ```yc-module-compilation``` container
- Run ```pip install -r tests_requirements.txt```
- Set all the needed environment variables using the instructions above (this is not necessary if they are already set)
- Run the tests with coverage:
  - To run all the tests: ```coverage run -m pytest```
  - To run some particular test file: ```coverage run -m pytest tests/test_file_name.py```
- Generate an html report using command: ```coverage html```, this will create the ```htmlcov``` directory inside the ```yc-module-compilation``` container
- Unattach from the ```yc-module-compilation``` container and go to the ```deployment/module-compilation``` directory in your host machine
- Copy the ```htmlcov``` directory to your host machine using: ```docker cp yc-module-compilation:/module-compilation/htmlcov tests```, this command will copy the ```htmlcov``` directory from the ```yc-module-compilation``` container into the ```tests``` directory in your host machine
- Now you can open the file ```tests/htmlcov/index.html``` via your browser and explore all the information about the tests' coverage.