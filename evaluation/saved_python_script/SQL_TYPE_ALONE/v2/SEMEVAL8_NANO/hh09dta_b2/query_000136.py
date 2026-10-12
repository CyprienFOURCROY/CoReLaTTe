import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inn = tables["ii_in"]
    inr = tables["ii_inr"]

    # Households with a positive amount directly received from an Other Government Program
    recip = inn[inn["in02a10"] > 0][["folio"]].drop_duplicates()
    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "min"))
    df = recip.merge(hh_state, on="folio", how="inner")

    # Households per state, at least 30
    by_state = df.groupby("ent", as_index=False).agg(n_hh_qualifying=("folio", "count"))
    by_state = by_state[by_state["n_hh_qualifying"] >= 30]

    # Households that produced or sold dairy products (inr02a == 1) in the whole survey, by state
    dairy = inr.loc[inr["inr02a"] == 1, ["folio"]].drop_duplicates().merge(hh_state, on="folio", how="inner")
    dairy_by_state = dairy.groupby("ent", as_index=False).agg(n_dairy_yes=("folio", "count"))

    result = by_state.merge(dairy_by_state, on="ent", how="left")
    return result
