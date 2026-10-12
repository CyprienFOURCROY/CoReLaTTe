import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]

    # Households with at least one adult (18+), by state
    adults = portad[portad["edad"] >= 18][["ent", "folio"]].drop_duplicates()

    # States with at least 50 such households
    state_counts = adults.groupby("ent", as_index=False).agg(n_households=("folio", "count"))
    big_states = state_counts[state_counts["n_households"] >= 50]

    # Households that own an electronic device (ah03e == 2)
    owners = ah.loc[ah["ah03e"] == 2, ["folio"]].drop_duplicates()
    df = adults[adults["folio"].isin(owners["folio"]) & adults["ent"].isin(big_states["ent"])]

    # Households owning a device that also have no member answering "no" are kept
    result = df.groupby("ent", as_index=False).agg(n_households_with_electronic=("folio", "count"))
    result = result[result["n_households_with_electronic"] >= 50]
    return result.sort_values("n_households_with_electronic", ascending=False).reset_index(drop=True)
