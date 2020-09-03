from flaskr import models

#土日の間で週1回で株価のデータを更新
if __name__ == '__main__':
    count = models.FetchData.read_count()
    flag = "y"
    #全企業を更新するか判定
    if count == 0 :
        flag = input("If you want to update stock_data ? [y/n] :")
    if flag == "y":
        models.FetchData.write_count(count)
        models.FetchData.fetched_data_to_mongo()
    else:
        print("操作を終了します。")

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

