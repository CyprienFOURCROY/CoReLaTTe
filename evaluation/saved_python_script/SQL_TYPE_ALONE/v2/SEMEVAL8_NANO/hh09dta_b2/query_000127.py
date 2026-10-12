import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    se = tables["ii_se"]
    vlh = tables["ii_vlh"]

    # Households that reported none of the six shocks (all answers equal to 3)
    no_shock_mask = (
        (se["se01a"] == 3) & (se["se01b"] == 3) & (se["se01c"] == 3)
        & (se["se01d"] == 3) & (se["se01e"] == 3) & (se["se01f"] == 3)
    )
    no_shock = set(se.loc[no_shock_mask, "folio"])

    # Average number of times house/business/parcel was entered or robbed since 2005
    avg_all = vlh["vlh18a"].mean()

    # Households with at least one shock and more incidents than that average
    shock = vlh[~vlh["folio"].isin(no_shock)][["folio", "vlh18a"]]
    result = shock[shock["vlh18a"] > avg_all].reset_index(drop=True)
    return result
