import pandas as pd
from pymongo import MongoClient

from flask import Flask

#MongoDBびローカル環境の指定 悪用防止のためパスワードは差し替えています。
client = MongoClient("mongodb+srv://Densuke:i180442d@optimze-portfolio-clust.pydh1.mongodb.net/stock_database?retryWrites=true&w=majority")
#データベースの起動
db = client['stock_database']
#クエリ操作の際に使うファイル
stock_df = pd.read_csv("./flaskr/data/stock.csv")

def create_app():
    """Flaskのappを作成する関数"""
    from flaskr.views import bp
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(bp)
    return app
