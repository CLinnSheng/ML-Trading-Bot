from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 
from finbert_utils import estimate_sentiment

"""
Short Position: Selling a security that you do not own
    Borrow the security from a broker and sell it in the market. Later, buy back the security to return it to the broker
    ideally at a lower price to make profit
    
Long Position: Buy a security with the expactation that the price will increase
    Own the security and can sell it later, ideally at a high price to make profit
"""

API_KEY = ""
API_SECRET = ""
BASE_URL = ""

ALPACA_CREDS = {
    "API_KEY" : API_KEY,
    "API_SECRET" : API_SECRET,
    "PAPER" : True
}

class MLTrader(Strategy):
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
            self.symbol = symbol
            self.sleeptime = "24H" # Daily Trading
            self.last_trade = None
            self.cash_at_risk = cash_at_risk
            self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)
    
    def position_sizing(self):
        cash = self.get_cash()
        last_price = self.get_last_price(self.symbol)
        quantity = int(self.cash * self.cash_at_risk / last_price)
        return cash, last_price, quantity
    
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing()
        probability, sentiment = self.get_sentiment()

        if cash > last_price * quantity:
            if sentiment == "positive" and probability > .88:
                if self.last_trade == "sell": # Indicating the last order is a short position
                    # Closing all the short positions because we expecting the market gonna be bullish
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    side="buy",
                    type="bracket",
                    take_profit_price=last_price*1.20,
                    stop_loss_limit_price=last_price*.95
                )
                self.submit_order(order)
                self.last_trade="buy"
            
            elif sentiment == "negative" and probability > .88:
                if self.last_trade == "buy": # Long position
                    # Closing all the long order because we expecting the market gonna be bearish
                    self.sell_all()
                order = self.create_order(
                    self.symbol,
                    quantity,
                    side="sell",
                    type="bracket",
                    take_profit_price=last_price*0.80,
                    stop_loss_limit_price=last_price*1.05
                )
                self.submit_order(order)
                self.last_trade="sell"
                
    def get_dates(self):
        today = self.get_datetime()
        threedays_prior = today - Timedelta(days=3)        
        return today.strftime("%Y-%m-%d"), threedays_prior.strftime("%Y-%m-%d")

    def get_sentiment(self):
        today, threedays_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=threedays_prior, end=today)
        news = [new.__dict__["_raw"]["summary"] for new in news]
        return estimate_sentiment(news)

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 5, 30)

broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name="mlstrat", broker=broker, parameters={"symbol":"SPY",
                                                               "cash_at_risk":.5})

# strategy.backtest(
#     YahooDataBacktesting,
#     start_date,
#     end_date,
#     parameters={"symbol" : "SPY"}
# )

trader = Trader()
trader.add_strategy(strategy)
trader.run_all()
