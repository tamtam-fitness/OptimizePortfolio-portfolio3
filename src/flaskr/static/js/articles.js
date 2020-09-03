// ポートフォリオ理論の記事のurlを渡す関数
data = [
        {
            "path":"https://wineytrade.com/python_portfolio_01/", 
            "name":"Pythonによるポートフォリオ理論① 株式投資の資産管理をレクチャー！",
        },
        {
            "path":"https://wineytrade.com/python_portfolio_02/", 
            "name":"Pythonによるポートフォリオ理論② 株式投資の資産管理をレクチャー！",
        },
        {
            "path":"https://wineytrade.com/python_portfolio_03/", 
            "name":"Pythonによるポートフォリオ理論③ 株式投資の資産管理をレクチャー！",
        },
        {
            "path":"https://wineytrade.com/python_portfolio_04/", 
            "name":"Pythonによるポートフォリオ理論④ 株式投資の資産管理をレクチャー！",
        },
]

for (var i = 0;i < data.length; i++){
    $('<li class="article"></li>')
        .append('<a href =" '+ data[i].path +'"  target="_blank" >'+data[i].name+'</a>')
        .appendTo('#article_unit');
}

