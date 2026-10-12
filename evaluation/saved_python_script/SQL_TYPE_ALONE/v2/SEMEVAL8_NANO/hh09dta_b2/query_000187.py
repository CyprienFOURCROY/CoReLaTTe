import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    su = tables["ii_su"]
    inn = tables["ii_in"]

    # Participants in the Other Government Program (in01a10_1 == 1) with a positive amount
    prog = inn[(inn["in01a10_1"] == 1) & (inn["in02a10"] > 0)][["folio", "in02a10"]]

    # Average amount over all participants
    avg_amount = prog["in02a10"].mean()

    # Households where a member uses land for farming (su01 == 1)
    farm = su.loc[su["su01"] == 1, ["folio"]]
    df = farm.merge(prog, on="folio", how="inner")

    result = df[df["in02a10"] > avg_amount][["folio", "in02a10"]].reset_index(drop=True)
    return result
