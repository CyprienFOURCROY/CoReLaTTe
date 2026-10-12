import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    ah = tables["ii_ah"]

    # Adults (18+) in Oaxaca (ent == 20)
    adults = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)][["folio", "ls", "edad"]]

    # Forced-entry robbery of the current dwelling since 2005 (vlh12a_a == 1)
    robbed = set(vlh.loc[vlh["vlh12a_a"] == 1, "folio"])
    adults = adults[adults["folio"].isin(robbed)]

    # Any household member owns poultry (ah03m == 1)
    poultry = ah.groupby("folio", as_index=False).agg(any_poultry=("ah03m", lambda x: int((x == 1).any())))
    adults = adults.merge(poultry, on="folio", how="left")
    adults["any_poultry"] = adults["any_poultry"].fillna(0).astype(int)

    rows = []
    for flag, group in adults.groupby("any_poultry"):
        group_mean = group["edad"].mean()
        rows.append({
            "any_poultry": flag,
            "mean_age": group_mean,
            "n_older": int((group["edad"] > group_mean).sum()),
        })
    return pd.DataFrame(rows)
