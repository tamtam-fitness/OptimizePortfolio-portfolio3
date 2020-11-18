from models.analyzing_stock import PlottingStockPrice, OptimizingPortfolio


def test_OptimizingPortfolio():
    tickers = ["4755", "3938"]
    optimizing_portfolio = OptimizingPortfolio(tickers)
    weight_keys, _, _ = optimizing_portfolio.operate()
    assert weight_keys == ["4755.T", "3938.T","未選択","未選択"]





    
