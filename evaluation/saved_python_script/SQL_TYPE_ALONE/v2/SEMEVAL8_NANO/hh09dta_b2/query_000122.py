import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inn = tables["ii_in"]
    nna = tables["ii_nna"]

    # Oaxaca members (ent == 20)
    oax = portad[portad["ent"] == 20]

    # Households with a positive amount directly received from the Other Government Program
    pos = inn[inn["folio"].isin(oax["folio"]) & (inn["in02a10"] > 0)]
    avg_amount = pos["in02a10"].mean()
    high = pos[pos["in02a10"] > avg_amount]

    # Own/share a non-agricultural business (nna01: 1 yes, 2 no)
    df = high[["folio"]].merge(nna[["folio", "nna01"]], on="folio", how="inner")
    df = df[df["nna01"].isin([1, 2])]

    # Average age of the members of those households (used as household size)
    members = oax[["folio", "edad"]].merge(df, on="folio", how="inner")
    result = members.groupby("nna01", as_index=False).agg(avg_hh_size=("edad", "mean"))
    return result
