import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Oaxaca households (ent == 20)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])

    # Households with reported amounts owed (crh02_1 == 1) and total debts plus interest (crh04_1 == 1)
    debt = crh[(crh["crh02_1"] == 1) & (crh["crh04_1"] == 1) & crh["folio"].isin(oax)]
    debt = debt[["folio", "crh04_2"]].drop_duplicates("folio")

    # Overall average total debt and number of households
    result = pd.DataFrame({
        "avg_total_debts": [debt["crh04_2"].mean()],
        "household_count": [debt["folio"].nunique()],
    })
    return result
