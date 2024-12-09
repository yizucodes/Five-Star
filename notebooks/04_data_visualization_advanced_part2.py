from flask import Flask, render_template, jsonify
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils
import pandas as pd
import json
import os
from pathlib import Path
from functools import lru_cache

# Setup template directory
template_dir = os.path.abspath('../templates')
app = Flask(__name__, template_folder=template_dir)

# Cache the loaded data
@lru_cache(maxsize=1)
def load_data():
    df = pd.read_csv('../data/processed/final_indepth_sentiment_analysis.csv')
    df['review_date'] = pd.to_datetime(df['review_date'])
    return df

def create_overall_sentiment_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['main_category'] == main_category]
        
    sentiment_counts = filtered_df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title=f'Overall Sentiment Distribution {f"- {main_category}" if main_category and main_category not in ["All Categories", "all"] else ""}',
        color_discrete_map={
            'positive': '#3498db',
            'neutral': '#9b59b6',
            'negative': '#1abc9c'
        }
    )
    # Optimize layout updates
    fig.update_layout(
        showlegend=True,
        margin=dict(t=50, l=0, r=0, b=0)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_rating_sentiment_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['main_category'] == main_category]
        
    rating_sentiment = pd.crosstab(filtered_df['overall'], filtered_df['sentiment'], normalize='index') * 100
    
    fig = go.Figure()
    for sentiment in ['positive', 'neutral', 'negative']:
        fig.add_trace(go.Bar(
            name=sentiment,
            x=rating_sentiment.index,
            y=rating_sentiment[sentiment],
            marker_color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment]
        ))
    
    title = 'Sentiment Distribution by Rating'
    if main_category and main_category not in ['All Categories', 'all']:
        title += f' - {main_category}'
        
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title='Rating',
        yaxis_title='Percentage',
        margin=dict(t=50, l=50, r=0, b=50)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_time_series_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['main_category'] == main_category]
        
    # Optimize groupby operation
    monthly_sentiment = filtered_df.groupby([pd.Grouper(key='review_date', freq='M'), 'sentiment']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    for sentiment in ['positive', 'neutral', 'negative']:
        if sentiment in monthly_sentiment.columns:
            fig.add_trace(go.Scatter(
                x=monthly_sentiment.index,
                y=monthly_sentiment[sentiment],
                name=sentiment,
                mode='lines',  # Removed markers for better performance
                line=dict(color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment])
            ))
    
    title = 'Sentiment Trends Over Time'
    if main_category and main_category not in ['All Categories', 'all']:
        title += f' - {main_category}'
        
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Number of Reviews',
        margin=dict(t=50, l=50, r=0, b=50)
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def dashboard():
    df = load_data()
    categories = ['All Categories'] + sorted([cat for cat in df['main_category'].unique() if cat != 'All Electronics'])
    
    return render_template(
        'index.html',
        overall_plot=create_overall_sentiment_plot(df),
        rating_plot=create_rating_sentiment_plot(df),
        time_series_plot=create_time_series_plot(df),
        main_categories=categories
    )

@app.route('/update_plots/<main_category>')
def update_plots(main_category):
    df = load_data()
    return jsonify({
        'overall_plot': create_overall_sentiment_plot(df, main_category),
        'rating_plot': create_rating_sentiment_plot(df, main_category),
        'time_series_plot': create_time_series_plot(df, main_category)
    })

if __name__ == '__main__':
    app.run(debug=True)