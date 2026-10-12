import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inn = tables["ii_in"]
    vlh = tables["ii_vlh"]

    # Positive amount from the Other Government Program (in01a10_1 == 1 and in02a10 > 0)
    gov = inn[(inn["in01a10_1"] == 1) & (inn["in02a10"] > 0)][["folio"]].drop_duplicates()

    # Feel unsafe or very unsafe at home (vlh04 in 3, 4)
    unsafe = vlh[vlh["vlh04"].isin([3, 4])][["folio"]].drop_duplicates()

    df = gov.merge(unsafe, on="folio", how="inner")
    df = df.merge(portad.groupby("folio", as_index=False).agg(ent=("ent", "min")), on="folio", how="inner")

    # Households by state, above the average across states
    by_state = df.groupby("ent", as_index=False).agg(qualified_count=("folio", "count"))
    avg_count = by_state["qualified_count"].mean()
    result = by_state[by_state["qualified_count"] > avg_count]
    return result.sort_values("qualified_count", ascending=False).reset_index(drop=True)
