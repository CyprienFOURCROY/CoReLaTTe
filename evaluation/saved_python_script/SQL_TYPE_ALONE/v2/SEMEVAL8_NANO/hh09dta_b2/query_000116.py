import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    inr = tables["ii_inr"]

    # One state per household
    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "max"))

    # Households that use a plot of land for farming (su01 == 1)
    land = su.loc[su["su01"] == 1, ["folio"]].drop_duplicates().merge(hh_state, on="folio", how="inner")

    # Honey-producing households (inr02i == 1) among them
    honey = inr.loc[inr["inr02i"] == 1, ["folio"]].drop_duplicates()
    land_honey = land[land["folio"].isin(honey["folio"])]

    # States with at least 3 honey-producing households
    result = land_honey.groupby("ent", as_index=False).agg(n_honey=("folio", "count"))
    result = result[result["n_honey"] >= 3].sort_values("n_honey", ascending=False).reset_index(drop=True)
    return result
