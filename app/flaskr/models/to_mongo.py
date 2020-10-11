import pandas as pd

from . import db

class ReadingCollectionLengthFromMongo:
    
    def read_collection_length(self, db_stacks) -> int:
        """コレクションが何個あるか調べる関数"""
        length = 0
        for _ in db_stacks.find():
            length += 1  
        return length

class FetchedStockToMongo:
    def __init__(self, reading_length: ReadingCollectionLengthFromMongo) -> None:
        self.__reading_length = reading_length

    def move_fetched_stock_to_mongo(self, stacks: list) -> None:
        """取得したデータをMongoDBへ入れる"""
        #DBを取得できたかどうか
        if len(stacks) == 0:
            print("データを取得していないためDB操作を終了しました。")
        else:
            db_stacks = db.stacks
            #コレクションが何個あるか調べる
            length = self.__reading_length.read_collection_length(db_stacks)
            #DBに東証企業の全てのデータがあるかどうか
            if 3629 <= length :
                #stackをMongoDBへ移動
                for stack in stacks:
                    #DBのUPDATE（更新）
                    db_stacks.find_one_and_update(
                        {'ticker':stack['ticker']}, 
                        {'$set':{
                                'stock_price':stack['stock_price'],
                                'Date':stack['Date']
                                }
                        }
                    )
            else:
                for stack in stacks:
                    #DBのINSERT（新規追加）
                    db_stacks.insert_one(stack)
            print("MongoDBへ移動しました。")


"""
<<<MongoDBの基本操作>>>

#MongoDBの立ち上げ
mongod --dbpath ./flaskr/data/db

#CREATE
MongoDBびローカル環境の指定
client = MongoClient('mongodb://localhost:27017/')
データベースの作成
db = client['stock_database']
db_stacks = db.stacks

#INSERT
db_stacks.insert_one(stack)

#READ
db_stacks.find_one({'ticker':"1301.T"}
for stack in db_stacks.find():
        print(stack)


#UPDATE
db_stacks.find_one_and_update(
    {'ticker':'1301.T'}, {'$set':{'stock_price':80}}
)

#DELETE
検索で該当するデータの全ての最初の一つを削除
db_stacks.delete_one({'ticker':'1301.T'})
検索で該当するデータの全てを削除
db_stacks.delete_many({'ticker':'1301.T'})
データの全てを削除
db_stacks.delete_many({})

"""