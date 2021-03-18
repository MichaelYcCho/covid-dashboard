import pandas as pd

daily_df = pd.read_csv("data/daily_report.csv")

# 전체 확진자, 사망자, 회복자 수
totals_df = daily_df[["Confirmed", "Deaths", "Recovered"]].sum().reset_index(name="count")
totals_df = totals_df.rename(columns={'index': "coundition"})


# 도시를 그룹화 한후 해당 도시의 확진자, 사망자, 회복자 수
countries__df = daily_df[["Country_Region", "Confirmed", "Deaths", "Recovered"]]
countries__df = daily_df.groupby("Country_Region").sum().reset_index()