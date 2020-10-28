from abc import ABC, abstractmethod

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import expected_returns
from pypfopt import risk_models

from . import db  

class AnalyzingPortfolio(ABC):
    #複数銘柄のポートフォリオの投資比率を最適化するクラス
    
    def __init__(self, tickers: list) -> None:

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

    @abstractmethod
    def operate(self):
        pass

class PlottingStockPrice(AnalyzingPortfolio):

    def operate(self) -> None:
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
    

class OptimizingPortfolio(AnalyzingPortfolio):  
    def operate(self) -> tuple:
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
