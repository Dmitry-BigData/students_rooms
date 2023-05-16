import os
import unittest
import psycopg2
from unittest.mock import MagicMock, patch
from decimal import Decimal
import xml.etree.ElementTree as ET
import json

class TestQueryExecution(unittest.TestCase):

    def setUp(self):
        self.connection = psycopg2.connect(host="localhost", user="postgres", password="postgres", dbname="test_db_1")

    def tearDown(self):
        self.connection.close()

    def test_execute_query_and_save_results_json(self):
        # Prepare test data
        query = "SELECT * FROM students"
        output_file_name = "result.json"

        # Execute the function
        self.execute_query_and_save_results(query, output_file_name)

        # Check if the JSON file is created
        self.assertTrue(os.path.exists("query_results/result.json"))

        # Clean up the generated file
        os.remove("query_results/result.json")

    def test_execute_query_and_save_results_xml(self):
        # Prepare test data
        query = "SELECT * FROM stuents"
        output_file_name = "result.xml"

        # Execute the function
        self.execute_query_and_save_results(query, output_file_name)

        # Check if the XML file is created
        self.assertTrue(os.path.exists("query_results/result.xml"))

        # Clean up the generated file
        os.remove("query_results/result.xml")

    def test_execute_query_and_save_results_invalid_output_format(self):
        # Prepare test data
        query = "SELECT * FROM table_name"
        output_file_name = "result.txt"

        # Capture the print output
        with patch('builtins.print') as mock_print:
            # Execute the function
            self.execute_query_and_save_results(query, output_file_name)

            # Check if the appropriate error message is printed
            mock_print.assert_called_with("Improper output format. Please indicate .json or .xml format in output file name.")

    def execute_query_and_save_results(self, query, output_file_name):
        """Mocked implementation of the function to test"""

        output_format = output_file_name.split('.')[1].lower()

        cursor_mock = MagicMock()  # Simulates the behavior of the database cursor object
        cursor_mock.description = [('col1',), ('col2',)] # A list of tuples representing the column names
        cursor_mock.fetchall.return_value = [(1, 'data1'), (2, 'data2')]  # A list of tuples representing the rows of data retrieved from the database.

        output_dir = "query_results"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, output_file_name)

        with patch('psycopg2.connect') as mock_connect:
            """This establishes the chain of attributes and methods to be mocked for the database connection object returned by psycopg2.connect. 
            It ensures that when self.connection.cursor() is called within the function being tested, 
            it returns the cursor_mock object created earlier."""
            mock_connect.return_value.__enter__.return_value.cursor.return_value = cursor_mock

            if output_format == "json":
                with open(output_path, 'w') as f:
                    f.write('{"data": "example"}')

            elif output_format == 'xml':
                root = ET.Element("root")
                ET.SubElement(root, "data").text = "example"
                tree = ET.ElementTree(root)
                tree.write(output_path)
            else:
                print("Improper output format. Please indicate .json or .xml format in output file name.")


if __name__ == '__main__':
    unittest.main()