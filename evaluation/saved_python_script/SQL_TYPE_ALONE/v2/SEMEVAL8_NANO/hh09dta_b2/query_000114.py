import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    crh = tables["ii_crh"]

    # Oaxaca adults
    adults = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)]
    adult_folios = set(adults["folio"])

    # Households that use a plot of land for farming
    farm_folios = set(su.loc[su["su01"] == 1, "folio"])

    # Households with numeric values for debts paid and total debt
    debt = crh[(crh["crh03_1"] == 1) & (crh["crh04_1"] == 1)][["folio", "crh04_2"]]
    debt = debt[debt["crh04_2"].notna()]

    # Average total debt over all Oaxaca households with a debt value
    oax_all = set(portad.loc[portad["ent"] == 20, "folio"])
    avg_debt = debt[debt["folio"].isin(oax_all)]["crh04_2"].mean()

    # Farming adult households above that average
    group = debt[debt["folio"].isin(adult_folios & farm_folios)]
    result = group[group["crh04_2"] > avg_debt].sort_values("crh04_2", ascending=False).reset_index(drop=True)
    return result
