import smtplib
import requests

# YOUR MAIL AND PASSWORD HERE
gmail_my_email = "----------------------@gmail.com"
gmail_password = "-----------------------------"

# IF YOU USE DIFFRENT MAIL DOMAIN CHANGE HERE
gmail_protocol = "smtp.gmail.com"


STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# YOUR API KEYS HERE
STOCK_API_KEY = "-------------------------------------"
NEWS_API_KEY = "----------------------------------------"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "5min",
    "apikey": STOCK_API_KEY
}

news_api_params = {
    "qInTitle": "tesla",
    "apiKey": NEWS_API_KEY
}


stock_response = requests.get(STOCK_ENDPOINT, params=stock_api_params)
stock_response.raise_for_status()
stock_data = stock_response.json()
stock_data_list = [value for (
    key, value) in stock_data["Time Series (Daily)"].items()]

yesterday_data = stock_data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = stock_data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

stock_diffrence = abs(float(yesterday_closing_price) -
                      float(day_before_yesterday_closing_price))

stock_diff_percent = (stock_diffrence / float(yesterday_closing_price))*100


def send_alert_mail(f_article):
    mes = f_article.encode("utf-8")
    with smtplib.SMTP(gmail_protocol, port=587) as connection:
        connection.starttls()
        connection.login(user=gmail_my_email, password=gmail_password)
        connection.sendmail(from_addr=gmail_my_email, to_addrs=gmail_my_email,
                            msg=f"Subject:Tesla Stock news \n\n {mes}.")


if stock_diff_percent > 1:
    news_response = requests.get(NEWS_ENDPOINT, params=news_api_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    articles = news_data["articles"]
    three_articles = articles[:3]
    formatted_article = [
        f"{STOCK_NAME}:{round(stock_diff_percent)}% Headline: {article['title']} \n Brief: {article['description']}" for article in three_articles]

    for i in formatted_article:
        send_alert_mail(i)
