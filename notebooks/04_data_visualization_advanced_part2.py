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

@lru_cache(maxsize=1)
def load_data():
    df = pd.read_csv('../data/processed/final_indepth_sentiment_analysis_w_processed_category.csv')
    df['review_date'] = pd.to_datetime(df['review_date'])
    return df

def create_rating_sentiment_distribution_plot(df):
    """Grouped bar chart of sentiment distribution by rating"""
    ratings = sorted(df['overall'].unique())
    sentiments = ['positive', 'neutral', 'negative']
    colors = {'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}
    
    data = []
    for sentiment in sentiments:
        counts = [len(df[(df['overall'] == rating) & (df['sentiment'] == sentiment)]) for rating in ratings]
        data.append(
            go.Bar(
                name=sentiment,
                x=ratings,
                y=counts,
                marker_color=colors[sentiment]
            )
        )
    
    fig = go.Figure(data=data)
    
    fig.update_layout(
        title='Sentiment Distribution by Rating for Electronic Products',
        xaxis_title='Rating Score',
        yaxis_title='Number of Reviews',
        barmode='group',
        showlegend=True
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_category_distribution_plot(df):
    """Distribution of reviews across categories"""
    category_counts = df['overall_category'].value_counts().head(10)  # Top 10 categories
    
    fig = go.Figure(data=[
        go.Bar(
            x=category_counts.values,
            y=category_counts.index,
            orientation='h',
            marker_color='#3498db'
        )
    ])
    
    fig.update_layout(
        title='Top 10 Product Categories by Review Count',
        xaxis_title='Number of Reviews',
        yaxis_title='Category',
        height=400,
        showlegend=False
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_enhanced_category_distribution_plot(df):
    top_categories = df['overall_category'].value_counts().head(10).index
    filtered_df = df[df['overall_category'].isin(top_categories)]
    
    sentiment_by_category = pd.crosstab(
        filtered_df['overall_category'], 
        filtered_df['sentiment'], 
        normalize='index'
    ) * 100
    
    total_counts = filtered_df['overall_category'].value_counts()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=total_counts.values,
        y=total_counts.index,
        orientation='h',
        name='Total Reviews',
        marker_color='#3498db',
        text=total_counts.values,
        textposition='auto',
        hovertemplate="n=%{x}<br>" +
                      "positive=%{customdata[0]:.1f}%<br>" +
                      "neutral=%{customdata[1]:.1f}%<br>" +
                      "negative=%{customdata[2]:.1f}%<extra></extra>",
        customdata=[[
            sentiment_by_category.loc[cat, 'positive'],
            sentiment_by_category.loc[cat, 'neutral'],
            sentiment_by_category.loc[cat, 'negative']
        ] for cat in total_counts.index]
    ))
    
    fig.update_layout(
        title='Top 10 Product Categories: Review Count and Sentiment Distribution',
        xaxis_title='Number of Reviews',
        yaxis_title='Category',
        height=500,
        showlegend=False
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_overall_sentiment_plot(df, overall_category=None):
    # Filter data
    filtered_df = df.copy()
    if overall_category and overall_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['overall_category'] == overall_category]
    
    # Get sentiment counts
    sentiment_counts = filtered_df['sentiment'].value_counts()
    total_reviews = len(filtered_df)
    
    # Print debug information
    print(f"\nCategory: {overall_category}")
    print(f"Total reviews: {total_reviews}")
    print("Sentiment counts:", sentiment_counts.to_dict())
    
    # Create pie chart
    fig = go.Figure(data=[go.Pie(
        labels=sentiment_counts.index,
        values=sentiment_counts.values,
        marker=dict(colors=[
            '#3498db',  # positive
            '#9b59b6',  # neutral
            '#1abc9c'   # negative
        ]),
        textinfo='value+percent',
        hovertemplate="<b>%{label}</b><br>" +
                      "Count: %{value}<br>" +
                      "Percentage: %{percent}<br>" +
                      "<extra></extra>"
    )])
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f'Overall Sentiment Distribution {f"- {overall_category}" if overall_category and overall_category not in ["All Categories", "all"] else ""}<br>Total Reviews: {total_reviews}',
            y=0.95
        ),
        margin=dict(t=50, l=0, r=0, b=0),
        showlegend=True
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_rating_sentiment_plot(df, overall_category=None):
    filtered_df = df.copy()
    if overall_category and overall_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['overall_category'] == overall_category]
    
    rating_sentiment = pd.crosstab(filtered_df['overall'], filtered_df['sentiment'], normalize='index') * 100
    
    fig = go.Figure()
    for sentiment in ['positive', 'neutral', 'negative']:
        if sentiment in rating_sentiment.columns:
            fig.add_trace(go.Bar(
                name=sentiment,
                x=rating_sentiment.index,
                y=rating_sentiment[sentiment],
                marker_color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment]
            ))
    
    title = f'Sentiment Distribution by Rating - {overall_category}' if overall_category and overall_category not in ['All Categories', 'all'] else 'Sentiment Distribution by Rating'
    
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title='Rating',
        yaxis_title='Percentage',
        showlegend=True
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def dashboard():
    df = load_data()
    
    categories = sorted(df['overall_category'].unique())
    categories = ['All Categories'] + [cat for cat in categories if cat != 'All Electronics']
    
    # Create plots
    overall_sentiment = create_overall_sentiment_plot(df)
    rating_sentiment_dist = create_rating_sentiment_distribution_plot(df)
    category_distribution = create_enhanced_category_distribution_plot(df)
    rating_sentiment = create_rating_sentiment_plot(df)
    brand_sentiment = create_brand_sentiment_ratio_plot(df)
    
    return render_template(
        'index.html',
        overall_sentiment=overall_sentiment,
        rating_distribution=rating_sentiment_dist,
        category_distribution=category_distribution,
        brand_distribution=brand_sentiment,
        category_sentiment=overall_sentiment,
        rating_sentiment=rating_sentiment,
        main_categories=categories
    )

@app.route('/update_plots/<overall_category>')
def update_plots(overall_category):
    df = load_data()
    
    return jsonify({
        'overall_plot': create_overall_sentiment_plot(df, overall_category),
        'rating_plot': create_rating_sentiment_plot(df, overall_category)
    })

if __name__ == '__main__':
    app.run(debug=True)
