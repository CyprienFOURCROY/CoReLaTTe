import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    se = tables["ii_se"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Oaxaca households (ent == 20) with a disease/accident/hospitalization (se01b == 1)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])
    sick = set(se.loc[se["se01b"] == 1, "folio"]) & oax

    # Recorded motor vehicle value (ah04d_1 == 1), averaged over the members that own one
    veh = ah[ah["folio"].isin(sick) & (ah["ah04d_1"] == 1) & ah["ah04d_2"].notna()]
    veh_hh = veh.groupby("folio", as_index=False).agg(vehicle_value=("ah04d_2", "mean"))

    # Join with the reported total debts (crh04_1 == 1)
    debt = crh[crh["crh04_1"] == 1][["folio", "crh04_2"]]
    df = veh_hh.merge(debt, on="folio", how="inner")

    # Below the average vehicle value of these households
    avg_vehicle = df["vehicle_value"].mean()
    below = df[df["vehicle_value"] < avg_vehicle]

    return pd.DataFrame({"avg_debts_below_avg_vehicle": [below["crh04_2"].mean()]})
