import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Adults (18+) in Oaxaca (ent == 20)
    adults = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)][["folio", "ls"]]
    oax_folios = set(portad.loc[portad["ent"] == 20, "folio"])

    # Oaxaca average of the reported total debts plus interest (crh04_1 == 1)
    debt = crh[(crh["crh04_1"] == 1) & crh["folio"].isin(oax_folios)]
    avg_debt = debt["crh04_2"].mean()
    high_debt = debt[debt["crh04_2"] > avg_debt]

    # Households that own a motor vehicle (ah03d == 1), one row per owner
    owners = ah[ah["ah03d"] == 1][["folio", "ls"]]

    # Adults of those households (one row per owner and per debt record)
    df = adults.merge(high_debt[["folio", "crh04_2"]], on="folio").merge(owners[["folio"]], on="folio")

    return pd.DataFrame({"n_individuals": [len(df)]})
