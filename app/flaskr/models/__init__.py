import os

from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient

load_dotenv()

#MongoDBびローカル環境の指定 悪用防止のためパスワードは差し替えています。
client = MongoClient(f"mongodb+srv://Densuke:{os.environ['PASSWORD']}@optimze-portfolio-clust.pydh1.mongodb.net/stock_database?retryWrites=true&w=majority")
#データベースの起動
db = client['stock_database']
#クエリ操作の際に使うファイル
stock_df = pd.read_csv("./flaskr/data/stock.csv")
