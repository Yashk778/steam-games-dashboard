import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Steam Games Dashboard", layout="wide")

df = pd.read_csv('steam_games_cleaned.csv')

# Sidebar Navigation
st.sidebar.title("🎮 Steam Dashboard")

page = st.sidebar.radio("Navigate", [
    "🏠 Overview",
    "🎯 Genres & Sentiment",
    "📅 Release Trends",
    "👨‍💻 Developers & Publishers",
    "💰 Pricing",
    "🔥 Popularity"
])

# Year Filter
st.sidebar.markdown("---")
years = sorted(df['release_year'].unique())
selected_years = st.sidebar.slider("Release Year Range",
                                    min_value=int(min(years)),
                                    max_value=int(max(years)),
                                    value=(1998, 2024))

df = df[(df['release_year'] >= selected_years[0]) & 
        (df['release_year'] <= selected_years[1])]

# ─── PAGES ───────────────────────────────────────────

if page == "🏠 Overview":
    st.title("🎮 Steam Games Dashboard")
    st.markdown("Exploring trends and insights from around 2000 Steam games")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Games", len(df))
    col2.metric("Avg Price", f"₹{df['price'].mean():.0f}")
    col3.metric("Avg Review Score", f"{df['review_score'].mean():.1f}%")
    col4.metric("Most Common Genre",
                df['genres'].str.split(',').explode().str.strip().value_counts().index[0])

    st.markdown("---")
    st.markdown("### 👈 Use the sidebar to explore different sections")

elif page == "🎯 Genres & Sentiment":
    st.title("🎯 Genres & Sentiment")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        genre_exploded = df['genres'].str.split(',').explode().str.strip()
        genre_counts = genre_exploded.value_counts().reset_index()
        genre_counts.columns = ['genre', 'count']
        fig1 = px.bar(genre_counts, x='genre', y='count',
                      title='Most Common Genres on Steam',
                      color='count', color_continuous_scale='viridis')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        sentiment_counts = df['review_sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['sentiment', 'count']
        fig2 = px.pie(sentiment_counts, values='count', names='sentiment',
                      title='Games by Review Sentiment')
        st.plotly_chart(fig2, use_container_width=True)

elif page == "📅 Release Trends":
    st.title("📅 Release Trends")
    st.markdown("---")

    year_counts = df['release_year'].value_counts().sort_index().reset_index()
    year_counts.columns = ['year', 'count']
    fig3 = px.line(year_counts, x='year', y='count',
                   title='Number of Games Released Per Year',
                   markers=True)
    st.plotly_chart(fig3, use_container_width=True)

    month_counts = df['release_month'].value_counts().sort_index().reset_index()
    month_counts.columns = ['month', 'count']
    month_counts['month'] = ['Jan','Feb','Mar','Apr','May','Jun',
                              'Jul','Aug','Sep','Oct','Nov','Dec']
    fig5 = px.bar(month_counts, x='month', y='count',
                  title='Number of Games Released Per Month',
                  color='count', color_continuous_scale='teal')
    st.plotly_chart(fig5, use_container_width=True)

elif page == "👨‍💻 Developers & Publishers":
    st.title("👨‍💻 Developers & Publishers")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        top_devs = df[df['developer'] != 'Other']['developer'].value_counts().head(10).reset_index()
        top_devs.columns = ['developer', 'count']
        fig4 = px.bar(top_devs, x='count', y='developer',
                      orientation='h',
                      title='Top 10 Developers by Number of Games',
                      color='count', color_continuous_scale='blues')
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        top_pubs = df[df['publisher'] != 'Other']['publisher'].value_counts().head(10).reset_index()
        top_pubs.columns = ['publisher', 'count']
        fig6 = px.bar(top_pubs, x='count', y='publisher',
                      orientation='h',
                      title='Top 10 Publishers by Number of Games',
                      color='count', color_continuous_scale='reds')
        st.plotly_chart(fig6, use_container_width=True)

elif page == "💰 Pricing":
    st.title("💰 Pricing Insights")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        fig7 = px.histogram(df[df['price'] > 0], x='price', nbins=50,
                            title='Paid Games Price Distribution')
        st.plotly_chart(fig7, use_container_width=True)

    with col2:
        free_paid = df['price'].apply(lambda x: 'Free' if x == 0 else 'Paid').value_counts().reset_index()
        free_paid.columns = ['type', 'count']
        fig8 = px.pie(free_paid, values='count', names='type',
                      title='Free vs Paid Games')
        st.plotly_chart(fig8, use_container_width=True)

elif page == "🔥 Popularity":
    st.title("🔥 Popularity Insights")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        fig9 = px.histogram(df, x='review_score', nbins=30,
                            title='Review Score Distribution')
        st.plotly_chart(fig9, use_container_width=True)

    with col2:
        fig10 = px.scatter(df, x='price', y=np.log1p(df['review_count']),
                           color='review_score',
                           title='Price vs Popularity (colored by Review Score)',
                           color_continuous_scale='viridis')
        st.plotly_chart(fig10, use_container_width=True)