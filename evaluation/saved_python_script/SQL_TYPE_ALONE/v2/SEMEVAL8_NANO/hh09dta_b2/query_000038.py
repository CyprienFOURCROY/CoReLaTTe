import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    se = tables["ii_se"]

    # Households that experienced a disease, accident or hospitalization in the last five years (se01b == 1)
    sick_folios = se.loc[se["se01b"] == 1, "folio"].unique()

    # Electronic device answers of those households (ah03e: owns an electronic device)
    ah_sick = ah[ah["folio"].isin(sick_folios)][["folio", "ah03e"]]
    ah_state = ah_sick.merge(portad[["folio", "ent"]].drop_duplicates("folio"), on="folio", how="inner")

    # Average per state and number of households
    state_stats = ah_state.groupby("ent").agg(
        avg_electronic_value=("ah03e", "mean"),
        respondent_count=("folio", "nunique"),
    ).reset_index()

    # Only states with at least two such households, top 10 by average
    state_stats = state_stats[state_stats["respondent_count"] >= 2]
    result = state_stats.sort_values("avg_electronic_value", ascending=False).head(10).reset_index(drop=True)
    return result
