import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    inr = tables["ii_inr"]
    inn = tables["ii_in"]

    # Households with a member that produced or sold dairy products (inr02a == 1)
    dairy = set(inr.loc[inr["inr02a"] == 1, "folio"])

    # Households that received Liconsa milk (in03a == 1)
    liconsa = set(inn.loc[inn["in03a"] == 1, "folio"])

    # Total number of dairy households and of those that also received Liconsa milk
    return pd.DataFrame({
        "dairy_hh_count": [len(dairy)],
        "liconsa_and_dairy_hh_count": [len(dairy & liconsa)],
    })
