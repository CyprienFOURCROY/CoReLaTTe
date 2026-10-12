import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    crh = tables["ii_crh"]
    vlh = tables["ii_vlh"]

    # Households with at least one member aged 60 or older
    seniors = set(portad.loc[portad["edad"] >= 60, "folio"])

    # Households that feel unsafe or very unsafe at home (vlh04 in 3, 4)
    unsafe = set(vlh.loc[vlh["vlh04"].isin([3, 4]), "folio"])

    hh = portad.groupby("folio", as_index=False).agg(ent=("ent", "max"))
    hh = hh[hh["folio"].isin(seniors & unsafe)]

    # Total debt of those households, missing values counted as 0
    debt = hh.merge(crh[["folio", "crh04_2"]], on="folio", how="left")
    debt["total_debt"] = debt["crh04_2"].fillna(0)

    # State averages at or above the overall average
    state_avg = debt.groupby("ent")["total_debt"].mean()
    overall = debt["total_debt"].mean()
    state_avg = state_avg[state_avg >= overall]

    top = state_avg.idxmax()
    return pd.DataFrame({"state": [top], "avg_debt": [state_avg.max()]})
