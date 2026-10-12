import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inn = tables["ii_in"]
    vlh = tables["ii_vlh"]

    # Households with a resident aged 70 or older
    seniors = portad[portad["edad"] >= 70].groupby("folio", as_index=False).agg(state=("ent", "max"))

    # Received the '70 y mas' benefit in the last 12 months (in01a11_1 == 1)
    benefit = set(inn.loc[inn["in01a11_1"] == 1, "folio"])

    # Feel unsafe or very unsafe at home (vlh04 in 3, 4)
    unsafe = set(vlh.loc[vlh["vlh04"].isin([3, 4]), "folio"])

    df = seniors[seniors["folio"].isin(benefit & unsafe)]

    # Households per state, only states with at least 10
    result = df.groupby("state", as_index=False).agg(hh_count=("folio", "count"))
    result = result[result["hh_count"] >= 10].sort_values("hh_count", ascending=False)
    return result.reset_index(drop=True)
