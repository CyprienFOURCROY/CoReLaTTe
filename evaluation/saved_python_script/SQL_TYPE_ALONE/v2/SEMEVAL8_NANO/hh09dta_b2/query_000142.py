import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    vlh = tables["ii_vlh"]
    nna = tables["ii_nna"]

    # Households that own or share a non-agricultural business (nna01 == 1)
    business = set(nna.loc[nna["nna01"] == 1, "folio"])

    # Households that feel unsafe or very unsafe at home
    unsafe = vlh[vlh["vlh04"].isin([5, 6]) & vlh["folio"].isin(business)]

    # Above the average number of times entered/robbed since 2005
    avg_times = unsafe["vlh18a"].mean()
    result = unsafe[unsafe["vlh18a"] > avg_times][["folio", "vlh18a", "vlh04"]]
    return result.sort_values("vlh18a", ascending=False).reset_index(drop=True)
