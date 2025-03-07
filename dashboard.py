# Mengambil dataset
file_1_path = 'data/data_1.csv'
file_2_path = 'data/data_2.csv'

# Mengkonversi menjadi dataframe
df_day = pd.read_csv(file_1_path)
df_hour = pd.read_csv(file_2_path)

#Mengetahui info dataframe
print(df_hour.info())
print(df_day.info())

# Mengecek apakah terdapat missing value
df_hour.isnull().sum()
df_day.isnull().sum()

#Mengecek apakah terdapat duplikat data
df_hour.duplicated().sum()
df_day.duplicated().sum()

#Mengkonversi kolom dteday menjadi kolom datetime berdasarkan lib pandas
df_hour["dteday"] = pd.to_datetime(df_hour["dteday"])
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

#Mengkonversi kolom nilai season menjadi istilah season
df_hour["season"] = df_hour["season"].replace({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
df_day["season"] = df_day["season"].replace({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

#Mengkonversi kolom nilai workingday menjadi istilah workingday
df_hour["workingday"] = df_hour["workingday"].replace({0: "Not Workday", 1: "Workday"})
df_day["workingday"] = df_day["workingday"].replace({0: "Not Workday", 1: "Workday"})

#Mengkonversi kolom nilai holiday menjadi istilah holiday
df_hour["holiday"] = df_hour["holiday"].replace({0: "Not holiday", 1: "holiday"})
df_day["holiday"] = df_day["holiday"].replace({0: "Not holiday", 1: "holiday"})

#Menghilangkan kolom instant, hum, dan winspeed
df_hour = df_hour.drop(['instant', 'hum', 'windspeed'], axis=1)
df_day = df_day.drop(['instant', 'hum', 'windspeed'], axis=1)

#Menambahkan kolom baru yang mengkonversi nilai temp dan atemp
df_hour['temp.cvt'] = df_hour['temp']*41
df_hour['atemp.cvt'] = df_hour['atemp']*50

df_day['temp.cvt'] = df_day['temp']*41
df_day['atemp.cvt'] = df_day['atemp']*50

# Bagaimana rata-rata dan median suhu harian pada masing-masing musim dalam 2 tahun terakhir?
season_temp_stats = df_day.groupby("season")["temp.cvt"].agg(["mean", "median", "min", "max"])

# Bagaimana data historis temp dan atemp dalam dua tahun terakhir
def plot_temp_trend_by_month():
    df_day["month"] = df_day["dteday"].dt.to_period("M")
    monthly_avg_temp = df_day.groupby("month").agg({"temp.cvt": "mean", "atemp.cvt": "mean"})
    
    plt.figure(figsize=(10,6))
    plt.plot(monthly_avg_temp.index.astype(str), monthly_avg_temp["temp.cvt"], marker='o', linestyle='-', label="Temperature in Celcius")
    plt.plot(monthly_avg_temp.index.astype(str), monthly_avg_temp["atemp.cvt"], marker='s', linestyle='-', label="Feeling Temperature in celcius", color='red')
    
    plt.title("Monthly Average Temperature and Atemp Trend")
    plt.xlabel("Month")
    plt.ylabel("Temperature")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

#Bagaimana data historis jumlah penyewa dalam dua tahun terakhir
def plot_rentals_trend_by_month():
    df_day["month"] = df_day["dteday"].dt.to_period("M")
    monthly_rentals = df_day.groupby("month")["cnt"].sum()
    
    plt.figure(figsize=(10,6))
    plt.plot(monthly_rentals.index.astype(str), monthly_rentals, marker='o', linestyle='-', label="Total Rentals", color='blue')
    
    plt.title("Monthly Total Rentals Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Rentals")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

# Berapa banyak jumlah penyewa harian berdasarkan musim?
season_rentals = df_day.groupby("season")["cnt"].sum()

# Berapa banyak jumlah penyewa harian berdasarkan casual atau registered?
casual_registered_rentals = df_day[["casual", "registered"]].sum()

# Berapa banyak jumlah penyewa harian berdasarkan hari kerja atau tidak?
workday_rentals = df_day.groupby("workingday")["cnt"].sum()

# Berapa banyak jumlah penyewa harian saat libur nasional dibanding tidak?
holiday_rentals = df_day.groupby("holiday")["cnt"].sum()

# Berapa banyak jumlah penyewa pada setiap jam dalam satu hari?
hourly_rentals = df_hour.groupby("hr")["cnt"].sum()

# Menampilkan hasil
plot_temp_trend_by_month()
plot_rentals_trend_by_month()
results = {
    "Season Temperature Stats": season_temp_stats,
    "Rentals by Season": season_rentals,
    "Casual vs Registered Rentals": casual_registered_rentals,
    "Rentals by Hour": hourly_rentals,
    "Rentals by Workday": workday_rentals,
    "Rentals by Holiday": holiday_rentals,
}

# Menampilkan hasil dengan loop
for key, value in results.items():
    print(f"\n{key}:\n{value}\n")

def plot_season_temp():
    temp_stats = df_day.groupby("season")["temp"].agg(["mean", "median", "min", "max"])
    fig, ax = plt.subplots(figsize=(8,5))
    temp_stats.plot(kind='bar', ax=ax)
    ax.set_title("Temperature Statistics by Season")
    ax.set_xlabel("Season")
    ax.set_ylabel("Temperature")
    ax.legend(["Mean", "Median", "Min", "Max"])
    st.pyplot(fig)

def plot_temp_trend_by_month():
    df_day["month"] = df_day["dteday"].dt.to_period("M")
    monthly_avg_temp = df_day.groupby("month").agg({"temp": "mean", "atemp": "mean"})
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(monthly_avg_temp.index.astype(str), monthly_avg_temp["temp"], marker='o', linestyle='-', label="Temperature (C)")
    ax.plot(monthly_avg_temp.index.astype(str), monthly_avg_temp["atemp"], marker='s', linestyle='-', label="Feeling Temperature (C)", color='red')
    
    ax.set_title("Monthly Average Temperature and Atemp Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature")
    ax.set_xticklabels(monthly_avg_temp.index.astype(str), rotation=45)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def plot_rentals_trend_by_month():
    df_day["month"] = df_day["dteday"].dt.to_period("M")
    monthly_rentals = df_day.groupby("month")["cnt"].sum()
    
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(monthly_rentals.index.astype(str), monthly_rentals, marker='o', linestyle='-', label="Total Rentals", color='blue')
    
    ax.set_title("Monthly Total Rentals Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Rentals")
    ax.set_xticklabels(monthly_rentals.index.astype(str), rotation=45)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

def plot_rentals_by_category():
    casual_registered = df_day[["casual", "registered"]].sum()
    fig, ax = plt.subplots(figsize=(6,6))
    ax.pie(casual_registered, labels=["Casual", "Registered"], autopct='%1.1f%%', colors=['blue', 'green'])
    ax.set_title("Total Rentals: Casual vs Registered Users")
    st.pyplot(fig)

def plot_rentals_by_workingday():
    workday_rentals = df_day.groupby("workingday")["cnt"].sum()
    fig, ax = plt.subplots(figsize=(8,5))
    workday_rentals.plot(kind='bar', color=['purple', 'red'], ax=ax)
    ax.set_title("Total Rentals: Working Day vs Holiday")
    ax.set_xlabel("Workday (0=Holiday, 1=Workday)")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

# Streamlit Dashboard
st.title("Bike Sharing Data Dashboard")

st.subheader("1. Temperature Statistics by Season")
plot_season_temp()
st.write("Key Insight: Temperature varies across seasons, affecting bike rental behavior.")

st.subheader("2. Monthly Temperature Trends")
plot_temp_trend_by_month()
st.write("Key Insight: Observing the trend of temperature and perceived temperature over time.")

st.subheader("3. Monthly Total Rentals Trend")
plot_rentals_trend_by_month()
st.write("Key Insight: Identifying peak and off-peak rental months.")

st.subheader("4. Casual vs Registered Rentals")
plot_rentals_by_category()
st.write("Key Insight: Understanding the proportion of casual versus registered users.")

st.subheader("5. Rentals by Working Day and Holiday")
plot_rentals_by_workingday()
st.write("Key Insight: How working days and holidays impact rentals.")