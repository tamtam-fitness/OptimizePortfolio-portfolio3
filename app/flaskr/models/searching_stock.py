from . import stock_df

class UserSearchStock(object):
    #土日（証券市場）が閉まっている時に、一週間毎にDの株価を更新するクラス

    @staticmethod
    def search_stock(type_in: str):
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
        