import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools import DuckDuckGoSearchRun


# ---------- Page Header ----------
st.markdown("""
# 🎉 Event Planner Agent
Plan your event end-to-end with AI assistance
""")
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 70px;
    font-size: 24px;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------- Sidebar Inputs ----------
st.sidebar.header("Event Details")

event_type = st.sidebar.text_input("Event Type", "Wedding")
event_date = st.sidebar.date_input("Event Date")
budget = st.sidebar.number_input(
    "Budget (₹)",
    min_value=500,
    value=50000,
    step=500
)
guest_count = st.sidebar.number_input(
    "Guest Count",
    min_value=1,
    value=100,
    step=10
)
location = st.sidebar.selectbox(
    "Location",
    ["Select City", "Bangalore", "Mumbai", "Delhi", "Hyderabad", "Chennai", "Other"]
)

if location == "Other":
    location = st.sidebar.text_input("Enter Your City")

# ---------- Metrics ----------
col1, col2, col3 = st.columns(3)
col1.metric("Event Type", event_type)
col2.metric("Guests", guest_count)
col3.metric("Budget", f"₹{budget}")

# ---------- Countdown ----------
today = datetime.today().date()
days_left = (event_date - today).days
st.info(f"⏳ {days_left} days left until your event!")


# ---------- Initialize LLM ----------
llm = ChatGroq(
    temperature=0.3,
    model_name="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------- Web Search ----------
search = DuckDuckGoSearchRun()


# ---------- Budget Calculator ----------
def calculate_budget(total_budget):
    allocation = {
        "Venue": total_budget * 0.35,
        "Catering": total_budget * 0.30,
        "Decoration": total_budget * 0.10,
        "Entertainment": total_budget * 0.10,
        "Photography": total_budget * 0.10,
        "Misc": total_budget * 0.05
    }
    return allocation


# ---------- Timeline Generator ----------
timeline_prompt = PromptTemplate(
    input_variables=["event_type", "event_date"],
    template="""
Create a detailed timeline checklist for {event_type} event 
scheduled on {event_date}.

Include:
- 1 month before
- 2 weeks before
- 1 week before
- 1 day before
- Event day

Return as bullet points.
"""
)

timeline_chain = timeline_prompt | llm | StrOutputParser()


# ---------- AI Suggestions ----------
suggestion_prompt = PromptTemplate(
    input_variables=["event_type", "guest_count"],
    template="""
Suggest creative ideas for a {event_type} event 
with {guest_count} guests.

Include:
- Theme ideas
- Entertainment ideas
- Decoration ideas
"""
)

suggestion_chain = suggestion_prompt | llm | StrOutputParser()


# ---------- Vendor Search ----------
def search_vendors(event_type, location):
    query = f"Best {event_type} venues and catering services in {location}"
    result = search.run(query)
    return result


# ---------- Reminder Generator ----------
def generate_reminders(event_date):
    reminders = [
        ("Book Venue", event_date - timedelta(days=30)),
        ("Confirm Catering", event_date - timedelta(days=14)),
        ("Send Invitations", event_date - timedelta(days=7)),
        ("Final Check", event_date - timedelta(days=1))
    ]
    return reminders

#-----------show theme images----------

def show_theme_images(event_type):

    st.header("🎨 Celebration Theme Ideas")

    image_urls = []

    if event_type.lower() == "wedding":
        image_urls = [
            ("https://images.unsplash.com/photo-1519741497674-611481863552", "Royal Wedding"),
            ("https://images.unsplash.com/photo-1522673607200-164d1b6ce486", "Beach Wedding"),
            ("https://images.unsplash.com/photo-1507502707541-f369a3b18502", "Garden Wedding"),
            ("https://images.unsplash.com/photo-1606800052052-a08af7148866", "Traditional Wedding"),
            ("https://images.unsplash.com/photo-1591604466107-ec97de577aff", "Luxury Wedding")
        ]

    elif event_type.lower() == "birthday":
        image_urls = [
            ("https://images.unsplash.com/photo-1464349153735-7db50ed83c84", "Kids Birthday"),
            ("https://images.unsplash.com/photo-1530103862676-de8c9debad1d", "Luxury Birthday"),
            ("https://images.unsplash.com/photo-1555244162-803834f70033", "Outdoor Birthday"),
            ("https://images.unsplash.com/photo-1527529482837-4698179dc6ce", "Balloon Theme"),
            ("https://images.unsplash.com/photo-1513151233558-d860c5398176", "Party Theme")
        ]

    else:
        image_urls = [
            ("https://images.unsplash.com/photo-1492684223066-81342ee5ff30", "Celebration"),
            ("https://images.unsplash.com/photo-1511795409834-ef04bbd61622", "Party"),
            ("https://images.unsplash.com/photo-1505236858219-8359eb29e329", "Festival"),
            ("https://images.unsplash.com/photo-1519671482749-fd09be7ccebf", "Decoration"),
            ("https://images.unsplash.com/photo-1469371670807-013ccf25f16a", "Event")
        ]

    cols = st.columns(len(image_urls))

    for col, (url, caption) in zip(cols, image_urls):
        col.image(url, caption=caption)

# ---------- Smart Task Generator ----------
def generate_tasks(event_type):

    common_tasks = [
        "Book Venue",
        "Confirm Catering",
        "Send Invitations",
        "Finalize Decoration",
        "Arrange Entertainment"
    ]

    if event_type.lower() == "wedding":
        extra_tasks = [
            "Book Photographer",
            "Arrange Makeup Artist",
            "Plan Mehendi",
            "Wedding Dress Selection",
            "Guest Accommodation"
        ]

    elif event_type.lower() == "birthday":
        extra_tasks = [
            "Order Cake",
            "Plan Party Games",
            "Buy Decorations",
            "Arrange Return Gifts",
            "Music Playlist"
        ]

    else:
        extra_tasks = [
            "Prepare Guest List",
            "Book Photographer",
            "Plan Activities"
        ]

    return common_tasks + extra_tasks

# ---------- Hero Button ----------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    plan = st.button("🚀 Plan My Event")

if plan:

    # ---------- Budget ----------
    st.header("📊 Budget Allocation")

    allocation = calculate_budget(budget)

    df = pd.DataFrame({
        "Category": list(allocation.keys()),
        "Amount": list(allocation.values())
    })

    fig = px.pie(
        df,
        names="Category",
        values="Amount",
        title="Budget Breakdown"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ---------- AI Ideas ----------
    st.header("🧠 AI Event Ideas")

    ideas = suggestion_chain.invoke({
    "event_type": event_type,
    "guest_count": guest_count
    })

    st.write(ideas)

    st.divider()

    # ---------- Theme Images ----------
    show_theme_images(event_type)

    st.divider()

    # ---------- Timeline ----------
    st.header("📅 Timeline & Checklist")

    timeline = timeline_chain.invoke({
        "event_type": event_type,
        "event_date": event_date
    })

    st.write(timeline)

    st.divider()

    # ---------- Vendors ----------
    st.header("🔍 Venue & Vendor Suggestions")

    vendors = search_vendors(event_type, location)
    st.write(vendors)

    st.divider()

    st.divider()

    # ---------- Smart Task Checklist ----------
    st.header("📋 Smart Task Checklist")

    tasks = generate_tasks(event_type)

    if "task_status" not in st.session_state:
        st.session_state.task_status = {task: False for task in tasks}

    completed = 0

    for task in tasks:
        st.session_state.task_status[task] = st.checkbox(
            task,
            value=st.session_state.task_status.get(task, False)
        )

        if st.session_state.task_status[task]:
            completed += 1

    # ---------- Progress Bar ----------
    progress = completed / len(tasks)

    st.progress(progress)

    st.write(f"✅ {completed} of {len(tasks)} tasks completed")

    st.divider()

    # ---------- Reminders ----------
    st.header("⏰ Task Reminders")

    reminders = generate_reminders(event_date)

    for task, date in reminders:
        st.write(f"📌 {task} → {date}")
        