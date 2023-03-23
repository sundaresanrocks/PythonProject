import pytest
from pymongo import MongoClient

@pytest.fixture(scope="class")
def client():
    client = MongoClient(host="172.18.0.2", port=27017, username="root", password = "rootpassword")
    print(client.list_database_names())
    db = client["testdb"]
    yield db
    print("Closing the session")
    client.close()


@pytest.fixture(scope="function")
def client_1():
    print("executing once per function")
    yield
    print("deleting after each function")