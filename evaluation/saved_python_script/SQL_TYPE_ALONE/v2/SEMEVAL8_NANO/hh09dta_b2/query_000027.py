import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    vlh = tables["ii_vlh"]
    crh = tables["ii_crh"]

    # Adults aged 18 or older
    adults = portad[portad["edad"] >= 18]

    # Households that completely disagree that their locality is close (vlh01k == 4)
    disagree = set(vlh.loc[vlh["vlh01k"] == 4, "folio"])

    # Households with a reported total debt plus interests
    debt = set(crh.loc[crh["crh04_1"] == 1, "folio"])

    df = adults[adults["folio"].isin(disagree & debt)]

    # Total number of adults
    return pd.DataFrame({"adult_count": [len(df)]})
