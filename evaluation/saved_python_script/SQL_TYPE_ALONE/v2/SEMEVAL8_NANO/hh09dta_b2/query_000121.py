import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    crh = tables["ii_crh"]
    ah = tables["ii_ah"]

    # Oaxaca households (ent == 20) that use a plot for farming (su01 == 1)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])
    farm = su[(su["su01"] == 1) & su["folio"].isin(oax)]

    # Expense on agricultural workers (su237) and its average (taken over all land-using records)
    avg_workers = su.loc[su["su01"] == 1, "su237"].mean()
    high = set(farm.loc[farm["su237"] > avg_workers, "folio"])

    # Positive total debt
    debt = set(crh.loc[(crh["crh04_1"] == 1) & (crh["crh04_2"] > 0), "folio"])

    # Value of electronic devices of the selected households
    sel = high & debt
    elec = ah[ah["folio"].isin(sel)].groupby("folio", as_index=False).agg(elec_value=("ah04e_2", "max"))

    return pd.DataFrame({"avg_elec_value": [elec["elec_value"].mean()]})
