import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    nna = tables["ii_nna"]
    vlh = tables["ii_vlh"]

    # Households with at least one adult (18+)
    adults = portad[portad["edad"] >= 18].groupby("folio", as_index=False).agg(ent=("ent", "min"))

    # Households with a member owning/sharing a non-agricultural business (nna01 == 1)
    business = set(nna.loc[nna["nna01"] == 1, "folio"])

    # Households that answered "Feel safe at home" (vlh04 in 1-4)
    valid = vlh[vlh["vlh04"].isin([1, 2, 3, 4])]
    df = valid[valid["folio"].isin(business)].merge(adults, on="folio", how="inner")

    total = df.groupby("ent", as_index=False).agg(total_hh=("folio", "count"))
    recent = df[df["vlh02_2"] >= 2005].groupby("ent", as_index=False).agg(recent_hh=("folio", "count"))
    by_state = total.merge(recent, on="ent", how="left").fillna(0)

    # States at or above the average post-2005 count
    avg_recent = by_state["recent_hh"].mean()
    result = by_state[by_state["recent_hh"] >= avg_recent]
    return result.sort_values("recent_hh", ascending=False).reset_index(drop=True)
