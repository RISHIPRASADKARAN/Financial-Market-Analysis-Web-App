import streamlit as st
import pandas as pd
import plotly.express as px
from financial_market_analysis import WebScraper, DataProcessor, PatternAnalyzer, Visualizer

# Initialize components
scraper = WebScraper()
processor = DataProcessor()
analyzer = PatternAnalyzer()
visualizer = Visualizer()

st.set_page_config(layout='wide', page_title='Financial Market Analysis')
st.title("📈 Financial Market Analysis Platform")

# Sidebar Menu
menu = st.sidebar.radio("Navigation", ["Home", "Stock Analysis", "News Sentiment", "Visualization"])

if menu == "Home":
    st.subheader("Welcome to Financial Market Analysis")
    st.write("This platform allows you to analyze stock trends, sentiment, and correlations interactively.")

elif menu == "Stock Analysis":
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE)")
    if st.button("Scrape Data"):
        with st.spinner("Fetching stock data..."):
            stock_data = scraper.scrape_historical_data(stock_symbol)
            if not stock_data.empty:
                st.success("Data Retrieved Successfully!")
                st.dataframe(stock_data.tail(10))
                
                # Trend Analysis
                trend_results = analyzer.identify_trends(stock_data, stock_symbol)
                trend_fig = visualizer.plot_stock_trends(trend_results['data'], title=f"{stock_symbol} Price Trend")
                st.pyplot(trend_fig)
            else:
                st.error("Failed to fetch data. Try a different symbol.")

elif menu == "News Sentiment":
    if st.button("Analyze Sentiment"):
        with st.spinner("Analyzing financial news..."):
            news_data = scraper.scrape_financial_news(10)
            sentiment_results = analyzer.analyze_sentiment(news_data)
            st.dataframe(sentiment_results['data'].head())
            
            # Word Cloud
            wordcloud_fig = visualizer.plot_sentiment_wordcloud(sentiment_results['data'])
            st.pyplot(wordcloud_fig)

elif menu == "Visualization":
    st.subheader("Data Visualization")
    if st.button("Show Correlation Heatmap"):
        stock_data = scraper.scrape_historical_data("RELIANCE")
        correlation_results = analyzer.analyze_correlations(stock_data)
        heatmap_fig = visualizer.plot_correlation_heatmap(correlation_results['correlation_matrix'])
        st.pyplot(heatmap_fig)

st.sidebar.markdown("---")
st.sidebar.text("Developed with ❤️ using Streamlit")
