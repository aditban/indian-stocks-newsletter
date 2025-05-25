
import os, sys, datetime, requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv
import yfinance as yf
from transformers import pipeline
import pandas as pd
from jinja2 import Template

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
NEWSAPI_KEY = os.environ["NEWSAPI_KEY"]
smtp_user = os.environ["BREVO_SMTP_USER"]
smtp_pass = os.environ["BREVO_SMTP_PASS"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
sentiment = pipeline("sentiment-analysis", model="ProsusAI/finbert")

def fetch_news(symbol):
    base = "https://newsapi.org/v2/everything"
    params = {
        "q": symbol,
        "language": "en",
        "domains": "economictimes.com,moneycontrol.com,livemint.com",
        "pageSize": 5,
        "apiKey": NEWSAPI_KEY
    }
    r = requests.get(base, params=params, timeout=15)
    if r.status_code != 200:
        return []
    return r.json().get("articles", [])

def analyse(symbol):
    yf_sym = symbol if symbol.endswith((".NS",".BO")) else symbol + ".NS"
    price = yf.Ticker(yf_sym).fast_info.get("lastPrice")
    news = fetch_news(symbol.split('.')[0])
    labels = [sentiment(n["title"])[0]["label"] for n in news]
    signal = max(set(labels), key=labels.count) if labels else "NEUTRAL"
    return {"symbol": symbol, "price": price, "signal": signal, "news": news}

HTML_TEMPLATE = Template("""<h2>Your daily market brief – {{date}}</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Ticker</th><th>Price (INR)</th><th>Signal</th></tr>
{% for row in rows -%}
<tr>
  <td>{{row.symbol}}</td><td>{{"%.2f"|format(row.price)}}</td><td>{{row.signal}}</td>
</tr>
{% endfor %}
</table>
<p>Not financial advice. Unsubscribe by replying "STOP".</p>
""")

def send_mail(to_addr, html):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Indian Stocks Daily – " + datetime.date.today().isoformat()
    msg['From'] = "noreply@example.com"
    msg['To'] = to_addr
    msg.attach(MIMEText(html, 'html'))
    with smtplib.SMTP_SSL("smtp-relay.brevo.com", 465) as server:
        server.login(smtp_user, smtp_pass)
        server.sendmail(msg['From'], [to_addr], msg.as_string())

def main():
    # fetch subscribers
    res = supabase.table("subscribers").select("*").execute()
    for sub in res.data:
        tickers = [t if t.endswith((".NS",".BO")) else t+".NS" for t in sub["tickers"]]
        rows = [analyse(t) for t in tickers]
        html = HTML_TEMPLATE.render(date=datetime.date.today().isoformat(), rows=rows)
        send_mail(sub["email"], html)

if __name__ == "__main__":
    main()
