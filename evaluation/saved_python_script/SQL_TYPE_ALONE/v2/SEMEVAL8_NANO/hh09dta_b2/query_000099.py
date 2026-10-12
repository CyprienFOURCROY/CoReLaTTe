import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inr = tables["ii_inr"]
    ah = tables["ii_ah"]

    # Households that produced or sold fattening animals (inr02j == 1)
    sellers = inr.loc[inr["inr02j"] == 1, "folio"].unique()

    # Bull/cow asset value per household
    bull = ah.groupby("folio", as_index=False).agg(bull_value=("ah04j_2", "max"))
    bull = bull[bull["bull_value"].notna()]

    # Average bull/cow value (over all households with a recorded value)
    avg_bull_value = bull["bull_value"].mean()

    # Sellers whose value exceeds that average
    high = bull[bull["folio"].isin(sellers) & (bull["bull_value"] > avg_bull_value)]

    # Number of adults per household
    adults = portad[portad["edad"] >= 18].groupby("folio", as_index=False).agg(adult_count=("ls", "count"))
    df = high.merge(adults, on="folio", how="inner")

    return pd.DataFrame({"avg_adult_count_high_value_sellers": [df["adult_count"].mean()]})
