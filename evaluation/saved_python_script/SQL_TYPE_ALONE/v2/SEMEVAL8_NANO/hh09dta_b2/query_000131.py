import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    inr = tables["ii_inr"]
    crh = tables["ii_crh"]

    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "max"))

    # Households that use a plot/land for farming (su01 == 1)
    farm = su.loc[su["su01"] == 1, ["folio"]]

    # Households that produced or sold meat (inr02c == 1)
    meat = inr.loc[inr["inr02c"] == 1, ["folio"]].drop_duplicates()

    # Maximum amount paid on debts (crh03_2)
    paid = crh[["folio", "crh03_2"]]

    df = farm.merge(meat, on="folio").merge(paid, on="folio").merge(hh_state, on="folio")
    by_state = df.groupby("ent", as_index=False).agg(hh_count=("folio", "count"), max_paid=("crh03_2", "max"))

    # States with at least 25 households, maximum above the average of state maxima
    by_state = by_state[by_state["hh_count"] >= 25]
    avg_max = by_state["max_paid"].mean()
    result = by_state[by_state["max_paid"] > avg_max].sort_values("max_paid", ascending=False)
    return result.reset_index(drop=True)
