import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]

    # Members aged 60 or older
    seniors = portad[portad["edad"] >= 60]

    # Electronic device owners with a positive stated value
    dev = ah[(ah["ah03e"] == 1) & (ah["ah04e_1"] == 1) & (ah["ah04e_2"] > 0)]
    df = seniors.merge(dev[["folio", "ah04e_2"]], on="folio", how="inner")

    # Maximum device value per household, then average and count by state
    hh = df.groupby(["folio", "ent"], as_index=False).agg(hh_max_e_device_value=("ah04e_2", "max"))
    result = hh.groupby("ent", as_index=False).agg(
        avg_hh_max_e_device_value=("hh_max_e_device_value", "mean"),
        n_households=("folio", "count"),
    )
    return result.sort_values("ent").reset_index(drop=True)
