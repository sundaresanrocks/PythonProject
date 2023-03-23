from pymongo import MongoClient
import unittest
import pytest
import logging
from ddt import ddt, unpack, data
from parameterized import parameterized

cars = [{'name': 'Audi', 'price': 52642},
        {'name': 'Mercedes', 'price': 57127},
        {'name': 'Skoda', 'price': 9000},
        {'name': 'Volvo', 'price': 29000},
        {'name': 'Bentley', 'price': 350000},
        {'name': 'Citroen', 'price': 21000},
        {'name': 'Hummer', 'price': 41400},
        {'name': 'Volkswagen', 'price': 21600}]

# @pytest.fixture(scope="class")
# def mongo_client_db():
#     client = MongoClient(host="172.18.0.2", port=27017, username="root", password = "rootpassword")
#     print(client.list_database_names())
#     db = client["testdb"]
#     yield db
#     print("Closing the session")
#     client.close()

# @pytest.fixture(scope="session")
# def client():
#     client = MongoClient(host="172.18.0.2", port=27017, username="root", password = "rootpassword")
#     print(client.list_database_names())
#     db = client["testdb"]
#     yield db
#     print("Closing the session")
#     client.close()

logger = logging.getLogger()

def test_function(a, b):
    return a + b

class MyTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def setup(self, client, client_1):
        self.db = client

    @pytest.mark.skip
    def test_mongo_read(self):
        results = self.db.cars.find()
        count = len([i for i in results])

        if count == 0:
            insert_obj = self.db.cars.insert_many(cars)
            output = {'Status': 'Successfully Inserted', 'Document_ID': insert_obj}
            print(output)

        aggr = [{"$match":{"$or":[{'name': "Audi" }, { 'name': "Mercedes" }]}}]

        aggr = [{"$match":{"$or":[{'name': "Audi" }, { 'name': "Volvo" }]}}]
        logger.info("#### {}".format(aggr))
        val = self.db.cars.aggregate(aggr)
        length = len([i for i in val])


        self.assertEqual(length, 14, "failed because of test issue")

    @pytest.mark.skip
    def test_mongo_agg(self):
        results = self.db.cars.find()
        count = len([i for i in results])

        if count == 0:
            insert_obj = self.db.cars.insert_many(cars)
            output = {'Status': 'Successfully Inserted', 'Document_ID': insert_obj}
            print(output)

        aggr = [{"$match":{"$or":[{'name': "Audi" }, { 'name': "Volvo" }]}}]

        val = self.db.cars.aggregate(aggr)
        length = len([i for i in val])
        logger.info("#### {}".format(aggr))

        self.assertEqual(length, 14, "failed because of test issue")
        # agr = [{"$group": {"_id":1, "all":{"$sum":"$price"}}}]
        #
        # val = list(db.cars.aggregate(agr))
        #
        # print('The sum of prices is {}'.format(val))

    @parameterized.expand([
        (1, 2, 3),
        (1, 2, 3)
    ],ids=[
        'int and dict',
        'bool and str',
    ])
    def test_max(self, input1, input2, expected):
        "Verify the max function works"
        value = test_function(input1, input2)
        self.assertEqual(value, expected)





