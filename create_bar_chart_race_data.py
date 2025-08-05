
import sqlite3
import pandas as pd


class CreateBarChartRaceData:
    """
    用於建立 Bar Chart Race 動畫資料的類別，內含兩個主要方法：
    1. 產生台灣總統2024大選投票數據的累積總和。
    2. 產生 COVID-19 各國確診數據的每日前 10 名。
    """

    def adjust_datetime_format(self, x: str):
        """
        將傳入的時間字串 x 調整成 ISO 8601 格式 (YYYY-MM-DD HH:MM:SS)。
        由於日期固定為 2024-01-13，只需保留時間部分。
        
        參數:
        x (str): 原始時間字串，EX: 格式為 '113/01/13 16:30:49'
        
        回傳:
        調整後的 ISO 8601 格式時間字串 '2024-01-13 16:30:49'
        """
        _, time_part = x.split()  # # 以空白分隔，取出時間部分 (只保留 '16:30:49')
        date_part = "2024-01-13"  # 固定日期為 2024-01-13
        datetime_iso_8601 = f"{date_part} {time_part}" # 組合為 '2024-01-13 16:30:49'
        return datetime_iso_8601


    def create_cumulative_votes_by_time_candidate(self):
        """
        建立總統大選各候選人隨時間累積的投票數據。
        
        資料來源:
        - SQLite 資料庫中的投票數據
        - Excel 檔案中的投票所完成時間
        
        回傳:
        pandas.DataFrame 包含每個時間點、候選人的累積投票數。
        """
        connection = sqlite3.connect("data/taiwan_presidential_election_2024.db")

        # 撰寫 SQL 查詢，將投票所、候選人、票數進行合併與彙總
        sql_query = """
        SELECT polling_places.county,
               polling_places.polling_place,
               candidates.candidate,
               SUM(votes.votes) AS sum_votes
          FROM votes
          JOIN candidates
            ON votes.candidate_id = candidates.id
          JOIN polling_places
            ON votes.polling_place_id = polling_places.id
         GROUP BY polling_places.county,
                  polling_places.polling_place,
                  candidates.candidate;
        """
        votes_by_county_polling_place_candidate = pd.read_sql(sql_query, con=connection)
        connection.close()

        # 讀取 Excel 檔案中的投票所完成時間 (略過前3行無用標題列)
        votes_collected = pd.read_excel("data/113全國投開票所完成時間.xlsx", skiprows=[0, 1, 2])

        votes_collected.columns = ["county", "town", "polling_place", "collected_at", "number_of_voters"]  # 重新命名欄位名稱 
        votes_collected = votes_collected[["county", "town", "polling_place", "collected_at"]]  # 僅保留有用欄位 (number_of_voters 暫時不使用)

        # 設定合併時的對應欄位 key
        merge_key = ["county", "polling_place"]
        merged = pd.merge(votes_by_county_polling_place_candidate, votes_collected, left_on=merge_key, right_on=merge_key, how="left")

        # 依照每個收票時間與候選人進行 group by，並計算 sum_votes 總和
        votes_by_collected_at_candidate = merged.groupby(["collected_at", "candidate"])["sum_votes"].sum().reset_index()

        # 對每位候選人的票數進行累積總和（cumulative sum）
        votes_by_collected_at_candidate["cumulative_sum_votes"] = votes_by_collected_at_candidate.groupby("candidate")["sum_votes"].cumsum()

        # 將 collected_at 欄位的格式調整為 ISO 8601 標準格式 => 先使用 adjust_datetime_format，再用 pd.to_datetime
        votes_by_collected_at_candidate["collected_at"] = votes_by_collected_at_candidate["collected_at"].map(self.adjust_datetime_format)
        votes_by_collected_at_candidate["collected_at"] = pd.to_datetime(votes_by_collected_at_candidate["collected_at"])

        return votes_by_collected_at_candidate



    def create_covid_19_confirmed(self):
        """
        建立 COVID-19 各國每日確診數據，僅保留每天確診數前 10 名的國家。
        
        資料來源:
        - SQLite 資料庫中的 COVID-19 數據。
        
        回傳:
        pandas.DataFrame 包含每日確診數最多的前10國家與其數據。
        """

        connection = sqlite3.connect("data/covid_19.db")

        # [1] 篩選⽇期⼩於 2020-12-31 的資料，因為在這個時間點以前確診⼈數前 10 的國家排名比較有變化。
        # [2] time_series 本身就是採取累計記數的方式進行的
        sql_query = """
        SELECT reported_on,
            country,
            confirmed
        FROM time_series
        WHERE reported_on <= '2020-12-31';
        """

        covid_19_confirmed = pd.read_sql(sql_query, con=connection)
        connection.close()

        # 對每個日期進行分組，並取出當天確診數前10名的國家
        covid_19_confirmed = covid_19_confirmed.groupby("reported_on").apply(lambda x: x.nlargest(10, 'confirmed')).reset_index(drop=True)
        covid_19_confirmed["reported_on"] = pd.to_datetime(covid_19_confirmed["reported_on"])  # 將 reported_on 欄位轉為 ISO 8601 標準格式，方便排序與動畫處理    

        return covid_19_confirmed    


# 測試用函式：執行資料處理流程並印出結果
def test():
    create_bar_chart_race_data = CreateBarChartRaceData()
    cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
    covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()

    print(cumulative_votes_by_time_candidate)
    print(covid_19_confirmed)

if __name__ == "__main__":
    test()