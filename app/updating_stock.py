from flaskr import models_bundle

#土日の間で週1回で株価のデータを更新
if __name__ == '__main__':
    models_bundle.update_stock()

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

