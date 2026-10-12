import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    se = tables["ii_se"]
    crh = tables["ii_crh"]
    nna = tables["ii_nna"]

    # Households with a reported total debt (crh04_1 == 1)
    debt = crh[crh["crh04_1"] == 1][["folio", "crh04_2"]]

    # Overall mean debt (over all indebted households)
    overall_mean = debt["crh04_2"].mean()

    # Households with a disease, accident or hospitalization (se01b == 1)
    sick = set(se.loc[se["se01b"] == 1, "folio"])
    df = debt[debt["folio"].isin(sick) & (debt["crh04_2"] > overall_mean)]

    # Households with at least one adult
    adults = set(portad.loc[portad["edad"] >= 18, "folio"])
    df = df[df["folio"].isin(adults)]

    hh = portad.groupby("folio", as_index=False).agg(ent=("ent", "min"))
    df = df.merge(hh, on="folio").merge(nna[["folio", "nna01"]], on="folio")

    result = df.groupby(["ent", "nna01"], as_index=False).agg(
        avg_debt_above_overall_mean=("crh04_2", "mean"),
        household_count=("folio", "count"),
    )
    return result
