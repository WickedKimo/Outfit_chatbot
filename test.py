import streamlit as st
from geopy.geocoders import Nominatim
import requests
from datetime import datetime
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 初始化geolocator
geolocator = Nominatim(user_agent="geoapp")

# 標題
st.title("穿搭推薦系統")

# 用戶輸入所在城市
user_location = st.text_input("請輸入你的所在城市:")

if user_location:
    location = geolocator.geocode(user_location)

    if location:
        st.write(f"{user_location} 經緯座標: {location.latitude}, {location.longitude}")
        latitude = location.latitude
        longitude = location.longitude
        today = datetime.now().date().isoformat()

        # 使用 Open-Meteo API 查詢天氣
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
              f"&hourly=temperature_2m,apparent_temperature,precipitation_probability,uv_index" \
              f"&timezone=Asia%2FTaipei&start_date={today}&end_date={today}"

        response = requests.get(url)
        data = response.json()

        temps = data["hourly"]["temperature_2m"]
        feels_like = data["hourly"]["apparent_temperature"]
        rain_prob = data["hourly"]["precipitation_probability"]
        uv_index = data["hourly"]["uv_index"]

        max_temp = max(temps)
        min_temp = min(temps)
        max_feels_like = max(feels_like)
        min_feels_like = min(feels_like)
        max_rain_prob = max(rain_prob)
        max_uv = max(uv_index)
        temp_diff = max_temp - min_temp

        # 顯示天氣資訊
        st.write(f"所在地: {today}")
        st.write(f"氣溫：{min_temp}°C~{max_temp}°C（日夜溫差{temp_diff:.1f}°C）")
        st.write(f"體感溫度：{min_feels_like}°C~{max_feels_like}°C")
        st.write(f"降雨機率（最高）：{max_rain_prob}%")
        st.write(f"紫外線指數（最高）：{max_uv}")

        # 問題：是否有特殊情況（約會/運動/無）
        special = st.selectbox("今天是否有特殊情況？", ["無", "約會", "運動"])

        # 根據天氣和特殊情況推薦穿搭
        def recommend_outfit(weather, special_occasion=None):
            suggestions = []
            max_temp = weather["max_temp"]
            temp_diff = weather["temp_diff"]
            rain_prob = weather["max_rain_prob"]
            uv = weather["max_uv"]

            if special_occasion == "約會":
                suggestions.append("建議搭配飾品，魅力up!up!")
            elif special_occasion == "運動":
                suggestions.append("建議穿著運動服裝和運動鞋，加油!")
            else:
                if max_temp < 10:
                    suggestions.append("穿羽絨外套、圍巾、毛帽")
                elif max_temp < 16:
                    suggestions.append("穿風衣或厚針織衫")
                elif max_temp < 22:
                    suggestions.append("穿薄外套或長袖上衣")
                else:
                    suggestions.append("穿短袖上衣")

                if max_temp >= 30:
                    if temp_diff <= 5:
                        suggestions.append("建議搭配短褲，涼爽為主")
                    elif 5 < temp_diff <= 10:
                        suggestions.append("建議搭配長褲，或可攜帶一件薄外套")
                else:
                    suggestions.append("建議搭配長褲")

                if temp_diff > 6:
                    suggestions.append("日夜溫差較大，建議洋蔥式穿搭")

                if rain_prob >= 50:
                    suggestions.append("有降雨機率，建議帶雨傘或穿雨衣、防水外套")
                    suggestions.append("下身可選擇防水褲、裙或短褲，避免濕透")

                if uv >= 7:
                    suggestions.append("紫外線強，請擦防曬乳、攜帶遮陽配件")

            return suggestions

        # 顯示穿搭建議
        st.write("今日穿搭建議：")
        st.write("\n".join(recommend_outfit({
            "max_temp": max_temp,
            "temp_diff": temp_diff,
            "max_rain_prob": max_rain_prob,
            "max_uv": max_uv
        }, special)))

        # 顯示圖片
        def get_random_image_with_info(path):
            if not os.path.exists(path):
                return None, "找不到資料夾"
            files = os.listdir(path)
            if not files:
                return None, "資料夾沒有圖片"
            filename = random.choice(files)
            try:
                img = Image.open(os.path.join(path, filename))
                category = path.split('_')[-1]
                return img, filename, category
            except Exception as e:
                return None, None, f"無法開啟圖片 {filename}：{e}"

        clothes_db_path = "./clothes_db"
        # 顯示圖片的代碼，與原始代碼類似

        # 顯示圖像
        fig, ax = plt.subplots(figsize=(15, 10))  # Explicitly create a figure object
        ax.axis('off')

        # 顯示圖片的邏輯與原始代碼類似

        # 顯示圖像
        st.pyplot(fig)

else:
    st.write("請輸入有效的城市名稱。")
