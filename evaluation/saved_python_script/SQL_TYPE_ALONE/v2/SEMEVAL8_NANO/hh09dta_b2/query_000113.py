import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    vlh = tables["ii_vlh"]

    # Adults aged 18+ in the state (ent == 15)
    adults = portad[(portad["ent"] == 15) & (portad["edad"] >= 18)][["folio", "ls", "ent"]]

    # Households that use a plot of land for cultivation (su01 == 1)
    plot = su.loc[su["su01"] == 1, ["folio"]].drop_duplicates()
    adults = adults.merge(plot, on="folio", how="inner")

    # "Feel safe at home?" (vlh04), valid answers are 1-4
    df = adults.merge(vlh[["folio", "vlh04"]], on="folio", how="inner")
    df = df[df["vlh04"].isin([1, 2, 3, 4])]

    result = df.groupby("ent", as_index=False).agg(
        n_adults_valid=("ls", "count"),
        n_adults_unsafe=("vlh04", lambda x: x.isin([3, 4]).sum()),
    )
    return result
