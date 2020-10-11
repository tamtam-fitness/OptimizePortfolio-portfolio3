from flask import (
    Blueprint,
    jsonify,
    render_template, 
    request
)

from . import models_bundle

#ルーティングの作成
bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def index():
    """index.htmlの生成する関数"""
    weight_keys, weight_values, return_risk_sharpratio = models_bundle.send_views_index()
    return render_template('index.html',
                            weight_keys=weight_keys,
                            weight_values=weight_values,
                            return_risk_sharpratio=return_risk_sharpratio
                            )


@bp.route('/_type_in_stock')
def type_in_stock():
    """選択した銘柄が存在するか判定し、あれば出力する関数"""
    type_in = request.args.get('stock', None, type=str)
    searched_result = models_bundle.send_views_result_search_stock(type_in)
    return jsonify(searched_result)


@bp.route('/_memorize_stock_code')
def memorize_stock_code():
    stock_code = request.args.get('stock_code', None, type=str)
    read_li = []
    for i in range(1, 4+1):
        read = request.args.get(f'read{i}', None, type=str)
        if read != "銘柄：未選択":
            read_li.append(read)
    query_msg = models_bundle.send_views_msg_could_search_or_not(read_li, stock_code)
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
    optimize_result = models_bundle.send_views_result_analytics(tickers)
    return jsonify(optimize_result)
