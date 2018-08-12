
import mysql.connector

host = 'mysql-eg-publicsql.ebi.ac.uk:4157'

cnx = mysql.connector.connect(user='scott', password='password',
                              host=host,
                              database='employees')
cnx.close()