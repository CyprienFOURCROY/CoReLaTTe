import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    crh = tables["ii_crh"]
    vlh = tables["ii_vlh"]

    # Households with an amount owed on credit/loans (crh02_1 == 1)
    owed = crh.loc[crh["crh02_1"] == 1, ["folio", "crh02_2"]]

    # Number of house/business/parcel robberies since 2005 (vlh18a)
    rob = vlh[["folio", "vlh18a"]]
    df = owed.merge(rob, on="folio", how="inner")

    # Average among indebted households with any robbery
    avg_rob = df.loc[df["vlh18a"] > 0, "vlh18a"].mean()

    result = df[df["vlh18a"] > avg_rob][["folio", "vlh18a", "crh02_2"]].reset_index(drop=True)
    return result
