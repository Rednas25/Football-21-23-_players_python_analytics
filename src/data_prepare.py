from pathlib import Path
import numpy as np
import pandas as pd


def to_numeric_safe(series):
    return pd.to_numeric(
        series.astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="coerce",
    )


def load_two_seasons(data_dir):
    file_2122 = Path(data_dir) / "2021-2022 Football Player Stats.csv"
    file_2223 = Path(data_dir) / "2022-2023 Football Player Stats.csv"

    df_2122 = pd.read_csv(file_2122, encoding="latin-1", sep=";").copy()
    df_2223 = pd.read_csv(file_2223, encoding="latin-1", sep=";").copy()

    df_2122["Season"] = "2021/22"
    df_2223["Season"] = "2022/23"

    return df_2122, df_2223


def harmonize_columns(df1, df2):
    common_columns = set(df1.columns).intersection(df2.columns)
    common_columns.add("Season")
    common_columns = sorted(common_columns)

    df1 = df1.loc[:, [col for col in common_columns if col in df1.columns]].copy()
    df2 = df2.loc[:, [col for col in common_columns if col in df2.columns]].copy()

    return df1, df2


def pos_tags(pos):
    if not isinstance(pos, str):
        return []

    tags = []
    for tag in ["GK", "DF", "MF", "FW"]:
        if tag in pos:
            tags.append(tag)

    return tags


def pos_group_first(pos):
    if not isinstance(pos, str):
        return "UNK"

    if "GK" in pos:
        return "GK"

    for tag in ["DF", "MF", "FW"]:
        if pos.startswith(tag):
            return tag

    for tag in ["DF", "MF", "FW"]:
        if tag in pos:
            return tag

    return "UNK"


def add_minutes_and_90s(df):
    df = df.copy()

    if "Min" in df.columns:
        df["Min"] = to_numeric_safe(df["Min"])

    if "90s" in df.columns:
        df["90s"] = to_numeric_safe(df["90s"])

    if "Min" in df.columns:
        df["90s"] = df["90s"].fillna(df["Min"] / 90.0)

    df.loc[df["90s"] == 0, "90s"] = np.nan

    return df


def add_per90(df, cols, denom_col="90s"):
    df = df.copy()

    minutes_90 = df[denom_col].astype(float)

    for col in cols:
        if col not in df.columns:
            continue

        df[col] = to_numeric_safe(df[col])
        df[f"{col}_per90"] = df[col] / minutes_90

    return df


def prepare_base_df(data_dir, min_minutes=900, drop_gk=True):
    df_2122, df_2223 = load_two_seasons(data_dir)
    df_2122, df_2223 = harmonize_columns(df_2122, df_2223)

    df = pd.concat([df_2122, df_2223], ignore_index=True)
    df = add_minutes_and_90s(df)

    if "Min" in df.columns:
        df = df[df["Min"] >= min_minutes].copy()

    if "Pos" in df.columns:
        df["Pos_tags"] = df["Pos"].apply(pos_tags)
        df["Is_hybrid"] = df["Pos_tags"].apply(lambda tags: len(tags) > 1)
        df["Pos_group"] = df["Pos"].apply(pos_group_first)

    if drop_gk and "Pos_group" in df.columns:
        df = df[df["Pos_group"] != "GK"].copy()
    elif drop_gk and "Pos" in df.columns:
        df = df[df["Pos"] != "GK"].copy()

    return df.reset_index(drop=True)