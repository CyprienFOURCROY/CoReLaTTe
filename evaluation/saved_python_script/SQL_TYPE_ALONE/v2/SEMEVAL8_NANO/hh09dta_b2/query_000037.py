import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    su = tables["ii_su"]
    inn = tables["ii_in"]

    # Oaxaca (20) or Puebla (21)
    state_folios = portad.loc[portad["ent"].isin([20, 21]), "folio"].unique()

    # Land-using households (su01 == 1) in those states
    land_folios = su.loc[su["su01"] == 1, "folio"].unique()
    state_set = set(state_folios)
    land_folios = [f for f in land_folios if f in state_set]

    # Positive direct payment from the Other Government Program
    pay = inn[inn["folio"].isin(land_folios) & (inn["in02a10"] > 0)][["folio", "in02a10"]]

    # Above the average of those land-using households
    avg_pay = pay["in02a10"].mean()
    result = pay[pay["in02a10"] > avg_pay].sort_values("in02a10", ascending=False).reset_index(drop=True)
    return result
