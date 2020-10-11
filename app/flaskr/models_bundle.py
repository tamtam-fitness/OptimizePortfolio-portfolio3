
import glob
import os

from .models import ( 
    to_mongo,
    operating_count_and_fetching_stock,
    searching_stock,
    analyzing_stock
)


def update_stock() -> None:
    reading_writing_count = operating_count_and_fetching_stock.ReadingAndWritingCount()
    fetching_stock = operating_count_and_fetching_stock.FetchingStock()
    #土日の間で週1回で株価のデータを更新
    count = reading_writing_count.read_count()
    flag = "y"
    #全企業を更新するか判定
    if count == 0 :
        flag = input("If you want to update stock_data ? [y/n] :")
    if flag == "y":
        reading_writing_count.write_count(count)
        fetching_stock = operating_count_and_fetching_stock.OperatingCountAndFetchingStock(reading_writing_count, fetching_stock)
        stacks = fetching_stock.fetch_stock_and_operate_count()
        reading_length = to_mongo.ReadingCollectionLengthFromMongo()
        fetched_stock_to_mongo = to_mongo.FetchedStockToMongo(reading_length) 
        fetched_stock_to_mongo.move_fetched_stock_to_mongo(stacks)
    else:
        print("操作を終了します。")


def send_views_index() -> tuple:
    """index.htmlの生成する関数"""
    weight_keys = ["未選択","未選択","未選択","未選択"]
    weight_values = ["ー","ー","ー","ー"]
    return_risk_sharpratio =["ー","ー","ー"]
    return weight_keys, weight_values, return_risk_sharpratio


def send_views_result_search_stock(type_in: str) -> dict:

    """選択した銘柄が存在するか判定し、あれば出力する関数""" 
    search_company = searching_stock.UserSearchStock.search_stock(type_in)
    search_result = {
        'search_result1':"",
        'search_result2':"",
        'search_result3':"",
        'search_result4':"",
        'search_result5':""
    }

    if  type(search_company) is str :
        search_result['search_result1'] = search_company
    else :    
        for i in range(0, len(search_company)):
            code = search_company["銘柄コード"].values[i]
            company = search_company["会社名"].values[i]
            search_result[f"search_result{i+1}"] = f"{code}：{company}"
    return search_result


def send_views_msg_could_search_or_not(read_li: list, stock_code: dict) -> dict:

    query_msg = {"msg":"Nan"}

    if 4 <= len(read_li) :
        query_msg['msg'] = "最大取得銘柄数に達しています。"
    #マイナス１は銘柄未選択のセットを排除する為
    elif stock_code not in read_li :
        query_msg["msg"] = "データの検索が成功しました、検索を終了したい場合はポップアップを閉じてください。"

    else:
        query_msg["msg"] = "既に追加されているコードです。"
    return query_msg
    
def send_views_result_analytics(tickers: list) -> dict:

    optimize_result = {
            "msg": "Nan",
            "keys0" : "未選択",
            "keys1" : "未選択",
            "keys2" : "未選択",
            "keys3" : "未選択",
            "values0" : "ー",
            "values1" : "ー",
            "values2" : "ー",
            "values3" : "ー",
            "return": "ー",
            "risk": "ー",
            "sharpratio": "ー",
            "stock": tickers
    }

    if len(tickers) <= 1 :
        optimize_result["msg"] = "エラー：2銘柄以上を選択してください。"
    else:
        for x in glob.glob('./flaskr/static/img/result*jpg'):
            os.remove(x)
        plotting = analyzing_stock.PlottingStockPrice(tickers)
        optimizing = analyzing_stock.OptimizingPortfolio(tickers)
        plotting.operate()
        try:
            weight_keys, weight_values, return_risk_sharpratio = optimizing.operate() 
        except Exception:
            optimize_result["msg"] = "エラー：最適化に失敗しました、別の組み合わせを選択してください。"
        else :
            optimize_result["msg"] = "最適ポートフォリオの出力に成功しました。"
            for i in range(len(weight_keys)):
                optimize_result[f"keys{i}"] =  weight_keys[i]
                optimize_result[f"values{i}"] = weight_values[i]
            optimize_result["return"] = round(return_risk_sharpratio[0],4)
            optimize_result["risk"] = round(return_risk_sharpratio[1],4)
            optimize_result["sharpratio"] = round(return_risk_sharpratio[2],4)
    
    return optimize_result