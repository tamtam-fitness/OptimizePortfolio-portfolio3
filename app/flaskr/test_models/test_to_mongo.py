from models.to_mongo import ReadingCollectionLengthFromMongo,  FetchedStockToMongo
from models.conf import 

def fetched_stock_to_mongo():
    reading_collection_length_from_mongo = ReadingCollectionLengthFromMongo()
    fetched_stock_to_mongo = FetchedStockToMongo(reading_collection_length_from_mongo)
    pass