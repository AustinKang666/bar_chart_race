

from create_bar_chart_race_data import CreateBarChartRaceData
import pandas as pd

# 匯入 raceplotly 的 barplot 模組，用來建立跑動長條圖
from raceplotly.plots import barplot 

# 匯入 raceplotly 的 barplot 模組，用來建立跑動長條圖
create_bar_chart_race_data = CreateBarChartRaceData()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()  # 取得累積投票數據
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()  # 取得 COVID-19 各國每日確診數據


# --- 投票數據處理部分 ---

# 針對累積投票數據進行時間範圍過濾，只取 2024-01-13 17:30:30 以前的資料
# (如果想做部分時間動畫的話，可修改這裡的時間條件)
early_collected = cumulative_votes_by_time_candidate[cumulative_votes_by_time_candidate["collected_at"] < pd.to_datetime("2024-01-13 17:30:30")]
max_cumulative_votes = early_collected["cumulative_sum_votes"].max()  # 計算累積投票數據中的最大票數，用於設定圖表 x 軸範圍

# 使用 raceplotly 的 barplot 方法，建立候選人票數隨時間跑動的 Bar Chart Race
# item_column: 設定條列項目為 candidate (候選人)
# value_column: 設定條列長度為 cumulative_sum_votes (累積票數)
# time_column: 設定時間軸為 collected_at (收票完成時間)
# top_entries: 設定每個時間點只顯示票數最多的 3 名候選人
vote_raceplot = barplot(early_collected, item_column="candidate", value_column="cumulative_sum_votes",
                        time_column="collected_at", top_entries=3)

# 繪製 bar chart race 動畫
# item_label: 設定 y 軸標籤名稱
# value_label: 設定 x 軸標籤名稱
# frame_duration: 設定每一幀 (frame) 的播放時間為 50ms (影響動畫速度)
fig = vote_raceplot.plot(item_label = "Votes collected by candidate", value_label="Cumulative votes", frame_duration=50)

fig.write_html("bar_chart_race_votes.html") # 將繪製好的動畫圖表輸出為 HTML 檔案



# --- COVID-19 確診數據處理部分 ---

# 若有需要調整 COVID-19 資料的日期範圍，可以到 create_bar_chart_race_data.py 中調整 SQL 查詢條件
# 使用 raceplotly 的 barplot 方法，建立各國確診數隨時間變化的 Bar Chart Race
# item_column: 設定條列項目為 country (國家)
# value_column: 設定條列長度為 confirmed (確診數)
# time_column: 設定時間軸為 reported_on (通報日期)
confirmed_raceplot = barplot(covid_19_confirmed, item_column="country", value_column="confirmed", time_column="reported_on")

# 繪製 COVID-19 確診數的 bar chart race 動畫
# item_label: 設定 y 軸標籤名稱
# value_label: 設定 x 軸標籤名稱 
# frame_duration: 設定每一幀 (frame) 的播放時間為 50ms
fig = confirmed_raceplot.plot(item_label = "Confirmed by country", value_label="Number of cases", frame_duration=50)

# 將 COVID-19 確診數的動畫圖表輸出為 HTML 檔案
fig.write_html("bar_chart_race_confirmed.html")
