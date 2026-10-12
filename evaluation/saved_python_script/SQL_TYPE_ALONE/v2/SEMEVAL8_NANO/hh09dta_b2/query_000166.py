import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    se = tables["ii_se"]
    inn = tables["ii_in"]

    # Adults per household
    adults = portad[portad["edad"] >= 18].groupby("folio", as_index=False).agg(adult_count=("ls", "count"))

    # Land-using households (su01 == 1) with chemical fertilizer expense
    farm = su[su["su01"] == 1][["folio", "su231"]]

    # Total crop loss in the last five years (se01e == 1)
    lost = set(se.loc[se["se01e"] == 1, "folio"])

    # Other Government Program participation code in01a10_1 == 1
    in_prog = set(inn.loc[inn["in01a10_1"] == 1, "folio"])

    df = farm[farm["folio"].isin(lost) & farm["folio"].isin(in_prog)]
    df = df.merge(adults, on="folio", how="inner")

    result = df.groupby("adult_count", as_index=False).agg(
        avg_su231=("su231", "mean"),
        household_count=("folio", "count"),
    )
    return result.sort_values("adult_count").reset_index(drop=True)
