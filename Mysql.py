import pymysql

class MasterFlaskCode:
    def __init__(self):
        self.user = 'root'
        self.password = '1234'
        self.host = 'localhost'
        self.port = 3307  # Port should be an integer
        self.database = 'tn_blood_bank'

    def select_direct_query(self, qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute(qry)
        data = cursor.fetchall()
        conn.close()
        return data
    
    
    def select_query(self, query, params=None):
        """Execute a select query and return the result."""
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()


        try:
            with cursor  as cursor:
                cursor.execute(query, params)  # Execute query with parameters
                result = cursor.fetchall()  # Fetch all results
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    
    def find_id(self,table):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM "+table)
        data = cursor.fetchall()
        maxin = len(data)
        
        return maxin
    
    
    
    def find_max_id(self,table):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM "+table)
        data = cursor.fetchall()
        maxin = len(data)
        if maxin == 0:
            maxin = 1
        else:
            maxin += 1
        return maxin
    
    def Update_query(self,qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        result=cursor.execute(qry)
        conn.commit()
        conn.close()
        return result
    
    def Update_query(self, qry, values):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        try:
            cursor.execute(qry, values)
            conn.commit()  # Commit the transaction
            affected_rows = cursor.rowcount  # Get the number of rows affected
            cursor.close()  # Close the cursor
            return affected_rows  # Return the count of updated rows
        except Exception as e:
            print(f"Error executing update query: {e}")
            return -1  # 
    
    def fetch_one(self, query, values=None):
        conn = pymysql.connect(
            user=self.user, 
            password=self.password, 
            host=self.host, 
            port=self.port, 
            db=self.database, 
            charset='utf8mb4'
        )
        try:
            cursor = conn.cursor()
            cursor.execute(query, values)
            result = cursor.fetchone()  # Fetch only one row
            return result
        finally:
            cursor.close()
            conn.close()
    
    def insert_query(self, qry, values=None):
    # Establish a connection to the database
        conn = pymysql.connect(
        user=self.user, 
        password=self.password, 
        host=self.host, 
        port=self.port, 
        db=self.database, 
        charset='utf8mb4'
    )
        try:
            cursor = conn.cursor()
            if values:
            # Execute the query with the provided values (parameterized query)
                result = cursor.execute(qry, values)
            else:
            # Execute the query without values (if no values are passed)
                result = cursor.execute(qry)
        
        # Commit the transaction
            conn.commit()
        
            return result  # Return the result of the execution
        except Exception as e:
        # Rollback in case of an error
            conn.rollback()
            raise e
        finally:
        # Close the connection
            cursor.close()
            conn.close()

    
    

    def fetch_all(self, query, params=None):
        conn = pymysql.connect(
            user=self.user, 
            password=self.password, 
            host=self.host, 
            port=self.port, 
            db=self.database, 
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def delete_direct_query(self, qry):
        conn = pymysql.connect(user=self.user, password=self.password, host=self.host, port=self.port, db=self.database, charset='utf8mb4')
        cursor = conn.cursor()
        
        try:
            cursor.execute(qry)
            conn.commit()
            print("Deletion successful.")
        except Exception as e:
            conn.rollback()
            print(f"An error occurred: {e}")
        finally:
            conn.close()