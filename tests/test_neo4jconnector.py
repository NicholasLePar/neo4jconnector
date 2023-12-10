import unittest
import pandas as pd

#Under test
from src.neo4jconnector import Neo4jConnector

class TestSuite001(unittest.TestCase):
    def test_connect_and_execute_query(self):
        db = Neo4jConnector("bolt://localhost:7687", "neo4j", "password")
        result = db.execute_query('MATCH(n) RETURN Count(n)')
        db.close()
        self.assertTrue(type(result)==pd.DataFrame)

