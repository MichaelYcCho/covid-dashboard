import pandas as pd


conditions = ["confirmed", "deaths", "recovered"]

daily_df = pd.read_csv("data/daily_report.csv")

# 전체 확진자, 사망자, 회복자 수
totals_df = daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={"index": "condition"})


# 도시를 그룹화 한후 해당 도시의 확진자, 사망자, 회복자 수
countries_df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries_df = (
            countries_df.groupby("Country_Region")
            .sum()
            .sort_values(by="Confirmed", ascending=False)
            .reset_index()
)


# 국가 리스트 DropDown 활용
dropdown_options = countries_df.sort_values("Country_Region").reset_index()
dropdown_options = dropdown_options["Country_Region"]


# 각 국가별 총확진자, 사망자, 완치자 수 
def make_country_df(country):
    def make_df(condition):
        df = pd.read_csv("data/time_confirmed.csv")
        df = df.loc[df["Country/Region"] == "Afghanistan"]
        df = df.drop(columns=["Province/State", "Country/Region", "Lat", "Long"]).sum().reset_index(name=condition)
        df = df.rename(columns = {'index': "date"})
        return df

    final_df = None

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


# 총 확진자, 사망자, 완치자 수 
def make_global_df():
    def make_df(condition):
        df = pd.read_csv(f"data/time_{condition}.csv")
        df = (
            df.drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
            .sum()
            .reset_index(name=condition)
        )
        df = df.rename(columns={"index": "date"})
        return df

    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df