import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inr = tables["ii_inr"]
    inn = tables["ii_in"]

    # Households that produced/sold fattening animals (inr02j == 1)
    animal_folios = set(inr.loc[inr["inr02j"] == 1, "folio"])

    # Households that received income from an Other Government Program (in01a10_1 == 1)
    gov_folios = set(inn.loc[inn["in01a10_1"] == 1, "folio"])

    # Households with at least one of the two
    eligible = animal_folios | gov_folios

    # Adults living in those households, by state
    adults = portad[(portad["edad"] >= 18) & (portad["folio"].isin(eligible))]
    by_state = adults.groupby("ent", as_index=False).agg(qualified_adults=("ls", "count"))

    # Above the average across states
    avg_adults = by_state["qualified_adults"].mean()
    result = by_state[by_state["qualified_adults"] > avg_adults]
    result = result.sort_values("qualified_adults", ascending=False).reset_index(drop=True)
    return result
