import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    nna = tables["ii_nna"]

    # Oaxaca individuals in households that own or share a non-agricultural business
    business = set(nna.loc[nna["nna01"] == 1, "folio"])
    people = portad[(portad["ent"] == 20) & portad["folio"].isin(business)].copy()

    # Overall average age of such individuals
    avg_edad = people["edad"].mean()

    # Ordered pairs (A, B) within the same household
    pairs = people.merge(people, on="folio", suffixes=("_a", "_b"))
    pairs = pairs[pairs["edad_b"] > avg_edad]
    pairs = pairs[pairs["rel_a"] == 20]

    return pd.DataFrame({"num_pairs": [len(pairs)]})
