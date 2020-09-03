from flaskr import create_app 

app = create_app()

#Webアプリの起動
if __name__ == '__main__':
    app.run(debug=True)
