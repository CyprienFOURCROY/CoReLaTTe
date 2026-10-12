import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    se = tables["ii_se"]

    # Households that reported a death in the last five years (se01a == 1)
    death = se.loc[se["se01a"] == 1, ["folio"]].drop_duplicates()

    # Households with at least one adult (18+)
    adults = portad[portad["edad"] >= 18].groupby("folio", as_index=False).agg(n_adults=("ls", "count"))

    hh_state = portad.groupby("folio", as_index=False).agg(ent=("ent", "max"))
    df = death.merge(hh_state, on="folio", how="inner")
    df = df.merge(adults, on="folio", how="left")

    result = df.groupby("ent", as_index=False).agg(
        numerator_households=("n_adults", lambda x: (x > 0).sum()),
        denominator_households=("folio", "count"),
    )
    return result
