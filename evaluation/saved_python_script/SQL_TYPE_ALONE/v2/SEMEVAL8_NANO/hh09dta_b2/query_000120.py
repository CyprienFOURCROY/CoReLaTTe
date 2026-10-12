import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]
    vlh = tables["ii_vlh"]
    crh = tables["ii_crh"]

    # Households with at least one member who owns a motor vehicle (ah03d == 1)
    owners = set(ah.loc[ah["ah03d"] == 1, "folio"])

    # Households that feel very safe at home (vlh04 == 1)
    very_safe = set(vlh.loc[vlh["vlh04"] == 1, "folio"])

    eligible = owners & very_safe

    # Total debt plus interest (crh04_1 == 1)
    debt = crh[(crh["crh04_1"] == 1) & crh["folio"].isin(eligible)]

    return pd.DataFrame({"avg_total_debt": [debt["crh04_2"].mean()]})
