from geopy.geocoders import Nominatim
import requests
from datetime import datetime
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

geolocator = Nominatim(user_agent="geoapp")  # 請將 'my-application' 替換為您的應用程式名稱

user_location = input("你的所在城市 :")
location = geolocator.geocode(user_location)

if location:
    print(f"{user_location} 經緯座標: {location.latitude}, {location.longitude}")
else:
    print(f"找不到 {user_location} 的經緯度資訊。請檢查城市名稱是否正確。")

latitude = location.latitude
longitude = location.longitude
today = datetime.now().date().isoformat()

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

print(f"所在地 {today}")
print(f"氣溫：{min_temp}°C~{max_temp}°C（日夜溫差{temp_diff:.1f}°C）")
print(f"體感溫度：{min_feels_like}°C~{max_feels_like}°C")
print(f"降雨機率（最高）：{max_rain_prob}%")
print(f"紫外線指數（最高）：{max_uv}")

# 您的天氣資料和穿搭建議函式 (保持不變)
weather = {
    "max_temp": max_temp,
    "temp_diff": temp_diff,
    "max_rain_prob": max_rain_prob,
    "max_uv": max_uv
}
#增加不同場合
special = input("今天是否有特殊情況 (約會/運動/無): ")

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
        # 一般情況的穿搭建議
        if max_temp < 10:
            suggestions.append("穿羽絨外套、圍巾、毛帽")
        elif max_temp < 16:
            suggestions.append("穿風衣或厚針織衫")
        elif max_temp < 22:
            suggestions.append("穿薄外套或長袖上衣")
        else:
            suggestions.append("穿短袖上衣")

        # 下身建議
        if max_temp >= 30:
            if temp_diff <= 5:
                suggestions.append("建議搭配短褲，涼爽為主")
            elif 5 < temp_diff <= 10:
                suggestions.append("建議搭配長褲，或可攜帶一件薄外套")
        else:
            suggestions.append("建議搭配長褲") # 預設搭配長褲

        # 溫差提醒
        if temp_diff > 6:
            suggestions.append("日夜溫差較大，建議洋蔥式穿搭")

        # 雨具建議
        if rain_prob >= 50:
            suggestions.append("有降雨機率，建議帶雨傘或穿雨衣、防水外套")
            suggestions.append("下身可選擇防水褲、裙或短褲，避免濕透")

        # 紫外線提醒
        if uv >= 7:
            suggestions.append("紫外線強，請擦防曬乳、攜帶遮陽配件")

    return suggestions

# 獲取 OneDrive 桌面上的 clothes_db 路徑 
# onedrive_desktop_path = os.path.join(os.path.expanduser('~'), "OneDrive", "Desktop")
clothes_db_path = "./clothes_db"

def get_random_image_with_info(path):
    # 修改此函式以返回圖片物件和相關資訊 (例如：類別、描述)
    # print(f"正在檢查路徑：{path}")
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

max_temp = weather["max_temp"]
temp_diff = weather["temp_diff"]
max_rain_prob = weather["max_rain_prob"]

top_category = ""
outwear_category=""
bottom_category = ""
rain_categories = []

# 根據特殊情況和天氣設定圖片類別
if special == "約會":
    top_category = "date_"
    
elif special == "運動":
    top_category = "sport_"
    bottom_category = "sports_"

else: # 沒有特殊情況
    if max_temp < 16:
        outwear_category = "coats_"
    elif max_temp < 22:
        outwear_category = "jackets_"

    if max_temp < 22:
        top_category = "longsleeves_"
    else:
        top_category = "tshirts_"

    if max_temp >= 30:
        if temp_diff <= 5:
            bottom_category = "shorts_"
        elif 5 < temp_diff <= 10:
            bottom_category = "pants_"
        else:
            bottom_category = "pants_"
    else:
        bottom_category = "pants_"

if max_rain_prob >= 50:
    rain_categories = ["raincoat_", "umbrella_"]
    
#底圖
plt.figure(figsize=(15, 10)) 
plt.axis('off')


# 顯示文字 
plt.text(0.1, 0.95, "今日穿搭建議：\n" + "\n".join(recommend_outfit(weather,special)), transform=plt.gcf().transFigure, fontsize=12, verticalalignment='top')

# 顯示圖片
image_count = 0
positions = [(0.2, 0.6), (0.4, 0.6), (0.6, 0.6), (0.8, 0.6),  # 上身和下身
             (0.3, 0.3), (0.5, 0.3), (0.7, 0.3)] # 雨具等

#外套圖片
if outwear_category: 
    outwear_path = os.path.join(clothes_db_path, "outwears_", outwear_category)
    outwear_img_pil, outwear_img_name, outwear_category_name = get_random_image_with_info(outwear_path)
    if outwear_img_pil:
        plt.subplot(2, 3, 1) # 個別的圖底
        plt.imshow(outwear_img_pil)
        plt.title(f"外套 : {outwear_category_name}")
        plt.axis('off')   
        
# 上身圖片
top_path = os.path.join(clothes_db_path, "tops_", top_category)
top_img_pil, top_img_name, top_category_name = get_random_image_with_info(top_path)
if top_img_pil:
    plt.subplot(2, 3, 2) 
    plt.imshow(top_img_pil)
    plt.title(f"上衣 : {top_category_name}")
    plt.axis('off') 

# 下身圖片
if bottom_category: 
    bottom_path = os.path.join(clothes_db_path, "bottoms_", bottom_category)
    bottom_img_pil, bottom_img_name, bottom_category_name = get_random_image_with_info(bottom_path)
    if bottom_img_pil:
        plt.subplot(2, 3, 3) 
        plt.imshow(bottom_img_pil)
        plt.title(f"下身 : {bottom_category_name}")
        plt.axis('off')

# 雨具圖片
for i, rain_cat in enumerate(rain_categories):
    rain_path = os.path.join(clothes_db_path, "rain_", rain_cat)
    rain_img_pil, rain_img_name, rain_category_name = get_random_image_with_info(rain_path)
    if rain_img_pil:
        plt.subplot(2, 3, 4 + i) 
        plt.imshow(rain_img_pil)
        plt.title(f"雨天配件 : {rain_category_name}")
        plt.axis('off')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑體
plt.rcParams['axes.unicode_minus'] = False   # 解決負號顯示為方塊的問題

plt.tight_layout(rect=[0, 0, 1, 0.9]) # 調整整體佈局,為頂部的文字留出空間
plt.show()
