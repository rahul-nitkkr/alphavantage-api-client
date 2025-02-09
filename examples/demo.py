"""
Demo script showing how to use the Alpha Vantage API client.
"""

import os
from pprint import pprint

from alphavantage import (
    AlphaVantageClient,
    APIError,
    RateLimitError
)

def main():
    # Initialize the client
    client = AlphaVantageClient()

    try:
        # Get company overview
        print("\n=== Company Overview ===")
        overview = client.get_company_overview(symbol="AAPL")
        print(f"Company: {overview.name}")
        print(f"Sector: {overview.sector}")
        print(f"Market Cap: ${overview.market_capitalization:,.2f}")
        print(f"PE Ratio: {overview.pe_ratio:.2f}")

        # Get income statement
        print("\n=== Latest Annual Income Statement ===")
        income_stmt = client.get_income_statement(symbol="AAPL")
        latest = income_stmt.annual_reports[0]
        print(f"Fiscal Year: {latest.fiscal_date_ending}")
        print(f"Total Revenue: ${latest.total_revenue:,.2f}")
        print(f"Net Income: ${latest.net_income:,.2f}")
        print(f"Operating Income: ${latest.operating_income:,.2f}")

        # Get balance sheet
        print("\n=== Latest Quarterly Balance Sheet ===")
        balance_sheet = client.get_balance_sheet(symbol="AAPL")
        latest = balance_sheet.quarterly_reports[0]
        print(f"Quarter: {latest.fiscal_date_ending}")
        print(f"Total Assets: ${latest.total_assets:,.2f}")
        print(f"Total Liabilities: ${latest.total_liabilities:,.2f}")
        print(f"Total Shareholder Equity: ${latest.total_shareholder_equity:,.2f}")

        # Get cash flow
        print("\n=== Latest Annual Cash Flow ===")
        cash_flow = client.get_cash_flow(symbol="AAPL")
        latest = cash_flow.annual_reports[0]
        print(f"Fiscal Year: {latest.fiscal_date_ending}")
        print(f"Operating Cashflow: ${latest.operating_cashflow:,.2f}")
        print(f"Capital Expenditures: ${latest.capital_expenditures:,.2f}")
        print(f"Dividend Payout: ${latest.dividend_payout:,.2f}")

        # Get earnings
        print("\n=== Latest Quarterly Earnings ===")
        earnings = client.get_earnings(symbol="AAPL")
        latest = earnings.quarterly_earnings[0]
        print(f"Quarter: {latest.fiscal_date_ending}")
        print(f"Reported EPS: ${latest.reported_eps:.2f}")
        print(f"Estimated EPS: ${latest.estimated_eps:.2f}")
        print(f"Surprise %: {latest.surprise_percentage:.2f}%")

        # Get news sentiment
        print("\n=== Latest News Sentiment ===")
        news = client.get_news_sentiment(
            tickers="AAPL,MSFT",
            topics="technology",
            limit=3
        )
        for item in news.feed:
            print(f"\nTitle: {item.title}")
            print(f"Sentiment: {item.overall_sentiment_label}")
            if item.overall_sentiment_score is not None:
                print(f"Score: {item.overall_sentiment_score:.2f}")
            print("Ticker Sentiment:")
            for ticker in item.ticker_sentiment:
                print(f"- {ticker['ticker']}: Relevance {ticker['relevance_score']}, "
                      f"Sentiment {ticker['ticker_sentiment_label']} ({ticker['ticker_sentiment_score']})")

        # Get top gainers/losers
        print("\n=== Market Movers ===")
        movers = client.get_top_gainers_losers()
        
        print("\nTop 3 Gainers:")
        for gainer in movers.top_gainers[:3]:
            print(f"{gainer.ticker}: +{gainer.change_percentage:.2f}%")
        
        print("\nTop 3 Losers:")
        for loser in movers.top_losers[:3]:
            print(f"{loser.ticker}: {loser.change_percentage:.2f}%")

    except APIError as e:
        print(f"API Error: {e.message}")
    except RateLimitError:
        print("Rate limit exceeded. Please wait before making more requests.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 