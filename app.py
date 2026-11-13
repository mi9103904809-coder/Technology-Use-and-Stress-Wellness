
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Tech Use and Stress Wellness Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Tech Use and Stress Wellness Dashboard")

# Load dataset
df = pd.read_csv("cleaned_Tech_use_stress_wellness.csv")

# Sidebar filters
st.sidebar.title("Dashboard Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    df["gender"].dropna().unique(),
    default=list(df["gender"].dropna().unique())
)

location = st.sidebar.multiselect(
    "Select Location",
    df["location_type"].dropna().unique(),
    default=list(df["location_type"].dropna().unique())
)

age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["age"].min()),
    int(df["age"].max()),
    (int(df["age"].min()), int(df["age"].max()))
)

filtered_df = df[
    (df["gender"].isin(gender)) &
    (df["location_type"].isin(location)) &
    (df["age"].between(age_range[0], age_range[1]))
].copy()

st.subheader("Data Preview")
st.dataframe(filtered_df.head(5), use_container_width=True)

st.write("Total Users:", len(filtered_df))

# Four dashboards
dashboard = st.selectbox(
    "Select Dashboard",
    [
        "Technology Usage Overview",
        "Stress & Mental Wellness",
        "Lifestyle & Wellness Habits",
        "Demographics & Wellness Apps"
    ]
)

if filtered_df.empty:
    st.warning("No data available for selected filters.")

elif dashboard == "Technology Usage Overview":
    st.header("Technology Usage Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Users", len(filtered_df))
    c2.metric("Average Screen Time", round(filtered_df["daily_screen_time_hours"].mean(), 2))
    c3.metric("Median Screen Time", round(filtered_df["daily_screen_time_hours"].median(), 2))
    c4.metric("Average Social Media Hours", round(filtered_df["social_media_hours"].mean(), 2))

    st.plotly_chart(px.histogram(filtered_df, x="daily_screen_time_hours", title="Screen Time Distribution"), use_container_width=True)

    device_cols = ["phone_usage_hours", "laptop_usage_hours", "tablet_usage_hours", "tv_usage_hours"]
    device_data = filtered_df[device_cols].sum().reset_index()
    device_data.columns = ["Device", "Total Usage"]
    st.plotly_chart(px.bar(device_data, x="Device", y="Total Usage", title="Device-wise Usage"), use_container_width=True)

    st.plotly_chart(px.box(filtered_df, x="screen_time_group", y="daily_screen_time_hours", title="Screen Time Groups"), use_container_width=True)
    st.plotly_chart(px.bar(filtered_df.groupby("location_type").size().reset_index(name="Users"), x="location_type", y="Users", title="Users by Location"), use_container_width=True)
    st.plotly_chart(px.scatter(filtered_df, x="social_media_hours", y="daily_screen_time_hours", title="Screen Time vs Social Media"), use_container_width=True)

elif dashboard == "Stress & Mental Wellness":
    st.header("Stress & Mental Wellness")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average Stress", round(filtered_df["stress_level"].mean(), 2))
    c2.metric("Mental Health Score", round(filtered_df["mental_health_score"].mean(), 2))
    c3.metric("Weekly Anxiety Score", round(filtered_df["weekly_anxiety_score"].mean(), 2))
    c4.metric("Weekly Depression Score", round(filtered_df["weekly_depression_score"].mean(), 2))

    st.plotly_chart(px.histogram(filtered_df, x="stress_level", title="Stress Level Distribution"), use_container_width=True)
    st.plotly_chart(px.bar(filtered_df.groupby("screen_time_group", observed=False)["stress_level"].mean().reset_index(), x="screen_time_group", y="stress_level", title="Average Stress by Screen Time Group"), use_container_width=True)
    st.plotly_chart(px.scatter(filtered_df, x="weekly_anxiety_score", y="weekly_depression_score", title="Anxiety vs Depression"), use_container_width=True)

    corr = filtered_df.select_dtypes(include="number").corr()
    st.plotly_chart(px.imshow(corr, text_auto=True, title="Correlation Heatmap"), use_container_width=True)
    st.plotly_chart(px.box(filtered_df, x="gender", y="stress_level", title="Stress by Gender"), use_container_width=True)

elif dashboard == "Lifestyle & Wellness Habits":
    st.header("Lifestyle & Wellness Habits")
    healthy = filtered_df["eats_healthy"].astype(str).str.lower().isin(["true", "yes", "1"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Physical Activity Hours", round(filtered_df["physical_activity_hours_per_week"].mean(), 2))
    c2.metric("Mindfulness Minutes", round(filtered_df["mindfulness_minutes_per_day"].mean(), 2))
    c3.metric("Caffeine Intake", round(filtered_df["caffeine_intake_mg_per_day"].mean(), 2))
    c4.metric("Healthy Eating %", round(healthy.mean() * 100, 2))

    st.plotly_chart(px.scatter(filtered_df, x="physical_activity_hours_per_week", y="stress_level", title="Physical Activity vs Stress"), use_container_width=True)
    st.plotly_chart(px.histogram(filtered_df, x="mindfulness_minutes_per_day", color="gender", title="Mindfulness by Gender"), use_container_width=True)

    eating_data = pd.DataFrame({
        "Eating Habit": ["Healthy", "Unhealthy"],
        "Users": [healthy.sum(), (~healthy).sum()]
    })
    st.plotly_chart(px.pie(eating_data, names="Eating Habit", values="Users", hole=0.5, title="Healthy vs Unhealthy Eating"), use_container_width=True)
    st.plotly_chart(px.violin(filtered_df, x="screen_time_group", y="physical_activity_hours_per_week", title="Activity by Screen Time Group"), use_container_width=True)
    st.plotly_chart(px.histogram(filtered_df, x="caffeine_intake_mg_per_day", title="Caffeine Distribution"), use_container_width=True)

elif dashboard == "Demographics & Wellness Apps":
    st.header("Demographics & Wellness Apps")
    apps = filtered_df["uses_wellness_apps"].astype(str).str.lower().isin(["true", "yes", "1"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Users", len(filtered_df))
    c2.metric("Wellness App Adoption %", round(apps.mean() * 100, 2))
    c3.metric("Average Age", round(filtered_df["age"].mean(), 2))
    c4.metric("Average Stress", round(filtered_df["stress_level"].mean(), 2))

    st.plotly_chart(px.histogram(filtered_df, x="age_group", title="Users by Age Group"), use_container_width=True)

    app_data = pd.DataFrame({
        "App Usage": ["Uses Apps", "Does Not Use Apps"],
        "Users": [apps.sum(), (~apps).sum()]
    })
    st.plotly_chart(px.pie(app_data, names="App Usage", values="Users", hole=0.5, title="Wellness App Adoption"), use_container_width=True)
    st.plotly_chart(px.bar(filtered_df.groupby("gender")["mental_health_score"].mean().reset_index(), x="gender", y="mental_health_score", title="Mental Health by Gender"), use_container_width=True)
    st.plotly_chart(px.violin(filtered_df, x="location_type", y="stress_level", title="Stress by Location"), use_container_width=True)
    st.plotly_chart(px.histogram(filtered_df, x="mental_health_score", color="uses_wellness_apps", title="Mental Health Score by App Usage"), use_container_width=True)

st.caption("Tech Use and Stress Wellness Analytics Project")
