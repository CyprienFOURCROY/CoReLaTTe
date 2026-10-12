import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    crh = tables["ii_crh"]

    # Households with a reported total debt (crh04_1 == 1)
    debt = crh[crh["crh04_1"] == 1][["folio", "crh04_2"]]

    # National reference for the debt (highest reported household debt)
    national_ref = debt["crh04_2"].max()

    # Households that feel unsafe or very unsafe (vlh04 in 3, 4)
    unsafe = vlh[vlh["vlh04"].isin([3, 4])][["folio"]]
    df = unsafe.merge(debt, on="folio", how="inner")

    people = portad.groupby("folio", as_index=False).agg(ent=("ent", "min"), resp_age=("edad", "mean"))
    df = df.merge(people, on="folio", how="inner")

    by_state = df.groupby("ent", as_index=False).agg(
        mean_total_debt_unsafe=("crh04_2", "mean"),
        mean_age_unsafe=("resp_age", "mean"),
        n_unsafe_with_value=("folio", "count"),
    )
    result = by_state[by_state["mean_total_debt_unsafe"] > national_ref]
    return result.sort_values("mean_total_debt_unsafe", ascending=False).reset_index(drop=True)
