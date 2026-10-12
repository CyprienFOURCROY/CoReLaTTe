import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    crh = tables["ii_crh"]

    # Households that use a plot/land (su01 == 2)
    farm = su[su["su01"] == 2][["folio"]].drop_duplicates()

    # Households with a reported total debts plus interests amount (crh04_1 == 1)
    debt = crh[crh["crh04_1"] == 1][["folio", "crh04_2"]]

    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "min"))
    df = farm.merge(debt, on="folio").merge(hh_state, on="folio")

    by_state = df.groupby("ent", as_index=False).agg(n_households=("folio", "count"), avg_debt=("crh04_2", "mean"))
    by_state = by_state[by_state["n_households"] >= 20]

    overall_avg = df["crh04_2"].mean()
    result = by_state[by_state["avg_debt"] > overall_avg].sort_values("avg_debt", ascending=False)
    return result.reset_index(drop=True)
