# Alpha Vantage API Client

A Python client for the Alpha Vantage API that provides easy access to financial market data including stocks, forex, and cryptocurrencies.

## Features

- Stock Time Series (Intraday, Daily, Weekly, Monthly)
- Fundamental Data (Company Overview, Income Statement, Balance Sheet, Cash Flow)
- Forex Data (Intraday, Daily, Weekly, Monthly)
- Cryptocurrency Data (Intraday, Daily, Weekly, Monthly)
- Type hints for better IDE support
- Automatic error handling and rate limiting
- Environment variable support for API key
- Pydantic models for type-safe response parsing

## Installation

```bash
pip install -r requirements.txt
```

## Usage

First, you'll need to get an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

You can either pass the API key directly to the client or set it as an environment variable:

```python
from alphavantage import AlphaVantageClient

# Using environment variable ALPHA_VANTAGE_API_KEY
client = AlphaVantageClient()

# Or passing API key directly
client = AlphaVantageClient(api_key="your_api_key")
```

### Examples

#### Getting Company Overview

```python
# Get company overview with type-safe response
overview = client.get_company_overview(symbol="IBM")

# Access fields with IDE autocompletion
print(f"Company: {overview.name}")
print(f"Sector: {overview.sector}")
print(f"Market Cap: {overview.market_capitalization}")
print(f"PE Ratio: {overview.pe_ratio}")
```

#### Getting Financial Statements

```python
# Get income statement
income_stmt = client.get_income_statement(symbol="IBM")

# Access annual and quarterly reports
for report in income_stmt.annual_reports:
    print(f"Fiscal Year: {report.fiscal_date_ending}")
    print(f"Total Revenue: {report.total_revenue}")
    print(f"Net Income: {report.net_income}")

# Get balance sheet
balance_sheet = client.get_balance_sheet(symbol="IBM")

# Access balance sheet items
for report in balance_sheet.quarterly_reports:
    print(f"Quarter: {report.fiscal_date_ending}")
    print(f"Total Assets: {report.total_assets}")
    print(f"Total Liabilities: {report.total_liabilities}")

# Get cash flow statement
cash_flow = client.get_cash_flow(symbol="IBM")

# Access cash flow items
for report in cash_flow.annual_reports:
    print(f"Fiscal Year: {report.fiscal_date_ending}")
    print(f"Operating Cashflow: {report.operating_cashflow}")
    print(f"Capital Expenditures: {report.capital_expenditures}")
```

#### Getting News & Sentiment

```python
# Get news sentiment for specific tickers
news = client.get_news_sentiment(
    tickers="IBM,AAPL",
    topics="technology",
    limit=10
)

# Access news items with sentiment analysis
for item in news.feed:
    print(f"Title: {item.title}")
    print(f"Sentiment: {item.overall_sentiment_label}")
    print(f"Score: {item.overall_sentiment_score}")
    
    # Access ticker-specific sentiment
    for ticker in item.ticker_sentiment:
        print(f"Ticker: {ticker['ticker']}")
        print(f"Relevance: {ticker['relevance_score']}")
```

#### Getting Market Movers

```python
# Get top gainers and losers
movers = client.get_top_gainers_losers()

# Access top gainers
print("Top Gainers:")
for gainer in movers.top_gainers:
    print(f"{gainer.ticker}: {gainer.change_percentage}%")

# Access top losers
print("\nTop Losers:")
for loser in movers.top_losers:
    print(f"{loser.ticker}: {loser.change_percentage}%")
```

## Error Handling

The client includes built-in error handling for common API issues:

- `APIKeyError`: Raised when there are issues with the API key
- `RateLimitError`: Raised when API rate limits are exceeded
- `InvalidParameterError`: Raised when invalid parameters are provided
- `APIError`: Raised for other API-related errors

Example error handling:

```python
from alphavantage import AlphaVantageClient, APIError, RateLimitError

try:
    client = AlphaVantageClient()
    overview = client.get_company_overview(symbol="INVALID")
except APIError as e:
    print(f"API Error: {e.message}")
except RateLimitError:
    print("Rate limit exceeded. Please wait before making more requests.")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 