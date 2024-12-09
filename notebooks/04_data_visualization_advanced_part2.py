from flask import Flask, render_template, jsonify
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.utils  # Add this line
import pandas as pd
import json
import os

import os
from pathlib import Path

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
print(f"Current file path: {current_file_path}")

# Get the project root directory (Five-Star_New/Five-Star)
project_root = Path(current_file_path).parents[2]
print(f"Project root: {project_root}")

# Set template directory to be project_root/templates
template_dir = os.path.join(project_root, 'templates')
print(f"Template directory: {template_dir}")

app = Flask(__name__, template_folder=template_dir)
# When initializing Flask, make sure this is correct

def load_data():
    # Replace with your data loading logic
    df = pd.read_csv('../data/processed/final_indepth_sentiment_analysis.csv')
    df['review_date'] = pd.to_datetime(df['review_date'])
    return df

def create_overall_sentiment_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category != 'all':
        filtered_df = filtered_df[filtered_df['main_category'] == main_category]
        
    sentiment_counts = filtered_df['sentiment'].value_counts()
    fig = px.pie(
        values=sentiment_counts.values,
        names=sentiment_counts.index,
        title=f'Overall Sentiment Distribution {f"- {main_category}" if main_category and main_category != "all" else ""}',
        color_discrete_map={
            'positive': '#3498db',
            'neutral': '#9b59b6',
            'negative': '#1abc9c'
        }
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_rating_sentiment_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category != 'all':
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
    if main_category and main_category != 'all':
        title += f' - {main_category}'
        
    fig.update_layout(
        barmode='stack',
        title=title,
        xaxis_title='Rating',
        yaxis_title='Percentage'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_time_series_plot(df, main_category=None):
    filtered_df = df.copy()
    if main_category and main_category != 'all':
        filtered_df = filtered_df[filtered_df['main_category'] == main_category]
        
    monthly_sentiment = filtered_df.groupby([filtered_df['review_date'].dt.to_period('M'), 'sentiment']).size().unstack()
    
    fig = go.Figure()
    for sentiment in ['positive', 'neutral', 'negative']:
        if sentiment in monthly_sentiment.columns:
            fig.add_trace(go.Scatter(
                x=monthly_sentiment.index.astype(str),
                y=monthly_sentiment[sentiment],
                name=sentiment,
                mode='lines+markers',
                line=dict(color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment])
            ))
    
    title = 'Sentiment Trends Over Time'
    if main_category and main_category != 'all':
        title += f' - {main_category}'
        
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Number of Reviews'
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def dashboard():
    df = load_data()
    
    # Get unique main categories
    main_categories = sorted(df['main_category'].unique())
    
    # Create initial plots
    overall_plot = create_overall_sentiment_plot(df)
    rating_plot = create_rating_sentiment_plot(df)
    time_series_plot = create_time_series_plot(df)
    
    return render_template(
        'index.html',
        overall_plot=overall_plot,
        rating_plot=rating_plot,
        time_series_plot=time_series_plot,
        main_categories=main_categories
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
    print(f"Current directory: {os.getcwd()}")
    print(f"Template directory: {template_dir}")
    print(f"Template exists: {os.path.exists(os.path.join(template_dir, 'index.html'))}")
    app.run(debug=True)