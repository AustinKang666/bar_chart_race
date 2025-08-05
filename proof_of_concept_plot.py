

from create_bar_chart_race_data import CreateBarChartRaceData
import plotly.express as px
import pandas as pd


create_bar_chart_race_data = CreateBarChartRaceData()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()


# 若有需要調整時間的話可改用  early_collected ，並自行更改後面的時間限制
early_collected = cumulative_votes_by_time_candidate[cumulative_votes_by_time_candidate["collected_at"] < pd.to_datetime("2024-01-13 17:30:30")]
max_cumulative_votes = early_collected["cumulative_sum_votes"].max()


'''概念驗證'''
# fig = px.bar(early_collected,
#             x="cumulative_sum_votes", y="candidate", color="candidate",
#             animation_frame="collected_at", animation_group="candidate", 
#             range_x=[0, max_cumulative_votes])

# fig.show()


'''概念驗證'''
# max_confirmed = covid_19_confirmed["confirmed"].max()
# fig = px.bar(covid_19_confirmed,
#             x="confirmed", y="country", color="country", 
#             animation_frame="reported_on", animation_group="country",
#             range_x=[0, max_confirmed])
# fig.update_yaxes(categoryorder="total ascending")
# fig.show()

