import streamlit as st
import pandas as pd
import altair as alt
from db import create_table, insert_incident, fetch_incidents
from ai import analyze_sentiment

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="FairExam", layout="wide")

# ---------------------------
# EXAMS LIST
# ---------------------------
EXAMS = [
    "NEET", "JEE Main", "JEE Advanced", "CUET",
    "CBSE Board", "ICSE Board", "SSC CGL", "SSC CHSL",
    "UPSC", "GATE", "CAT", "CLAT",
    "Railway (RRB)", "State PSC", "Other"
]

# ---------------------------
# UI STYLE
# ---------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
    color: white;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# INIT
# ---------------------------
create_table()

# ---------------------------
# HERO
# ---------------------------
st.markdown("""
# 🎓 FairExam  
### India's Education Transparency Platform  
""")

st.markdown("---")

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("🔍 Filter Data")

selected_exam = st.sidebar.selectbox(
    "Select Exam",
    ["All"] + EXAMS
)

# ---------------------------
# FORM
# ---------------------------
st.header("📢 Report an Exam Issue")

with st.form("incident_form"):
    exam = st.selectbox("Exam", EXAMS)

    if exam == "Other":
        exam = st.text_input("Enter Exam Name")

    issue_type = st.selectbox(
        "Issue Type",
        [
            "Paper Leak", "Result Error", "Server Issue",
            "Admit Card Issue", "Exam Center Problem",
            "Wrong Question Paper", "Delay in Result",
            "Technical Glitch", "Other"
        ]
    )

    state = st.text_input("State")
    description = st.text_area("Describe the issue")

    submitted = st.form_submit_button("Submit")

    if submitted:
        try:
            sentiment = analyze_sentiment(description)
        except:
            sentiment = "UNKNOWN"

        insert_incident(
            exam,
            issue_type,
            state,
            description,
            sentiment
        )

        st.success("✅ Issue reported successfully!")

st.markdown("---")

# ---------------------------
# DASHBOARD
# ---------------------------
st.header("📊 Transparency Dashboard")

data = fetch_incidents()

if data:
    df = pd.DataFrame(data, columns=[
        "ID", "Exam", "Issue Type", "State",
        "Description", "Sentiment", "Timestamp"
    ])

    if selected_exam != "All":
        df = df[df["Exam"] == selected_exam]

    # METRICS
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Issues", len(df))
    col2.metric("Most Affected Exam", df["Exam"].mode()[0])
    col3.metric("Most Common Issue", df["Issue Type"].mode()[0])

    st.markdown("---")

    # CHART
    st.subheader("📈 Issues by Exam")

    chart_data = df["Exam"].value_counts().reset_index()
    chart_data.columns = ["Exam", "Count"]

    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Exam',
        y='Count',
        tooltip=['Exam', 'Count']
    )

    st.altair_chart(chart, use_container_width=True)

    # ALERT SYSTEM
    st.subheader("🚨 Alert Mode")

    issue_counts = df["Issue Type"].value_counts()

    for issue, count in issue_counts.items():
        if count >= 2:
            st.warning(f"⚠️ High reports of {issue}: {count} cases")

    # TRUST SCORE
    st.subheader("📉 Exam Trust Score")

    total = len(df)
    exam_counts = df["Exam"].value_counts()

    for exam_name, count in exam_counts.items():
        score = max(0, 100 - (count / total) * 100)
        st.write(f"{exam_name}: {score:.1f}% trust")

    # LIVE FEED
    st.subheader("📢 Live Incident Feed")

    for _, row in df.head(5).iterrows():
        st.markdown(f"""
        <div style="
            font-size:15px;
            line-height:1.5;
            margin-bottom:15px;
            padding:12px;
            border-radius:10px;
            background-color:#1c1f26;
        ">
            <b>{row['Exam']}</b> | {row['Issue Type']} <br>
            📍 {row['State']} <br>
            📝 {row['Description']} <br>
            ⚡ <b>Sentiment:</b> {row['Sentiment']}
        </div>
        """, unsafe_allow_html=True)

    # TABLE
    st.subheader("📄 All Reports")
    st.dataframe(df)

else:
    st.info("No incidents reported yet.")