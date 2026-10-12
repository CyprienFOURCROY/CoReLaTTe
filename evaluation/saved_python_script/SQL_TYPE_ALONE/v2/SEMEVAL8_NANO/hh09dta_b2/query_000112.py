import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Oaxaca households (ent == 20)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])

    # Households that own an electronic device (ah03e == 1)
    device = set(ah.loc[ah["ah03e"] == 1, "folio"])

    # Households with owed money (crh02_1 == 2) that made payments (crh03_1 == 1)
    debt = crh[(crh["crh02_1"] == 2) & (crh["crh03_1"] == 1)]
    debt = debt[debt["folio"].isin(oax & device)]

    # Households that paid more than the average amount
    avg_paid = debt["crh03_2"].mean()
    result = debt[debt["crh03_2"] > avg_paid][["folio", "crh03_2"]]
    result = result.sort_values("crh03_2", ascending=False).reset_index(drop=True)
    return result
