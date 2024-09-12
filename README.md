# MLTrader: Machine Learning-Based Trading Strategy

## Overview

MLTrader is a machine learning-based trading strategy that uses sentiment analysis of recent news articles to make trading decisions. The strategy is designed to open long or short positions based on the sentiment of the news articles and close positions when the sentiment changes.

## Features

- **Sentiment Analysis**: Uses a pre-trained model to analyze the sentiment of news articles related to a specific stock.
- **Position Sizing**: Calculates the quantity of the symbol to buy or sell based on the cash at risk and the last price.
- **Trading Logic**: Opens long positions when the sentiment is positive and closes them when the sentiment turns negative. Opens short positions when the sentiment is negative and closes them when the sentiment turns positive.
- **Bracket Orders**: Uses bracket orders with take-profit and stop-loss prices to manage risk.

## Requirements
- Lumibot library
- [Alpaca API credentials](https://alpaca.markets/) 
- FinBERT model for sentiment analysis

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/mltrader.git
   cd mltrader
   python3 tradingbot.py
