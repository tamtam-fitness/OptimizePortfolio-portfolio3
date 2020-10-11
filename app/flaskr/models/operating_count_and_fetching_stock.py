import datetime
import pandas as pd
import pandas_datareader.data as pdd

from . import stock_df

class ReadingAndWritingCount:
    #土日（証券市場）が閉まっている時に、一週間毎にDの株価を更新するクラス
    def read_count(self) -> int:
        """ヤフーファイナンスから、どの株価から取得するか特定するために読み込む関数"""    
        with open("./flaskr/data/count.txt", mode="r") as f:
            count = int(f.read())
        return count
    
    def write_count(self, count: int) -> None:
        """株価の取得エラーが起こった時に途中から始められるようセーブする関数"""
        #countが全てのデータを取得した場合リスタートさせる
        if 3629 <= count:
            count = 0 
        with open("./flaskr/data/count.txt", mode="w") as f:
            f.write(str(count))  



class FetchingStock:
    #土日（証券市場）が閉まっている時に、一週間毎にDの株価を更新するクラス
    def fetch_stock_from_yahoo(self, ticker: int, start_date: datetime, end_date: datetime) -> dict:
        financial_data = pd.DataFrame()
        financial_data[f'{ticker}.T'] = pdd.DataReader(f'{ticker}.T', data_source='yahoo', start = start_date, end = end_date)['Adj Close']
        financial_data = financial_data.reset_index()
        stack = {
            'ticker': financial_data[f'{ticker}.T'].name,
            'Date': list(financial_data["Date"].astype('datetime64[D]')),
            'stock_price': list(financial_data[f'{ticker}.T'].astype('float64'))
        }
        return stack

class OperatingCountAndFetchingStock:

    def __init__(self, reading_writing_count: ReadingAndWritingCount, fetching_stock: FetchingStock) -> None:
        self.__reading_writing_count = reading_writing_count
        self.__fetching_stock = fetching_stock
    
    def fetch_stock_and_operate_count(self) ->list:
        """東証に登録されている約3600社の直近3年間の株価を取得する関数"""
        #count.txtからセーブしたカウントを読み込む
        count = self.__reading_writing_count.read_count()
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
                stack = self.__fetching_stock.fetch_stock_from_yahoo(ticker, start_date, end_date)
                stacks.append(stack)
                count += 1
                print(count)

        except:
            print(f"{count}行で処理が終了しました。")
            print(f"{memory}から始まって{count}まで{count - memory}行読み込まれました。")
        finally:
            self.__reading_writing_count.write_count(count)
            return stacks

