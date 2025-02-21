#!/usr/bin/python
import allure
import pytest
import input,os
import util.common as CM
from util.log import createLogger
from prettytable import PrettyTable
table = PrettyTable(["S.No","TestSuite","TestCase","Result"])
logger = createLogger()

###############PyTest Features#########################################
# Initialize counters
passed_tests = 0
failed_tests = 0
# Hook to capture the result of each test
def pytest_runtest_makereport(item, call):
    global passed_tests, failed_tests

    # Check when the test has finished running
    if call.when == 'call':  # 'call' indicates the actual test execution phase
        if call.excinfo is None:
            # Test passed (no exception raised)
            passed_tests += 1
            result = "PASSED"
        else:
            # Test failed (exception raised)
            failed_tests += 1
            result = "FAILED"
        table.add_row([passed_tests+failed_tests,item.nodeid.split("::")[0],item.nodeid.split("::")[1],result])
        # Print out the test name and result
        print(f"Test: {item.nodeid}, Result: {result}")
# Hook to print a summary after the tests have finished
def pytest_sessionfinish(session, exitstatus):
    print("\nTest Summary:")
    print(f"Total Passed: {passed_tests}")
    print(f"Total Failed: {failed_tests}")
    print(table)
def pytest_configure(config):
    version = os.getenv("m_chart_version", "NoVersionSpecified")  # Fetch the version from Jenkins parameter
    #config._metadata['Version'] = version  # Add version to the Allure report metadata
    # Use allure.dynamic to add custom metadata (e.g., version) to the Allure report
    allure.dynamic.label("version", version)  # Adds the version as a custom label to the report
    allure.dynamic.description(f"Test run version: {version}")
    # You can also add additional metadata, such as the environment or build number
    allure.dynamic.label("environment", os.getenv('ENVIRONMENT', 'dev'))
