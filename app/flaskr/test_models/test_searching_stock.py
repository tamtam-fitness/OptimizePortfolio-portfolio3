from models.searching_stock import UserSearchStock

def test_UserSearchStock():
    user_search_stock =  UserSearchStock()
    type_in = "4751"
    _ = user_search_stock.search_stock(type_in)
    assert True
