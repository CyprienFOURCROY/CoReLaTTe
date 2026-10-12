import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    inr = tables["ii_inr"]

    # Number of adults (18+) per household and the average
    adults = portad[portad["edad"] >= 18].groupby("folio", as_index=False).agg(adult_count=("ls", "count"))
    avg_adults = adults["adult_count"].mean()
    many = adults[adults["adult_count"] > avg_adults]

    # Members feel unsafe or very unsafe and lived in the current home since 2005
    unsafe = vlh[(vlh["vlh04"].isin([3, 4])) & (vlh["vlh02_2"] >= 2005)][["folio"]]
    hh = many[many["folio"].isin(unsafe["folio"])]

    # Households that produced canned goods (inr02b == 1)
    canned = set(inr.loc[inr["inr02b"] == 1, "folio"])

    return pd.DataFrame({
        "denominator_households": [len(hh)],
        "numerator_households_produced_canned_goods": [hh["folio"].isin(canned).sum()],
    })
