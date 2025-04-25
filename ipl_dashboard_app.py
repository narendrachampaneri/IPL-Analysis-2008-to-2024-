
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("IPL 2008–2024 Dashboard")

# Load data
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")

# Sidebar filters
st.sidebar.header("Filters")
season = st.sidebar.selectbox("Select Season", sorted(matches['season'].dropna().unique(), reverse=True))
team = st.sidebar.selectbox("Select Team", sorted(matches['team1'].dropna().unique()))

# Filter data
season_matches = matches[matches['season'] == season]
team_matches = season_matches[(season_matches['team1'] == team) | (season_matches['team2'] == team)]

# Display summary
st.subheader(f"Overview - {team} in {season}")
total_matches = len(team_matches)
wins = len(team_matches[team_matches['winner'] == team])
st.metric("Total Matches", total_matches)
st.metric("Wins", wins)

# Top Batsmen
st.subheader("Top 10 Run Scorers")
top_batsmen = deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x=top_batsmen.values, y=top_batsmen.index, ax=ax1)
st.pyplot(fig1)

# Top Bowlers
st.subheader("Top 10 Wicket Takers")
wickets = deliveries[deliveries['dismissal_kind'].notnull()]
top_bowlers = wickets['bowler'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, ax=ax2)
st.pyplot(fig2)

# Run Rate by Phase
st.subheader("Average Run Rate by Match Phase")
conditions = [
    (deliveries['over'] <= 6),
    (deliveries['over'] > 6) & (deliveries['over'] <= 15),
    (deliveries['over'] > 15)
]
choices = ['Powerplay', 'Middle Overs', 'Death Overs']
deliveries['phase'] = pd.Series(pd.cut(deliveries['over'], bins=[0,6,15,20], labels=choices))

phase_runrate = deliveries.groupby('phase')['total_runs'].mean()
fig3, ax3 = plt.subplots()
sns.barplot(x=phase_runrate.index, y=phase_runrate.values, ax=ax3)
st.pyplot(fig3)

st.caption("Dashboard by ChatGPT - IPL Dataset")
