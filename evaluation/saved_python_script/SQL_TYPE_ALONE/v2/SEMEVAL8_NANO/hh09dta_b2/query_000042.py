import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    su = tables["ii_su"]
    crh = tables["ii_crh"]

    # Households that use a plot/land for farming (su01 == 1)
    farm = su.loc[su["su01"] == 1, ["folio"]].drop_duplicates()

    # Households with bank savings (crh01_1b == 2)
    bank = crh.loc[crh["crh01_1b"] == 2, ["folio", "crh04_2"]]

    # Amount spent (taken from the debt amount column) and its average
    df = farm.merge(bank, on="folio", how="inner")
    df = df[df["crh04_2"].notna()]
    avg_spent = df["crh04_2"].mean()

    result = df[df["crh04_2"] > avg_spent][["folio", "crh04_2"]]
    result = result.rename(columns={"crh04_2": "su237"}).sort_values("su237", ascending=False)
    return result.reset_index(drop=True)
