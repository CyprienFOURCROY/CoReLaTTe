import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    crh = tables["ii_crh"]

    # Oaxaca households where every member is 60 or older
    oax = portad[portad["ent"] == 20]
    min_age = oax.groupby("folio", as_index=False).agg(min_age=("edad", "min"))
    seniors = set(min_age.loc[min_age["min_age"] >= 60, "folio"])

    # Feel unsafe or very unsafe at home (vlh04 in 3, 4)
    unsafe = set(vlh.loc[vlh["vlh04"].isin([3, 4]), "folio"])

    # Incurred credit/loan debt in the last 12 months with a stated amount
    debt = set(crh.loc[(crh["crh02_1"] == 1) & crh["crh02_2"].notna(), "folio"])

    count = len(seniors & unsafe & debt)
    return pd.DataFrame({"n_households_qualifying": [count]})
