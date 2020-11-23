from models.operating_count_and_fetching_stock import ReadingAndWritingCount, FetchingStock, OperatingCountAndFetchingStock


def test_OperatingCountAndFetchingStock():
    reading_and_writing_count = ReadingAndWritingCount()
    fetching_stock = FetchingStock()
    operating_count_and_fetching_stock = OperatingCountAndFetchingStock(reading_and_writing_count, fetching_stock)
    stacks = operating_count_and_fetching_stock.fetch_stock_and_operate_count()
    assert isinstance(stacks, list)