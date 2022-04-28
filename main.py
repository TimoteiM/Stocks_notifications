import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "8T27DSW7HDAMYXCT"
NEWS_API_KEY = "90a12f6a03d14634a945ff60bf98b002"

TWILIO_SID = "AC6a047d46063858cd531c43153fcf51a9"
TWILIO_AUTH_TOKEN = "0baf0223d9d99809b1d5251b63bae546"

stock_params = {
    "apikey": STOCK_API_KEY,
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()

stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]

yesterday_data = data_list[0]
yesterday_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(yesterday_price)
print(day_before_yesterday_closing_price)

difference = float(yesterday_price) - float(day_before_yesterday_closing_price)
up_down= None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
diff_percent = round((difference / float(yesterday_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 0.5:
    news_params = {
        "apiKEY": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
        "sortBy": "relevancy"
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

three_articles = articles[:3]

formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in three_articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in formatted_articles:
    print(article)
    message = client.messages.create(
        body=article,
        from_="+14793646388",
        to="+400771435128"

    )


