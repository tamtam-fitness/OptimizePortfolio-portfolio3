import glob
import os

from flask import (
    Blueprint,
    jsonify,
    render_template, 
    request
)

from . import models
from  flaskr import stock_df 

#ルーティングの作成
bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def index():
    """index.htmlの生成する関数"""
    weight_keys = ["未選択","未選択","未選択","未選択"]
    weight_values = ["ー","ー","ー","ー"]
    return_risk_sharpratio =["ー","ー","ー"]
    return render_template('index.html',
                            weight_keys=weight_keys,
                            weight_values=weight_values,
                            return_risk_sharpratio=return_risk_sharpratio
                            )

@bp.route('/_type_in_stock')
def type_in_stock():
    """選択した銘柄が存在するか判定し、あれば出力する関数"""

    type_in = request.args.get('stock', None, type=str)
    search_company = models.UserSearchStock.search_stock(type_in)
    search_result= {
        'search_result1':"",
        'search_result2':"",
        'search_result3':"",
        'search_result4':"",
        'search_result5':""
    }

    if  type(search_company) is str :
        search_result['search_result1'] = search_company
        return jsonify(search_result)
    else :    
        for i in range(0, len(search_company)):
            code = search_company["銘柄コード"].values[i]
            company = search_company["会社名"].values[i]
            search_result[f"search_result{i+1}"] = f"{code}：{company}"
        return jsonify(search_result)


@bp.route('/_memorize_stock_code')
def memorize_stock_code():
    stock_code = request.args.get('stock_code', None, type=str)
    read_li = []
    for i in range(1, 4+1):
        read = request.args.get(f'read{i}', None, type=str)
        if read != "銘柄：未選択":
            read_li.append(read)

    query_msg = {"msg":"Nan"}

    if 4 <= len(read_li) :
        query_msg['msg'] = "最大取得銘柄数に達しています。"
    #マイナス１は銘柄未選択のセットを排除する為
    elif stock_code not in read_li :
        query_msg["msg"] = "データの検索が成功しました、検索を終了したい場合はポップアップを閉じてください。"

    else:
        query_msg["msg"] = "既に追加されているコードです。"

    return jsonify(query_msg)


@bp.route('/_optimize_result')
def optimize_portfolio():
    """
    選択した複数銘柄で、株価をプロットしたり、
    最適ポートフォリオを出力したりする関数
    """
    tickers = []
    for i in range(1, 4+1):
        read = request.args.get(f'read{i}', None, type=str)
        if read != "銘柄：未選択":
            read = read.split("：")[0]
            tickers.append(read)

    optimize_result = {
            "msg":"Nan",
            "keys0" : "未選択",
            "keys1" : "未選択",
            "keys2" : "未選択",
            "keys3" : "未選択",
            "values0" : "ー",
            "values1" : "ー",
            "values2" : "ー",
            "values3" : "ー",
            "return":"ー",
            "risk":"ー",
            "sharpratio":"ー",
            "stock":tickers
    }

    if len(tickers) <= 1 :
        optimize_result["msg"] = "エラー：2銘柄以上を選択してください。"
        return jsonify(optimize_result)
    else:
        for x in glob.glob('./flaskr/static/img/result*jpg'):
            os.remove(x)
        financial_data = models.OptimizePortfolio(tickers)
        financial_data.plot_stockprice()
        try:
            weight_keys, weight_values, return_risk_sharpratio = financial_data.optimize_portfolio()    
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
        return jsonify(optimize_result)


@bp.route('/_reload_reset_stock')
def reload_reset_stock():
    """リセットボタンを押したとき、選択情報などを初期化する関数"""
    if os.path.isfile("./flaskr/static/img/result.jpg"):
        os.remove("./flaskr/static/img/result.jpg")
    return jsonify({
        "msg":"リロードしました。"
    })
