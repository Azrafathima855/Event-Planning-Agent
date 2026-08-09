# 🎉 Event Planner Agent

An AI-powered Event Planner Agent built with Streamlit that helps users plan and organize events based on their event type, date, budget, guest count, and location.

## ✨ Features

- 🎉 Event type, date, budget, guest count and location selection
- ⏳ Event countdown
- 📊 Automatic budget allocation with interactive pie chart
- 🧠 AI-generated event ideas
- 🎨 Event theme suggestions with images
- 📅 AI-generated event timeline and checklist
- 🔍 Venue and vendor suggestions using web search
- 📋 Smart task checklist
- 📈 Task completion progress tracking
- ⏰ Task reminders based on the event date
- 💡 Different task suggestions for weddings, birthdays and other events

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- LangChain
- Groq / Llama 3.1
- DuckDuckGo Search
- Python-dotenv

## 🤖 AI Components

The project uses LangChain with Groq's Llama 3.1 model to generate:

- Event ideas
- Event timelines
- Planning suggestions

DuckDuckGo Search is used to provide venue and vendor suggestions based on the selected event type and location.

## 💰 Budget Planning

The application automatically divides the user's budget into different categories:

- Venue
- Catering
- Decoration
- Entertainment
- Photography
- Miscellaneous

The allocation is displayed using an interactive pie chart.

## 📋 Smart Task Management

The application generates tasks according to the event type.

For example, wedding planning can include:

- Book Photographer
- Arrange Makeup Artist
- Plan Mehendi
- Wedding Dress Selection
- Guest Accommodation

Users can mark tasks as completed and track their progress.

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK