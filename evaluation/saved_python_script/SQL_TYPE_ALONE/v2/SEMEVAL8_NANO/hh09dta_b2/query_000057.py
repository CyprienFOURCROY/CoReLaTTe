import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    inr = tables["ii_inr"]

    # Oaxaca households with at least one adult
    adults = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)]
    adult_folios = set(adults["folio"])

    # Total value of electronic devices per household (missing counted as 0)
    e_val = ah.groupby("folio", as_index=False).agg(total_e_value=("ah04e_2", "sum"))
    hh = pd.DataFrame({"folio": sorted(adult_folios)}).merge(e_val, on="folio", how="left")
    hh["total_e_value"] = hh["total_e_value"].fillna(0)

    # Average over all Oaxaca adult households
    avg_value = hh["total_e_value"].mean()

    # Households that produced or sold crafts (inr02f == 1) with a value above the average
    crafts = set(inr.loc[inr["inr02f"] == 1, "folio"])
    above = hh[hh["folio"].isin(crafts) & (hh["total_e_value"] > avg_value)]

    return pd.DataFrame({"crafts_households_above_avg_count": [len(above)]})
