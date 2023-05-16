import json
import pandas
import psycopg2
import pandas as pd
import xml.etree.ElementTree as ET
from decimal import Decimal
import os
import dotenv
dotenv.load_dotenv()


class DatabaseToConnect:
    def __init__(self, connection_path=os.environ.get('DB_CONN_PATH')):
        self.connection = psycopg2.connect(connection_path)
        self.connection.autocommit = True

    def execute_query_without_saving(self, connection: psycopg2.connect, query: str):
        """Execute query without saving its result in separate file"""
        with connection.cursor() as cursor:
            cursor.execute(query)

    def execute_query_and_save_results(self, connection: psycopg2.connect, output_file_name: str, query: str):
        """Execute query with saving its result in a file of JSON or XML format"""
        def decimal_default(obj):
            """Function to convert non JSON serializable Decimal to float"""
            if isinstance(obj, Decimal):
                return float(obj)
            raise TypeError

        output_format = output_file_name.split('.')[1].lower()  # Getting output file format

        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        try:
            assert output_format == "json" or output_format == "xml"

            # Create the output directory if it doesn't exist
            output_dir = "query_results"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(output_dir, output_file_name)

            if output_format == "json":
                # Converting data to the list of dictionaries
                data = []
                for row in rows:
                    data.append(dict(zip(columns, row)))

                # Convert data to JSON string
                json_data = json.dumps(data, indent=4, default=decimal_default)

                # Saving JSON file
                with open(output_path, 'w') as file:
                    file.write(json_data)

            elif output_format == "xml":
                # Create the root element of the XML tree
                root = ET.Element("data")

                # Add each row of data as a child element of the root element
                for row in rows:
                    row_element = ET.SubElement(root, "row")
                    for i in range(len(columns)):
                        column_element = ET.SubElement(row_element, columns[i])
                        column_element.text = str(row[i])

                # Create the XML tree
                tree = ET.ElementTree(root)

                # Write the XML tree to a file
                tree.write(output_path)
        except AssertionError:
            print("Improper output format. Please indicate .json or .xml format in output file name.")

        cursor.close()

    def close_db_connection(self, connection: psycopg2.connect):
        connection.close()


def convert_json_to_pandas_dataframe(path_to_json_file) -> pandas.DataFrame:
    df = pd.read_json(path_to_json_file)
    return df
