import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inn = tables["ii_in"]

    # Households that received Liconsa milk (in03a == 1)
    liconsa = set(inn.loc[inn["in03a"] == 1, "folio"])

    # Households with a senior aged 70+ or a child under 12
    senior = set(portad.loc[portad["edad"] >= 70, "folio"])
    child = set(portad.loc[portad["edad"] < 12, "folio"])
    target = (senior | child) & liconsa

    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "min"))
    df = hh_state[hh_state["folio"].isin(target)]

    # Households by state, above the national average per state
    by_state = df.groupby("ent", as_index=False).agg(hh_with_liconsa=("folio", "count"))
    avg_hh = by_state["hh_with_liconsa"].mean()
    result = by_state[by_state["hh_with_liconsa"] > avg_hh].sort_values("hh_with_liconsa", ascending=False)
    return result.reset_index(drop=True)
