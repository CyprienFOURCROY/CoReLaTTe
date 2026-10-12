import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    se = tables["ii_se"]
    su = tables["ii_su"]

    # Oaxaca households (ent == 20) that use a plot of land (su01 == 1)
    oax = set(portad.loc[portad["ent"] == 20, "folio"])
    farm = set(su.loc[su["su01"] == 1, "folio"]) & oax

    # Crop loss in the last five years (se01e: 1 lost, 3 did not lose)
    lost = set(se.loc[(se["se01e"] == 1) & se["folio"].isin(farm), "folio"])
    not_lost = set(se.loc[(se["se01e"] == 3) & se["folio"].isin(farm), "folio"])

    # Washing machine/stove value (ah04f_2), taken per member record
    ah_f = ah[["folio", "ah04f_2"]].dropna(subset=["ah04f_2"])
    avg_lost = ah_f[ah_f["folio"].isin(lost)]["ah04f_2"].mean()

    # Households that did not lose the crop with value above that average
    no_loss = ah_f[ah_f["folio"].isin(not_lost)]
    above = no_loss[no_loss["ah04f_2"] > avg_lost]

    return pd.DataFrame({"avg_wash_no_loss_above": [above["ah04f_2"].mean()]})
