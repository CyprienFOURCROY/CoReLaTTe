import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    se = tables["ii_se"]

    # Members aged 60 or older in Oaxaca (ent == 20)
    seniors = portad[(portad["ent"] == 20) & (portad["edad"] >= 60)]

    # Households that feel unsafe at home (vlh04 in 1 or 2)
    unsafe = vlh[vlh["vlh04"].isin([1, 2])][["folio"]]

    # Households with a death in the last five years (se01a == 1)
    death = se[se["se01a"] == 1][["folio"]]

    df = seniors.merge(unsafe, on="folio", how="inner").merge(death, on="folio", how="inner")
    count = len(df)

    return pd.DataFrame({"n_households": [count]})
