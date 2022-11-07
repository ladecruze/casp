import pymongo

myclient = pymongo.MongoClient("mongodb://casp-mongodb-1/casp")

db = myclient["casp"]
products = db["products"]
products.delete_many({})
product_one = {"id": 1,"product_name":"Chocolates","price":"2","quantity":"5"}
product_two = {"id": 2,"product_name":"Biscuits","price":"5","quantity":"10"}
products.insert_many([product_one,product_two])