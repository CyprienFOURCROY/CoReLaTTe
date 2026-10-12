import pandas as pd


def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    portad = tables["ii_portad"]
    ah = tables["ii_ah"]

    # Individuals living in households that own an electronic device (ah03e == 1)
    owners = set(ah.loc[ah["ah03e"] == 1, "folio"])
    people = portad[portad["folio"].isin(owners)]

    total = people.groupby("ent", as_index=False).agg(total_individuals_in_device_households=("ls", "count"))
    young = people[(people["edad"] >= 18) & (people["edad"] <= 24)]
    young_count = young.groupby("ent", as_index=False).agg(age18_24_count=("ls", "count"))
    df = young_count.merge(total, on="ent", how="inner")

    # States above the average (computed on the total-individuals column)
    avg_total = df["total_individuals_in_device_households"].mean()
    result = df[df["age18_24_count"] > avg_total]
    return result.sort_values("age18_24_count", ascending=False).reset_index(drop=True)
