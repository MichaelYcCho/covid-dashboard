import pandas as pd


def make_global_df(condition):
    df = pd.read_csv(f"data/time_{condition}.csv")
    df = (
        df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
        .sum()
        .reset_index(name=condition)
    )
    df = df.rename(columns={"index": "date"})
    return df


daily_df = pd.read_csv("data/daily_report.csv")

# 전체 확진자, 사망자, 회복자 수
totals_df = daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={'index': "coundition"})


# 도시를 그룹화 한후 해당 도시의 확진자, 사망자, 회복자 수
countries__df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries__df = daily_df.groupby("Country_Region").sum().reset_index()


# 총 확진자, 사망자, 완치자 수 
conditions = ["confirmed", "deaths", "recovered"]

final_df = None

for condition in conditions:
    condition_df = make_global_df(condition)
    if final_df is None:
        final_df = condition_df
    else:
        final_df = final_df.merge(condition_df)