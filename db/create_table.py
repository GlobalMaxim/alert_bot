create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL ,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    username VARCHAR(32),
    tel_number VARCHAR(32),
    bio VARCHAR(70),
    count_exec_script INT 
)
"""
