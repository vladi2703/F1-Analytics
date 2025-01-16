#!/usr/bin python3


def create_championship_winners_dataset(drivers_df, races_df, driver_standings_df):
    # Get the final race of each season
    final_races = races_df.groupby("year")["round"].max().reset_index()
    final_races = final_races.merge(
        races_df[["year", "round", "raceId"]], on=["year", "round"]
    )

    # Get the championship standings after each final race
    champions = driver_standings_df.merge(final_races[["raceId", "year"]], on="raceId")

    print(champions)
    # Get the championship winners (position=1)
    champions = champions[champions["position"] == 1]

    champions = champions.merge(
        drivers_df[["driverId", "forename", "surname", "nationality"]], on="driverId"
    )

    championship_winners = champions[
        ["year", "driverId", "forename", "surname", "nationality", "points", "wins"]
    ].copy()

    championship_winners["driver_name"] = (
        championship_winners["forename"] + " " + championship_winners["surname"]
    )
    championship_winners = championship_winners.sort_values("year")
    championship_winners = championship_winners.reset_index(drop=True)

    return championship_winners


def create_constructor_champions_dataset(
    constructors_df, constructor_standings_df, races_df
):
    # Get the final race of each season
    final_races = races_df.groupby("year")["round"].max().reset_index()
    final_races = final_races.merge(
        races_df[["year", "round", "raceId"]], on=["year", "round"]
    )

    # Get the championship standings after each final race
    champions = constructor_standings_df.merge(
        final_races[["raceId", "year"]], on="raceId"
    )

    # Get the championship winners (position=1)
    champions = champions[champions["position"] == 1]

    champions = champions.merge(
        constructors_df[["constructorId", "name", "nationality"]], on="constructorId"
    )

    constructor_champions = champions[
        ["year", "constructorId", "name", "nationality", "points", "wins"]
    ].copy()

    constructor_champions = constructor_champions.sort_values("year")

    constructor_champions = constructor_champions.reset_index(drop=True)

    return constructor_champions


if __name__ == "__main__":
    import pandas as pd

    drivers = pd.read_csv("data/drivers.csv")
    results = pd.read_csv("data/results.csv")
    races = pd.read_csv("data/races.csv")
    driver_standings = pd.read_csv("data/driver_standings.csv")

    championship_winners = create_championship_winners_dataset(
        drivers, races, driver_standings
    )

    print("\nF1 Championship Winners Dataset:")
    print("=" * 50)
    print(championship_winners.head())

    print("\nTotal number of championships:", len(championship_winners))
    print("\nNumber of championships by driver:")
    print(championship_winners["driver_name"].value_counts().head())
    print("\nNumber of championships by nationality:")
    print(championship_winners["nationality"].value_counts().head())

    constructors = pd.read_csv("data/constructors.csv")
    constructor_standings = pd.read_csv("data/constructor_standings.csv")

    constructor_champions = create_constructor_champions_dataset(
        constructors, constructor_standings, races
    )

    print("\nF1 Constructor Championship Winners Dataset:")
    print("=" * 50)
    print(constructor_champions.head())

    print("\nTotal number of championships:", len(constructor_champions))
    print("\nNumber of championships by constructor:")
    print(constructor_champions["name"].value_counts().head())
    print("\nNumber of championships by nationality:")
    print(constructor_champions["nationality"].value_counts().head())

    most_recent = constructor_champions.iloc[-1]
    print(
        f"\nMost recent constructor champion ({most_recent['year']}): {most_recent['name']}"
    )

    championship_winners.to_parquet("data/championship_winners.parquet", index=False)
    constructor_champions.to_parquet("data/constructor_champions.parquet", index=False)
    print(
        "\nDatasets saved to data/championship_winners.parquet and data/constructor_champions.parquet"
    )
