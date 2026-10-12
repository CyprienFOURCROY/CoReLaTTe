import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inr = tables["ii_inr"]
    su = tables["ii_su"]

    # Households that use a plot/land for farming (su01 == 1) and produced/sold meat and eggs
    farm = set(su.loc[su["su01"] == 1, "folio"])
    both = set(inr.loc[(inr["inr02c"] == 1) & (inr["inr02d"] == 1), "folio"])
    folios = farm & both

    # Individuals of those households
    people = portad[portad["folio"].isin(folios)]
    overall_avg_age = people["edad"].mean()

    by_state = people.groupby("ent", as_index=False).agg(
        state_avg_age=("edad", "mean"),
        n_individuals=("edad", "count"),
    )

    # States with at least 10 individuals and an average age above the overall average
    result = by_state[(by_state["n_individuals"] >= 10) & (by_state["state_avg_age"] > overall_avg_age)]
    return result.sort_values("state_avg_age", ascending=False).reset_index(drop=True)
