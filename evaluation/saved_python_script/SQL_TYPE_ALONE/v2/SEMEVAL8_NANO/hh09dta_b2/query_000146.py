import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    inn = tables["ii_in"]

    # Oaxaca (ent == 20) households with at least one member aged 18+
    adults = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)]
    adult_folios = set(adults["folio"])

    # Households that use a plot of land for sowing/farming (su01 == 1)
    farm_folios = set(su.loc[su["su01"] == 1, "folio"])

    # Participated in the Other Government Program (in01a10_1 in 1, 2) with a positive direct amount
    prog = inn[inn["in01a10_1"].isin([1, 2]) & (inn["in02a10"] > 0)]
    prog_folios = set(prog["folio"])

    count = len(adult_folios & farm_folios & prog_folios)
    return pd.DataFrame({"n_households": [count]})
