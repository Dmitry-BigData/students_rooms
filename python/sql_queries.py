query_for_altering_students_table_data_types = """ 
ALTER TABLE students
ADD COLUMN birthday_1 DATE,
ALTER COLUMN id SET DATA TYPE int,
ALTER COLUMN name SET DATA TYPE varchar,
ALTER COLUMN room SET DATA TYPE int,
ALTER COLUMN sex SET DATA TYPE varchar(1);

UPDATE students SET birthday_1 = to_date(birthday, 'YYYY-MM_DD"T"HH24:MI:SSTH');

ALTER TABLE students DROP COLUMN birthday;

ALTER TABLE students RENAME COLUMN birthday_1 TO birthday;
"""

query_for_altering_rooms_table_data_types = """
ALTER TABLE rooms
ALTER COLUMN id SET DATA TYPE int,
ALTER COLUMN name SET DATA TYPE varchar;
"""

query_for_adding_constraints_to_students_table = """
ALTER TABLE students
ADD CONSTRAINT pk_students_id PRIMARY KEY (id),
ADD CONSTRAINT fk_students_rooms FOREIGN KEY (room) REFERENCES rooms (id);
"""

query_for_adding_constraints_to_rooms_table = """
ALTER TABLE rooms
ADD CONSTRAINT pk_rooms_id PRIMARY KEY (id);
"""

get_number_of_students_in_room = """
SELECT room, COUNT(name) AS number_of_students
FROM students
GROUP BY room
ORDER BY room ASC
"""

get_rooms_with_minimal_avg_age = """
SELECT room, ROUND(AVG(EXTRACT(YEAR FROM AGE(NOW(), birthday))), 1) as avg_age
FROM students
GROUP BY room
ORDER BY avg_age ASC
LIMIT 5;
"""

get_rooms_with_maximum_age_difference = """
SELECT room, MAX(EXTRACT(YEAR FROM AGE(NOW(), birthday))) - MIN(EXTRACT(YEAR FROM AGE(NOW(), birthday))) as age_diff
FROM students
GROUP BY room
ORDER BY age_diff DESC
LIMIT 5;
"""

get_rooms_with_students_of_different_sex = """
SELECT room, COUNT(DISTINCT sex)
FROM students
GROUP BY room
"""