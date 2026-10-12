import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    ah = tables["ii_ah"]

    # Adults in Oaxaca (ent == 20); individual ID 1 must be one of them
    oax = portad[(portad["ent"] == 20) & (portad["edad"] >= 18)]
    head = oax[oax["ls"] == 1]
    adult_folios = set(head["folio"])

    # Households that use a plot of land for cultivation (su01 == 1)
    farm_folios = set(su.loc[su["su01"] == 1, "folio"])

    # Individual with ID 1 owns a motor vehicle (ah03d == 1)
    owner = ah[(ah["ls"] == 1) & (ah["ah03d"] == 1)]
    owner_folios = set(owner["folio"])

    result = sorted(adult_folios & farm_folios & owner_folios)
    return pd.DataFrame({"folio": result})
