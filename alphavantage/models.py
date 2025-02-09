"""Models for Alpha Vantage API responses."""

from datetime import datetime
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class CompanyOverview(BaseModel):
    """Company overview information."""
    symbol: str = Field(..., alias="Symbol")
    asset_type: str = Field(..., alias="AssetType")
    name: str = Field(..., alias="Name")
    description: str = Field(..., alias="Description")
    cik: str = Field(..., alias="CIK")
    exchange: str = Field(..., alias="Exchange")
    currency: str = Field(..., alias="Currency")
    country: str = Field(..., alias="Country")
    sector: str = Field(..., alias="Sector")
    industry: str = Field(..., alias="Industry")
    address: str = Field(..., alias="Address")
    fiscal_year_end: str = Field(..., alias="FiscalYearEnd")
    latest_quarter: str = Field(..., alias="LatestQuarter")
    market_capitalization: Optional[float] = Field(None, alias="MarketCapitalization")
    ebitda: Optional[float] = Field(None, alias="EBITDA")
    pe_ratio: Optional[float] = Field(None, alias="PERatio")
    peg_ratio: Optional[float] = Field(None, alias="PEGRatio")
    book_value: Optional[float] = Field(None, alias="BookValue")
    dividend_per_share: Optional[float] = Field(None, alias="DividendPerShare")
    dividend_yield: Optional[float] = Field(None, alias="DividendYield")
    eps: Optional[float] = Field(None, alias="EPS")
    revenue_per_share_ttm: Optional[float] = Field(None, alias="RevenuePerShareTTM")
    profit_margin: Optional[float] = Field(None, alias="ProfitMargin")
    operating_margin_ttm: Optional[float] = Field(None, alias="OperatingMarginTTM")
    return_on_assets_ttm: Optional[float] = Field(None, alias="ReturnOnAssetsTTM")
    return_on_equity_ttm: Optional[float] = Field(None, alias="ReturnOnEquityTTM")
    revenue_ttm: Optional[float] = Field(None, alias="RevenueTTM")
    gross_profit_ttm: Optional[float] = Field(None, alias="GrossProfitTTM")
    diluted_eps_ttm: Optional[float] = Field(None, alias="DilutedEPSTTM")
    quarterly_earnings_growth_yoy: Optional[float] = Field(None, alias="QuarterlyEarningsGrowthYOY")
    quarterly_revenue_growth_yoy: Optional[float] = Field(None, alias="QuarterlyRevenueGrowthYOY")
    analyst_target_price: Optional[float] = Field(None, alias="AnalystTargetPrice")
    trailing_pe: Optional[float] = Field(None, alias="TrailingPE")
    forward_pe: Optional[float] = Field(None, alias="ForwardPE")
    price_to_sales_ratio_ttm: Optional[float] = Field(None, alias="PriceToSalesRatioTTM")
    price_to_book_ratio: Optional[float] = Field(None, alias="PriceToBookRatio")
    ev_to_revenue: Optional[float] = Field(None, alias="EVToRevenue")
    ev_to_ebitda: Optional[float] = Field(None, alias="EVToEBITDA")
    beta: Optional[float] = Field(None, alias="Beta")
    fifty_two_week_high: Optional[float] = Field(None, alias="52WeekHigh")
    fifty_two_week_low: Optional[float] = Field(None, alias="52WeekLow")
    fifty_day_moving_average: Optional[float] = Field(None, alias="50DayMovingAverage")
    two_hundred_day_moving_average: Optional[float] = Field(None, alias="200DayMovingAverage")
    shares_outstanding: Optional[float] = Field(None, alias="SharesOutstanding")
    dividend_date: str = Field(..., alias="DividendDate")
    ex_dividend_date: str = Field(..., alias="ExDividendDate")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class IncomeStatementItem(BaseModel):
    """Individual income statement entry."""
    fiscal_date_ending: str = Field(..., alias="fiscalDateEnding")
    reported_currency: str = Field(..., alias="reportedCurrency")
    gross_profit: Optional[float] = Field(None, alias="grossProfit")
    total_revenue: Optional[float] = Field(None, alias="totalRevenue")
    cost_of_revenue: Optional[float] = Field(None, alias="costOfRevenue")
    cost_of_goods_and_services_sold: Optional[float] = Field(None, alias="costofGoodsAndServicesSold")
    operating_income: Optional[float] = Field(None, alias="operatingIncome")
    selling_general_and_administrative: Optional[float] = Field(None, alias="sellingGeneralAndAdministrative")
    research_and_development: Optional[float] = Field(None, alias="researchAndDevelopment")
    operating_expenses: Optional[float] = Field(None, alias="operatingExpenses")
    investment_income_net: Optional[float] = Field(None, alias="investmentIncomeNet")
    net_interest_income: Optional[float] = Field(None, alias="netInterestIncome")
    interest_income: Optional[float] = Field(None, alias="interestIncome")
    interest_expense: Optional[float] = Field(None, alias="interestExpense")
    non_interest_income: Optional[float] = Field(None, alias="nonInterestIncome")
    other_non_operating_income: Optional[float] = Field(None, alias="otherNonOperatingIncome")
    depreciation: Optional[float] = Field(None, alias="depreciation")
    depreciation_and_amortization: Optional[float] = Field(None, alias="depreciationAndAmortization")
    income_before_tax: Optional[float] = Field(None, alias="incomeBeforeTax")
    income_tax_expense: Optional[float] = Field(None, alias="incomeTaxExpense")
    interest_and_debt_expense: Optional[float] = Field(None, alias="interestAndDebtExpense")
    net_income_from_continuing_operations: Optional[float] = Field(None, alias="netIncomeFromContinuingOperations")
    comprehensive_income_net_of_tax: Optional[float] = Field(None, alias="comprehensiveIncomeNetOfTax")
    ebit: Optional[float] = Field(None, alias="ebit")
    ebitda: Optional[float] = Field(None, alias="ebitda")
    net_income: Optional[float] = Field(None, alias="netIncome")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class IncomeStatement(BaseModel):
    """Complete income statement response."""
    symbol: str
    annual_reports: List[IncomeStatementItem] = Field(..., alias="annualReports")
    quarterly_reports: List[IncomeStatementItem] = Field(..., alias="quarterlyReports")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True


class BalanceSheetItem(BaseModel):
    """Individual balance sheet entry."""
    fiscal_date_ending: str = Field(..., alias="fiscalDateEnding")
    reported_currency: str = Field(..., alias="reportedCurrency")
    total_assets: Optional[float] = Field(None, alias="totalAssets")
    total_current_assets: Optional[float] = Field(None, alias="totalCurrentAssets")
    cash_and_cash_equivalents_at_carrying_value: Optional[float] = Field(None, alias="cashAndCashEquivalentsAtCarryingValue")
    cash_and_short_term_investments: Optional[float] = Field(None, alias="cashAndShortTermInvestments")
    inventory: Optional[float] = Field(None, alias="inventory")
    current_net_receivables: Optional[float] = Field(None, alias="currentNetReceivables")
    total_non_current_assets: Optional[float] = Field(None, alias="totalNonCurrentAssets")
    property_plant_equipment: Optional[float] = Field(None, alias="propertyPlantEquipment")
    accumulated_depreciation_amortization_ppe: Optional[float] = Field(None, alias="accumulatedDepreciationAmortizationPPE")
    intangible_assets: Optional[float] = Field(None, alias="intangibleAssets")
    intangible_assets_excluding_goodwill: Optional[float] = Field(None, alias="intangibleAssetsExcludingGoodwill")
    goodwill: Optional[float] = Field(None, alias="goodwill")
    investments: Optional[float] = Field(None, alias="investments")
    long_term_investments: Optional[float] = Field(None, alias="longTermInvestments")
    short_term_investments: Optional[float] = Field(None, alias="shortTermInvestments")
    other_current_assets: Optional[float] = Field(None, alias="otherCurrentAssets")
    other_non_current_assets: Optional[float] = Field(None, alias="otherNonCurrentAssets")
    total_liabilities: Optional[float] = Field(None, alias="totalLiabilities")
    total_current_liabilities: Optional[float] = Field(None, alias="totalCurrentLiabilities")
    current_accounts_payable: Optional[float] = Field(None, alias="currentAccountsPayable")
    deferred_revenue: Optional[float] = Field(None, alias="deferredRevenue")
    current_debt: Optional[float] = Field(None, alias="currentDebt")
    short_term_debt: Optional[float] = Field(None, alias="shortTermDebt")
    total_non_current_liabilities: Optional[float] = Field(None, alias="totalNonCurrentLiabilities")
    capital_lease_obligations: Optional[float] = Field(None, alias="capitalLeaseObligations")
    long_term_debt: Optional[float] = Field(None, alias="longTermDebt")
    current_long_term_debt: Optional[float] = Field(None, alias="currentLongTermDebt")
    long_term_debt_noncurrent: Optional[float] = Field(None, alias="longTermDebtNoncurrent")
    short_long_term_debt_total: Optional[float] = Field(None, alias="shortLongTermDebtTotal")
    other_current_liabilities: Optional[float] = Field(None, alias="otherCurrentLiabilities")
    other_non_current_liabilities: Optional[float] = Field(None, alias="otherNonCurrentLiabilities")
    total_shareholder_equity: Optional[float] = Field(None, alias="totalShareholderEquity")
    treasury_stock: Optional[float] = Field(None, alias="treasuryStock")
    retained_earnings: Optional[float] = Field(None, alias="retainedEarnings")
    common_stock: Optional[float] = Field(None, alias="commonStock")
    common_stock_shares_outstanding: Optional[float] = Field(None, alias="commonStockSharesOutstanding")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class BalanceSheet(BaseModel):
    """Complete balance sheet response."""
    symbol: str
    annual_reports: List[BalanceSheetItem] = Field(..., alias="annualReports")
    quarterly_reports: List[BalanceSheetItem] = Field(..., alias="quarterlyReports")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True


class CashFlowItem(BaseModel):
    """Individual cash flow statement entry."""
    fiscal_date_ending: str = Field(..., alias="fiscalDateEnding")
    reported_currency: str = Field(..., alias="reportedCurrency")
    operating_cashflow: Optional[float] = Field(None, alias="operatingCashflow")
    payments_for_operating_activities: Optional[float] = Field(None, alias="paymentsForOperatingActivities")
    proceeds_from_operating_activities: Optional[float] = Field(None, alias="proceedsFromOperatingActivities")
    change_in_operating_liabilities: Optional[float] = Field(None, alias="changeInOperatingLiabilities")
    change_in_operating_assets: Optional[float] = Field(None, alias="changeInOperatingAssets")
    depreciation_depletion_and_amortization: Optional[float] = Field(None, alias="depreciationDepletionAndAmortization")
    capital_expenditures: Optional[float] = Field(None, alias="capitalExpenditures")
    change_in_receivables: Optional[float] = Field(None, alias="changeInReceivables")
    change_in_inventory: Optional[float] = Field(None, alias="changeInInventory")
    profit_loss: Optional[float] = Field(None, alias="profitLoss")
    cashflow_from_investment: Optional[float] = Field(None, alias="cashflowFromInvestment")
    cashflow_from_financing: Optional[float] = Field(None, alias="cashflowFromFinancing")
    proceeds_from_repayments_of_short_term_debt: Optional[float] = Field(None, alias="proceedsFromRepaymentsOfShortTermDebt")
    payments_for_repurchase_of_common_stock: Optional[float] = Field(None, alias="paymentsForRepurchaseOfCommonStock")
    payments_for_repurchase_of_equity: Optional[float] = Field(None, alias="paymentsForRepurchaseOfEquity")
    payments_for_repurchase_of_preferred_stock: Optional[float] = Field(None, alias="paymentsForRepurchaseOfPreferredStock")
    dividend_payout: Optional[float] = Field(None, alias="dividendPayout")
    dividend_payout_common_stock: Optional[float] = Field(None, alias="dividendPayoutCommonStock")
    dividend_payout_preferred_stock: Optional[float] = Field(None, alias="dividendPayoutPreferredStock")
    proceeds_from_issuance_of_common_stock: Optional[float] = Field(None, alias="proceedsFromIssuanceOfCommonStock")
    proceeds_from_issuance_of_long_term_debt_and_capital_securities_net: Optional[float] = Field(None, alias="proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet")
    proceeds_from_issuance_of_preferred_stock: Optional[float] = Field(None, alias="proceedsFromIssuanceOfPreferredStock")
    proceeds_from_repurchase_of_equity: Optional[float] = Field(None, alias="proceedsFromRepurchaseOfEquity")
    proceeds_from_sale_of_treasury_stock: Optional[float] = Field(None, alias="proceedsFromSaleOfTreasuryStock")
    change_in_cash_and_cash_equivalents: Optional[float] = Field(None, alias="changeInCashAndCashEquivalents")
    change_in_exchange_rate: Optional[float] = Field(None, alias="changeInExchangeRate")
    net_income: Optional[float] = Field(None, alias="netIncome")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class CashFlow(BaseModel):
    """Complete cash flow statement response."""
    symbol: str
    annual_reports: List[CashFlowItem] = Field(..., alias="annualReports")
    quarterly_reports: List[CashFlowItem] = Field(..., alias="quarterlyReports")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True


class EarningsItem(BaseModel):
    """Individual earnings report."""
    fiscal_date_ending: str = Field(..., alias="fiscalDateEnding")
    reported_eps: Optional[float] = Field(None, alias="reportedEPS")
    reported_date: Optional[str] = Field(None, alias="reportedDate")
    estimated_eps: Optional[float] = Field(None, alias="estimatedEPS")
    surprise: Optional[float] = Field(None)
    surprise_percentage: Optional[float] = Field(None, alias="surprisePercentage")
    report_time: Optional[str] = Field(None, alias="reportTime")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class Earnings(BaseModel):
    """Complete earnings response."""
    symbol: str
    annual_earnings: List[EarningsItem] = Field(..., alias="annualEarnings")
    quarterly_earnings: List[EarningsItem] = Field(..., alias="quarterlyEarnings")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True


class NewsSentiment(BaseModel):
    """News sentiment item."""
    title: str
    url: str
    time_published: datetime
    authors: List[str]
    summary: str
    banner_image: Optional[str] = Field(None, alias="banner_image")
    source: str
    category_within_source: str = Field(..., alias="category_within_source")
    source_domain: str = Field(..., alias="source_domain")
    topics: List[Dict[str, Union[str, float]]]
    overall_sentiment_score: Optional[float] = Field(None, alias="overall_sentiment_score")
    overall_sentiment_label: str = Field(..., alias="overall_sentiment_label")
    ticker_sentiment: List[Dict[str, Union[str, float]]] = Field(..., alias="ticker_sentiment")

    @field_validator("time_published", mode="before")
    @classmethod
    def parse_timestamp(cls, v: str) -> datetime:
        """Parse the timestamp from format YYYYMMDDTHHMMSS to datetime."""
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y%m%dT%H%M%S")
            except ValueError:
                raise ValueError(f"Invalid timestamp format: {v}")
        return v

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class NewsSentimentResponse(BaseModel):
    """Complete news sentiment response."""
    items: str = Field(..., alias="items")
    sentiment_score_definition: str = Field(..., alias="sentiment_score_definition")
    relevance_score_definition: str = Field(..., alias="relevance_score_definition")
    feed: List[NewsSentiment]

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True


class TopGainerLoser(BaseModel):
    """Individual top gainer/loser entry."""
    ticker: str
    price: Optional[float] = Field(None)
    change_amount: Optional[float] = Field(None, alias="change_amount")
    change_percentage: Optional[float] = Field(None, alias="change_percentage")
    volume: Optional[int] = Field(None)

    @field_validator("change_percentage", mode="before")
    @classmethod
    def parse_percentage(cls, v: str) -> Optional[float]:
        """Parse percentage string by removing '%' symbol."""
        if isinstance(v, str):
            try:
                return float(v.rstrip('%'))
            except ValueError:
                raise ValueError(f"Invalid percentage format: {v}")
        return v

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True
        json_encoders = {
            float: lambda v: None if v is None else float(v),
            int: lambda v: None if v is None else int(v)
        }

    @field_validator("*", mode="before")
    @classmethod
    def convert_none_str(cls, v):
        """Convert 'None' strings to None for all fields."""
        if v == "None":
            return None
        return v


class TopGainersLosers(BaseModel):
    """Complete top gainers/losers response."""
    metadata: str
    last_updated: str = Field(..., alias="last_updated")
    top_gainers: List[TopGainerLoser] = Field(..., alias="top_gainers")
    top_losers: List[TopGainerLoser] = Field(..., alias="top_losers")
    most_actively_traded: List[TopGainerLoser] = Field(..., alias="most_actively_traded")

    class Config:
        """Pydantic model configuration."""
        populate_by_name = True 