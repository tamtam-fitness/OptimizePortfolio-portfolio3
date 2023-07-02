# 【OptimizePortfolioについての紹介】

※現在AWSの料金の問題で停止させています、起動のご要望があれば対応します

### もくじ
- 1.OptimizePortfolioの概要
- 2.OptimizePortfolioの機能一覧
- 3.OptimizePortfolioので使用している技術一覧

## 1.OptimizePortfolioの概要
OptimizePortfolioは、東京証券取引所に登録されている約3600社の株価データをもとに、
ユーザーが選択した複数銘柄のポートフォリオの 最適な投資比率（最適ポートフォリオ）を出力するWebアプリケーションです。 
これを使用することにより、ファイナンスの理論に沿った投資比率でポート フォリオを組むことが出来ます。

## 2.OptimizePortfolioの機能一覧
- ポップアップ表示
- 非同期処理にてポップアップから選択した銘柄を画面に表示
- 選択した銘柄の株価データを描画
- 選択した銘柄の最適な投資比率の計算結果を出力
- 計算結果によって得られる期待リターン・リスク・シャープレシオを出力
- 選択や計算結果の情報のリセット
- 定期的に株価データを取得しMongoDBに保存

## 3.OptimizePortfolioので使用している技術一覧
- 開発言語：Python, Bootstrap(HTML), CSS, jQuery(JavaScript)
- webサーバー:Nginx
- フレームワーク：Flask 
- データベース：MongoDB
- インフラ：AWS(Fargate, VPC, ECR, ALB), Docker(Dockerfile, docker-compose)
- その他：データ分析系ライブラリ各種使用, Models部分の一部のテスト作成

![infra](https://opop-img.s3.us-east-2.amazonaws.com/OptimizePortfolio_infra.png) 

## 使用デモ
銘柄を入力
[![Image from Gyazo](https://i.gyazo.com/7a64be0b95d511d603196870f6a81437.gif)](https://gyazo.com/7a64be0b95d511d603196870f6a81437)
最適比率を出力
[![Image from Gyazo](https://i.gyazo.com/a12d388e327ec47b6bd9340e6cab7f92.gif)](https://gyazo.com/a12d388e327ec47b6bd9340e6cab7f92)
