from flaskr import models_bundle

#土日の間で週1回で株価のデータを更新
if __name__ == '__main__':
    models_bundle.update_stock()

