import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Oaxaca households (ent == 20)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])

    # Households with a member owning a motor vehicle (ah03d == 1) or financial assets (ah03h == 1)
    vehicle = set(ah.loc[ah["ah03d"] == 1, "folio"])
    assets = set(ah.loc[ah["ah03h"] == 1, "folio"])
    eligible = oax & (vehicle | assets)

    # Total debts plus interest
    debt = crh[crh["folio"].isin(eligible) & crh["crh04_2"].notna()]

    return pd.DataFrame({"avg_total_debts": [debt["crh04_2"].mean()]})
