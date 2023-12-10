from neo4j import GraphDatabase
import argparse

class Neo4jConnector():
    def __init__(self,
                uri,
                user,
                password,
                printQuery=True,
                printResult=True):
        self.printQuery = printQuery
        self.printResult = printResult
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        if self.printQuery:
            print(query)

        result = None

        with self.driver.session().begin_transaction() as tx:
            if parameters is None:
                result = tx.run(query)
            else:
                result = tx.run(query,parameters)

            #Consume result as dataframe by default
            #TODO: Explore more options for consuming results
            result = result.to_df()

        if self.printResult:
            print(result)

        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(dest='uri',
                        type=str,
                        help='Neo4J Database URI')

    parser.add_argument(dest='user',
                        type=str,
                        help='Neo4J Database Username')

    parser.add_argument(dest='password',
                        type=str,
                        help='Neo4J Database Password')

    parser.add_argument(dest='query',
                        type=str,
                        help='Cypher query')

    parser.add_argument('--parameters',
                        required=False,
                        type=str,
                        help='Query parameters ex:{"name": "Alice", "age": 33}')

    parser.add_argument('--printQuery',
                        required=False,
                        type=str,
                        help='Display Query')

    parser.add_argument('--printResult',
                        required=False,
                        type=str,
                        help='Display Result')

    args = parser.parse_args()

    printQuery = False
    if args.printQuery is not None:
        printQuery = True

    printResult = False
    if args.printQuery is not None:
        printQuery = True

    db = Neo4jConnector(
                args.uri,
                args.user,
                args.password,
                printQuery,
                printResult)

    db.execute_query(
        args.query,
        args.parameters
    )

    db.close()
