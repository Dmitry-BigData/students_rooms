from sqlalchemy import create_engine, VARCHAR, INT
from moduls import *
from sql_queries import *
from time import sleep
dotenv.load_dotenv()

# sleep(600)
# CREATING TABLES FOR STUDENTS AND ROOMS AND INSERTING DATA
db_sql_alchemy = create_engine(os.environ.get('SQL_ALCHEMY_CONN_PATH'))
conn = db_sql_alchemy.connect()
students_dataframe = convert_json_to_pandas_dataframe("sources/students.json")
rooms_dataframe = convert_json_to_pandas_dataframe("sources/rooms.json")
students_dataframe.to_sql("students", con=conn, if_exists="replace", index=False, dtype={'birthday': VARCHAR, 'id': INT, 'name': VARCHAR, 'room': INT, 'sex': VARCHAR})
rooms_dataframe.to_sql("rooms", con=conn, if_exists="replace", index=False, dtype={'id': INT, 'name': VARCHAR})
conn.close()

# CHANGING DATA TYPES OF TABLES' COLUMNS
db = DatabaseToConnect(os.environ.get('DB_CONN_PATH'))
db.execute_query_without_saving(connection=db.connection, query=query_for_altering_students_table_data_types)
db.execute_query_without_saving(connection=db.connection, query=query_for_altering_rooms_table_data_types)

# ADDING PRIMARY KEY AND FOREIGN KEY CONSTRAINTS TO TABLES
db.execute_query_without_saving(connection=db.connection, query=query_for_adding_constraints_to_rooms_table)
db.execute_query_without_saving(connection=db.connection, query=query_for_adding_constraints_to_students_table)
db.close_db_connection(connection=db.connection)

# FIND AND SAVE ROOMS AND NUMBER OF STUDENTS THERE
db = DatabaseToConnect(os.environ.get('DB_CONN_PATH'))
db.execute_query_and_save_results(connection=db.connection, output_file_name="query1.xml", query=get_number_of_students_in_room)

# FIND 5 ROOMS WITH THE MINIMAL AVERAGE AGE OF STUDENTS
db.execute_query_and_save_results(connection=db.connection, output_file_name="query2.xml", query=get_rooms_with_minimal_avg_age)

# FIND 5 ROOMS WITH THE MAXIMUM AGE DIFFERENCE OF STUDENTS
db.execute_query_and_save_results(connection=db.connection, output_file_name="query3.xml", query=get_rooms_with_maximum_age_difference)

# FIND ROOMS WITH STUDENTS OF DIFFERENT SEX
db.execute_query_and_save_results(connection=db.connection, output_file_name="query4.xml", query=get_rooms_with_students_of_different_sex)
db.close_db_connection(connection=db.connection)

sleep(600)