"""Alpha Vantage API Client implementation."""

import os
import logging
from typing import Any, Dict, Optional
import requests
from dotenv import load_dotenv
from pprint import pprint

from .exceptions import APIError, APIKeyError, InvalidParameterError, RateLimitError
from .models import (
    BalanceSheet,
    CashFlow,
    CompanyOverview,
    Earnings,
    IncomeStatement,
    NewsSentimentResponse,
    TopGainersLosers,
)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler with formatting
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class AlphaVantageClient:
    """
    Alpha Vantage API client for accessing various financial data endpoints.
    
    Args:
        api_key (str, optional): Alpha Vantage API key. If not provided, will look for ALPHA_VANTAGE_API_KEY environment variable.
        base_url (str, optional): Base URL for the API. Defaults to the official Alpha Vantage API URL.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://www.alphavantage.co/query"
    ):
        load_dotenv()
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            logger.error("No API key provided")
            raise APIKeyError(
                "No API key provided. Pass it as argument or set ALPHA_VANTAGE_API_KEY environment variable."
            )
        self.base_url = base_url
        self.session = requests.Session()
        logger.info("AlphaVantage client initialized with base URL: %s", base_url)

    def _make_request(
        self,
        function: str,
        **params: Any
    ) -> Dict[str, Any]:
        """
        Make a request to the Alpha Vantage API.
        
        Args:
            function: The API function to call
            **params: Additional parameters to pass to the API
            
        Returns:
            Dict containing the API response
            
        Raises:
            APIError: If the API returns an error
            RateLimitError: If API rate limits are exceeded
        """
        params["function"] = function
        params["apikey"] = self.api_key
        
        # Log the request (excluding API key)
        log_params = params.copy()
        # log_params["apikey"] = "***"
        logger.info("Making API request - Function: %s, Params: %s", function, log_params)
        
        try:
            response = self.session.get(self.base_url, params=params)
            logger.debug("Response status code: %d", response.status_code)
            
            if response.status_code != 200:
                logger.error("API request failed - Status: %d, Response: %s", 
                           response.status_code, response.text)
                raise APIError(response.status_code, response.text)
                
            data = response.json()
            
            # Check for error messages in the response
            if "Error Message" in data:
                logger.error("API returned error - %s", data["Error Message"])
                raise APIError(response.status_code, data["Error Message"])
            
            if "Note" in data:
                note = data["Note"]
                logger.warning("API returned note: %s", note)
                if "API call frequency" in note:
                    logger.error("Rate limit exceeded")
                    raise RateLimitError(note)
            
            logger.info("API request successful - Function: %s", function)
            logger.debug("Response data: %s", data)
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error("Request failed - %s", str(e))
            raise APIError(500, f"Request failed: {str(e)}")

    # Stock Time Series APIs
    def get_time_series_intraday(
        self,
        symbol: str,
        interval: str = "5min",
        adjusted: bool = True,
        extended_hours: bool = True,
        month: Optional[str] = None,
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get intraday time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            interval: Time interval between two consecutive data points (1min, 5min, 15min, 30min, 60min)
            adjusted: Output adjusted data
            extended_hours: Include extended hours data
            month: A month of data in YYYY-MM format (for premium users)
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the intraday time series
        """
        if interval not in ["1min", "5min", "15min", "30min", "60min"]:
            raise InvalidParameterError(f"Invalid interval: {interval}")
            
        params = {
            "symbol": symbol,
            "interval": interval,
            "adjusted": "true" if adjusted else "false",
            "extended_hours": "true" if extended_hours else "false",
            "outputsize": outputsize,
            "datatype": datatype
        }
        
        if month:
            params["month"] = month
            return self._make_request("TIME_SERIES_INTRADAY_EXTENDED", **params)
        
        return self._make_request("TIME_SERIES_INTRADAY", **params)

    def get_time_series_daily(
        self,
        symbol: str,
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get daily time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the daily time series
        """
        return self._make_request(
            "TIME_SERIES_DAILY",
            symbol=symbol,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_time_series_daily_adjusted(
        self,
        symbol: str,
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get daily adjusted time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the daily adjusted time series
        """
        return self._make_request(
            "TIME_SERIES_DAILY_ADJUSTED",
            symbol=symbol,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_time_series_weekly(
        self,
        symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get weekly time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the weekly time series
        """
        return self._make_request(
            "TIME_SERIES_WEEKLY",
            symbol=symbol,
            datatype=datatype
        )

    def get_time_series_weekly_adjusted(
        self,
        symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get weekly adjusted time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the weekly adjusted time series
        """
        return self._make_request(
            "TIME_SERIES_WEEKLY_ADJUSTED",
            symbol=symbol,
            datatype=datatype
        )

    def get_time_series_monthly(
        self,
        symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get monthly time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the monthly time series
        """
        return self._make_request(
            "TIME_SERIES_MONTHLY",
            symbol=symbol,
            datatype=datatype
        )

    def get_time_series_monthly_adjusted(
        self,
        symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get monthly adjusted time series of the equity specified.
        
        Args:
            symbol: The stock symbol
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing the monthly adjusted time series
        """
        return self._make_request(
            "TIME_SERIES_MONTHLY_ADJUSTED",
            symbol=symbol,
            datatype=datatype
        )

    # Fundamental Data APIs
    def get_company_overview(
        self,
        symbol: str
    ) -> CompanyOverview:
        """
        Get the company information, financial ratios, and other key metrics for the equity specified.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            CompanyOverview object containing company overview data
        """
        data = self._make_request(
            "OVERVIEW",
            symbol=symbol
        )
        try:
            return CompanyOverview(**data)
        except Exception as e:
            print("Debug - API Response:")
            pprint(data)
            raise

    def get_income_statement(
        self,
        symbol: str
    ) -> IncomeStatement:
        """
        Get the annual and quarterly income statements for the company specified.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            IncomeStatement object containing income statement data
        """
        data = self._make_request(
            "INCOME_STATEMENT",
            symbol=symbol
        )
        return IncomeStatement(**data)

    def get_balance_sheet(
        self,
        symbol: str
    ) -> BalanceSheet:
        """
        Get the annual and quarterly balance sheets for the company specified.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            BalanceSheet object containing balance sheet data
        """
        data = self._make_request(
            "BALANCE_SHEET",
            symbol=symbol
        )
        return BalanceSheet(**data)

    def get_cash_flow(
        self,
        symbol: str
    ) -> CashFlow:
        """
        Get the annual and quarterly cash flows for the company specified.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            CashFlow object containing cash flow data
        """
        data = self._make_request(
            "CASH_FLOW",
            symbol=symbol
        )
        return CashFlow(**data)

    def get_earnings(
        self,
        symbol: str
    ) -> Earnings:
        """
        Get the annual and quarterly earnings for the company specified.
        
        Args:
            symbol: The stock symbol
            
        Returns:
            Earnings object containing earnings data
        """
        data = self._make_request(
            "EARNINGS",
            symbol=symbol
        )
        return Earnings(**data)

    def get_news_sentiment(
        self,
        tickers: Optional[str] = None,
        topics: Optional[str] = None,
        time_from: Optional[str] = None,
        time_to: Optional[str] = None,
        sort: str = "LATEST",
        limit: int = 50
    ) -> NewsSentimentResponse:
        """
        Get news and sentiment data for symbols or topics.
        
        Args:
            tickers: Comma-separated list of tickers
            topics: Comma-separated list of topics
            time_from: Start time (YYYYMMDDTHHMM format)
            time_to: End time (YYYYMMDDTHHMM format)
            sort: Sort order (LATEST, EARLIEST, RELEVANCE)
            limit: Number of results (1-1000)
            
        Returns:
            NewsSentimentResponse object containing news and sentiment data
        """
        params = {"sort": sort, "limit": limit}
        if tickers:
            params["tickers"] = tickers
        if topics:
            params["topics"] = topics
        if time_from:
            params["time_from"] = time_from
        if time_to:
            params["time_to"] = time_to
            
        data = self._make_request("NEWS_SENTIMENT", **params)
        return NewsSentimentResponse(**data)

    def get_top_gainers_losers(self) -> TopGainersLosers:
        """
        Get top gainers, losers, and most actively traded stocks.
        
        Returns:
            TopGainersLosers object containing market movers data
        """
        data = self._make_request("TOP_GAINERS_LOSERS")
        return TopGainersLosers(**data)

    # Forex APIs
    def get_forex_intraday(
        self,
        from_symbol: str,
        to_symbol: str,
        interval: str = "5min",
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get intraday forex data.
        
        Args:
            from_symbol: The currency to convert from
            to_symbol: The currency to convert to
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing forex data
        """
        if interval not in ["1min", "5min", "15min", "30min", "60min"]:
            raise InvalidParameterError(f"Invalid interval: {interval}")
            
        return self._make_request(
            "FX_INTRADAY",
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            interval=interval,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_forex_daily(
        self,
        from_symbol: str,
        to_symbol: str,
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get daily forex data.
        
        Args:
            from_symbol: The currency to convert from
            to_symbol: The currency to convert to
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing forex data
        """
        return self._make_request(
            "FX_DAILY",
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_forex_weekly(
        self,
        from_symbol: str,
        to_symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get weekly forex data.
        
        Args:
            from_symbol: The currency to convert from
            to_symbol: The currency to convert to
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing forex data
        """
        return self._make_request(
            "FX_WEEKLY",
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            datatype=datatype
        )

    def get_forex_monthly(
        self,
        from_symbol: str,
        to_symbol: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get monthly forex data.
        
        Args:
            from_symbol: The currency to convert from
            to_symbol: The currency to convert to
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing forex data
        """
        return self._make_request(
            "FX_MONTHLY",
            from_symbol=from_symbol,
            to_symbol=to_symbol,
            datatype=datatype
        )

    # Crypto APIs
    def get_crypto_intraday(
        self,
        symbol: str,
        market: str,
        interval: str = "5min",
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get intraday cryptocurrency data.
        
        Args:
            symbol: The cryptocurrency symbol
            market: The market to get data from
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing cryptocurrency data
        """
        if interval not in ["1min", "5min", "15min", "30min", "60min"]:
            raise InvalidParameterError(f"Invalid interval: {interval}")
            
        return self._make_request(
            "CRYPTO_INTRADAY",
            symbol=symbol,
            market=market,
            interval=interval,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_crypto_daily(
        self,
        symbol: str,
        market: str,
        outputsize: str = "compact",
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get daily cryptocurrency data.
        
        Args:
            symbol: The cryptocurrency symbol
            market: The market to get data from
            outputsize: Output size (compact/full)
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing cryptocurrency data
        """
        return self._make_request(
            "DIGITAL_CURRENCY_DAILY",
            symbol=symbol,
            market=market,
            outputsize=outputsize,
            datatype=datatype
        )

    def get_crypto_weekly(
        self,
        symbol: str,
        market: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get weekly cryptocurrency data.
        
        Args:
            symbol: The cryptocurrency symbol
            market: The market to get data from
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing cryptocurrency data
        """
        return self._make_request(
            "DIGITAL_CURRENCY_WEEKLY",
            symbol=symbol,
            market=market,
            datatype=datatype
        )

    def get_crypto_monthly(
        self,
        symbol: str,
        market: str,
        datatype: str = "json"
    ) -> Dict[str, Any]:
        """
        Get monthly cryptocurrency data.
        
        Args:
            symbol: The cryptocurrency symbol
            market: The market to get data from
            datatype: Output format (json/csv)
            
        Returns:
            Dict containing cryptocurrency data
        """
        return self._make_request(
            "DIGITAL_CURRENCY_MONTHLY",
            symbol=symbol,
            market=market,
            datatype=datatype
        ) 