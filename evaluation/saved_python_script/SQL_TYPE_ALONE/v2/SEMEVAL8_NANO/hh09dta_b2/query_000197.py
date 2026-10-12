import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]

    # Land-using households with a chemical fertilizer expense (su01 == 1, su231 > 0)
    land = su[(su["su01"] == 1) & (su["su231"] > 0)][["folio", "su231"]]

    # Oaxaca households (ent == 20)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])
    land_oax = land[land["folio"].isin(oax)]

    # Average over the Oaxaca land-using households, households above it
    avg_exp = land_oax["su231"].mean()
    result = land_oax[land_oax["su231"] > avg_exp].sort_values("su231", ascending=False)
    return result.reset_index(drop=True)
