import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    crh = tables["ii_crh"]

    # Households with a reported total debts plus interest value (crh04_1 == 1)
    debt = crh.loc[crh["crh04_1"] == 1, ["folio"]]

    # Device owners (ah03e == 1), one row per owner
    owners = ah.loc[ah["ah03e"] == 1, ["folio"]]

    hh_state = portad.groupby(["folio", "ent"], as_index=False).agg(n_persons=("ls", "count"))
    df = debt.merge(owners, on="folio", how="inner").merge(hh_state, on="folio", how="inner")

    by_state = df.groupby("ent", as_index=False).agg(n_households_with_debt_and_device=("folio", "count"))
    avg_count = by_state["n_households_with_debt_and_device"].mean()
    result = by_state[by_state["n_households_with_debt_and_device"] >= avg_count]
    return result.reset_index(drop=True)
