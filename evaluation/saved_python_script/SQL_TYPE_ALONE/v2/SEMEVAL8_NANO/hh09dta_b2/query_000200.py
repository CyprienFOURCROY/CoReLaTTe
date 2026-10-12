import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    crh = tables["ii_crh"]
    inn = tables["ii_in"]

    # Households with a reported total debt (crh04_1 == 1)
    debt = crh[crh["crh04_1"] == 1][["folio", "crh04_2"]]

    # Average total debt (over all reported households)
    avg_debt = debt["crh04_2"].mean()

    # Oaxaca households above that average
    oax_folios = portad.loc[portad["ent"] == 20, "folio"].unique()
    above = debt[debt["folio"].isin(oax_folios) & (debt["crh04_2"] > avg_debt)]

    # Households that received a positive amount from the Other Government Program
    paid = inn.groupby("folio", as_index=False).agg(in_total=("in02a10", "sum"))
    paid = paid[paid["in_total"] > 0]

    count = above[above["folio"].isin(paid["folio"])]["folio"].nunique()
    return pd.DataFrame({"num_households": [count]})
