import datetime
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pandas_datareader.data as pdd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import risk_models

from . import views
from flaskr import (
    db, 
    stock_df
)

class FetchData(object):
    #土日（証券市場）が閉まっている時に、一週間毎にDの株価を更新するクラス
    @classmethod
    def read_count(cls):
        """ヤフーファイナンスから、どの株価から取得するか特定するために読み込む関数"""    
        with open("./flaskr/data/count.txt", mode="r") as f:
            count = int(f.read())
        return count
    
    @classmethod
    def write_count(cls, count):
        """株価の取得エラーが起こった時に途中から始められるようセーブする関数"""
        #countが全てのデータを取得した場合リスタートさせる
        if 3629 <= count:
            count = 0 
        with open("./flaskr/data/count.txt", mode="w") as f:
            f.write(str(count))  
        
    @classmethod
    def fetch_stock_from_yahoo(cls):
        """東証に登録されている約3600社の直近3年間の株価を取得する関数"""
        #count.txtからセーブしたカウントを読み込む
        count = cls.read_count()
        memory = count
        print(f"{memory}行目よりデータを取得します。")
        try:
            #MongoDBに入れるデータ群
            stacks = []
            #直近3年間の株価を取得する、
            end_date = datetime.datetime.today()
            #今日の日付からtimedeltaで1年間ずらしたデータを生成
            start_date = end_date - datetime.timedelta(days= 365)
            #stock_dfから銘柄コードを呼び出し、ヤフーファイナンスUSからデータを取得
            for i in range(count, len(stock_df["銘柄コード"])):
                ticker = stock_df["銘柄コード"].values[i]
                #データを入れるためのデータフレームを作成
                financial_data = pd.DataFrame()
                financial_data[f'{ticker}.T'] = pdd.DataReader(f'{ticker}.T', data_source='yahoo', start = start_date, end = end_date)['Adj Close']
                financial_data = financial_data.reset_index()
                stack = {
                    'ticker': financial_data[f'{ticker}.T'].name,
                    'Date': list(financial_data["Date"].astype('datetime64[D]')),
                    'stock_price': list(financial_data[f'{ticker}.T'].astype('float64'))
                }
                stacks.append(stack)
                count += 1
                print(count)
        except:
            print(f"{count}行で処理が終了しました。")
            print(f"{memory}から始まって{count}まで{count - memory}行読み込まれました。")
        finally:
            cls.write_count(count)
            return stacks
    
    @classmethod
    def read_colections_length(cls, db_stacks): 
        """コレクションが何個あるか調べる関数"""
        length = 0
        for _ in db_stacks.find():
            length += 1  
        return length

    @classmethod
    def fetched_data_to_mongo(cls):
        """取得したデータをMongoDBへ入れる"""
        stacks = cls.fetch_stock_from_yahoo()
        #DBを取得できたかどうか
        if len(stacks) == 0:
            print("データを取得していないためDB操作を終了しました。")
        else:
            db_stacks = db.stacks
            #コレクションが何個あるか調べる
            length = cls.read_colections_length(db_stacks)
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


class UserSearchStock(object):
    #土日（証券市場）が閉まっている時に、一週間毎にDの株価を更新するクラス

    @classmethod
    def search_stock(cls, type_in):
        """銘柄が存在するか判定する関数"""
        if type_in == "" :
            return "銘柄コードもしくは会社名を入力してください。"
        elif type_in.isdecimal() :
            #コードを記入したとき
            #入力値のコードが存在するか判定
            search_company = stock_df[stock_df["銘柄コード"] == int(type_in)]
            if len(search_company) == 0 :
                return "存在する銘柄コードを入力してください。"
            else:
                return search_company
        else:
            search_company = stock_df[stock_df['会社名'].str.contains(type_in) == True]
            if len(search_company) == 0:
                return "検索出来ませんでした、正確な会社名に対応しています。"
                
            elif 6 <= len(search_company):
                return "検索ヒット数が多すぎます、具体的に記入してください。"
            else :      
                return search_company   
        

class OptimizePortfolio(object):
    #複数銘柄のポートフォリオの投資比率を最適化するクラス
    
    def __init__(self, tickers):

        """MongoDBから株価を取得しデータフレームを作成"""
        db_stacks = db.stacks

        stacks = []
        for ticker in tickers:
            stack = db_stacks.find_one({'ticker':f"{ticker}.T"})
            stacks.append(stack)

        financial_dict = {}
        for i in range(len(stacks)):
            wrapper_dict = {stacks[i]["ticker"]:stacks[i]["stock_price"]}
            financial_dict.update(wrapper_dict)
            
        financial_data = pd.DataFrame(financial_dict,
                        index= stacks[0]["Date"])
        
        self.tickers = tickers
        self.financial_data = financial_data
        
    def plot_stockprice(self):
        """株価をプロットする関数"""
        name = ""
        for i in self.tickers:
            name = name + "_" + i
        fig = plt.figure()
        title = "Portfolio Close Price History"

        for i in self.financial_data.columns.values:
            plt.plot(self.financial_data[i], label = i)

        plt.title(title)
        plt.xticks(rotation=30)
        plt.ylabel('Yen', fontsize =18)
        plt.legend( self.financial_data.columns.values, loc= 'upper left')
        fig.savefig(f"./flaskr/static/img/result{name}.jpg")
    
    def optimize_portfolio(self):
        """ポートフォリオを最適化する関数"""
        #平均リターンを求める
        #returns.mean() * 252
        mu = expected_returns.mean_historical_return(self.financial_data)
        #リスク（分散）を求める
        #Get the sample covariance matrix
        S = risk_models.sample_cov(self.financial_data) 
        #効率的フロンティアの作成
        ef = EfficientFrontier(mu, S)
        weights = ef.min_volatility()
        cleaned_weights = ef.clean_weights() 
        weight_keys = ["未選択","未選択","未選択","未選択"]
        weight_values = ["ー","ー","ー","ー"]
        count = 0
        for k ,v in dict(cleaned_weights).items():
            weight_keys[count] = k
            weight_values[count] = v
            count += 1
        #最適ポートフォリオの投資比率の出力, リターン・リスク・シャープレシオの出力
        return weight_keys, weight_values, ef.portfolio_performance(verbose=False)    
