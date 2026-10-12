import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    vlh = tables["ii_vlh"]

    # Households where a member owns a motor vehicle (ah03d == 1)
    owners = ah.loc[ah["ah03d"] == 1, ["folio"]].drop_duplicates()

    # Households reporting they feel very safe at home (vlh04 == 1)
    safe = vlh.loc[vlh["vlh04"] == 1, ["folio"]].drop_duplicates()

    df = owners.merge(safe, on="folio", how="inner")
    df = df.merge(portad.groupby("folio", as_index=False).agg(ent=("ent", "min")), on="folio", how="inner")

    # Households per state, at least 100
    result = df.groupby("ent", as_index=False).agg(n_households=("folio", "count"))
    result = result[result["n_households"] >= 100].sort_values("n_households", ascending=False)
    return result.reset_index(drop=True)
