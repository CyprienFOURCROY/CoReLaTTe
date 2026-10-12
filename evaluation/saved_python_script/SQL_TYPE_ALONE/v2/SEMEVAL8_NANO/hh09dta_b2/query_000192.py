import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inr = tables["ii_inr"]
    su = tables["ii_su"]

    # Households that reported producing/selling eggs (inr02d == 1), eggs sold last month (inr04d)
    eggs = inr[inr["inr02d"] == 1].groupby("folio", as_index=False).agg(eggs_last_month_total=("inr04d", "sum"))

    # Households that use a plot of land (su01 == 1)
    farm = set(su.loc[su["su01"] == 1, "folio"])
    eggs = eggs[eggs["folio"].isin(farm)]

    # Oaxaca households (ent == 20)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])
    eggs_oax = eggs[eggs["folio"].isin(oax)]

    # Average over Oaxaca households, and households strictly above it
    avg_eggs = eggs_oax["eggs_last_month_total"].mean()
    result = eggs_oax[eggs_oax["eggs_last_month_total"] > avg_eggs]
    return result[["folio", "eggs_last_month_total"]].reset_index(drop=True)
