import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    crh = tables["ii_crh"]

    # Households that use a plot/land for farming (su01 == 1)
    farm_folios = su.loc[su["su01"] == 1, "folio"].unique()

    # Positive total debt (crh04_1 == 1 and crh04_2 > 0), summed per household
    debt = crh[(crh["crh04_1"] == 1) & (crh["crh04_2"] > 0)]
    debt_hh = debt.groupby("folio", as_index=False).agg(total_debt=("crh04_2", "sum"))
    debt_hh = debt_hh[debt_hh["folio"].isin(farm_folios)]

    # Household size and state from the person roster
    hh = portad.groupby("folio", as_index=False).agg(member_count=("ls", "count"), ent=("ent", "max"))
    df = hh.merge(debt_hh, on="folio", how="inner")

    # Average debt and average household size by state, ranked by average debt
    result = df.groupby("ent", as_index=False).agg(
        avg_household_size=("member_count", "mean"),
        avg_total_debt=("total_debt", "mean"),
    )
    result = result.sort_values("avg_total_debt", ascending=False).reset_index(drop=True)
    return result
