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
    # Debug prints
    print("\nUnique categories before filtering:")
    print(df['overall_category'].unique())
    
    # Filter out Uncategorized before getting counts
    df_filtered = df[df['overall_category'] != 'Uncategorized']
    
    # Debug prints
    print("\nUnique categories after filtering:")
    print(df_filtered['overall_category'].unique())
    
    category_counts = df_filtered['overall_category'].value_counts().head(10)
    
    # Debug prints
    print("\nTop 10 categories and their counts:")
    print(category_counts)
    
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
    # Filter out unwanted categories and get sentiment counts
    df_filtered = df[
        (df['overall_category'].notna()) & 
        (df['overall_category'] != 'Uncategorized') & 
        (df['overall_category'].str.strip() != '')
    ]
    
    category_sentiment = []
    for category in df_filtered['overall_category'].unique():
        category_data = df_filtered[df_filtered['overall_category'] == category]
        sentiment_counts = category_data['sentiment'].value_counts()
        total = len(category_data)
        
        positive_count = sentiment_counts.get('positive', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negative', 0)
        
        category_sentiment.append({
            'category': category,
            'positive': positive_count,
            'neutral': neutral_count,
            'negative': negative_count,
            'total': total,
            'positive_pct': (positive_count/total)*100,
            'neutral_pct': (neutral_count/total)*100,
            'negative_pct': (negative_count/total)*100
        })
    
    category_df = pd.DataFrame(category_sentiment)
    top_categories = category_df.nlargest(5, 'positive')
    
    fig = go.Figure()
    
    for sentiment in ['positive', 'neutral', 'negative']:
        fig.add_trace(go.Bar(
            name=sentiment,
            x=top_categories[sentiment],
            y=top_categories['category'],
            orientation='h',
            marker_color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment],
            customdata=top_categories[[f'{sentiment}_pct', sentiment]].values,
            hovertemplate=f"{sentiment} count: %{{customdata[1]}}<br>" +
                         f"{sentiment}: %{{customdata[0]:.1f}}%<br>" +
                         "<extra></extra>"
        ))

    fig.update_layout(
        barmode='stack',
        title='Top 5 Categories by Positive Review Count',
        xaxis_title='Number of Reviews',
        yaxis_title='Category',
        height=400,
        hovermode='y unified'
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

def create_brand_sentiment_analysis_plot(df, main_category=None):
    if main_category and main_category not in ['All Categories', 'all']:
        df = df[df['main_category'] == main_category]
    
    df = df[df['brand'] != 'Unknown Brand']
    brand_counts = df['brand'].value_counts()
    valid_brands = brand_counts[brand_counts >= 10].index
    
    brand_sentiment = []
    for brand in valid_brands:
        brand_data = df[df['brand'] == brand]
        sentiment_counts = brand_data['sentiment'].value_counts()
        total = len(brand_data)
        
        positive_count = sentiment_counts.get('positive', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negative', 0)
        
        brand_sentiment.append({
            'brand': brand,
            'positive': positive_count,
            'neutral': neutral_count,
            'negative': negative_count,
            'total': total,
            'positive_pct': (positive_count/total)*100,
            'neutral_pct': (neutral_count/total)*100,
            'negative_pct': (negative_count/total)*100
        })
    
    brand_df = pd.DataFrame(brand_sentiment)
    if not brand_df.empty:
        top_brands = brand_df.nlargest(10, 'total')
        
        fig = go.Figure()
        
        for sentiment in ['positive', 'neutral', 'negative']:
            fig.add_trace(go.Bar(
                name=sentiment,
                x=top_brands[sentiment],
                y=top_brands['brand'],
                orientation='h',
                marker_color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment],
                customdata=top_brands[[f'{sentiment}_pct', sentiment]].values,
                hovertemplate=f"{sentiment} count: %{{customdata[1]}}<br>" +
                             f"{sentiment}: %{{customdata[0]:.1f}}%<br>" +
                             "<extra></extra>"
            ))

        title = 'Top 10 Brands by Review Volume and Sentiment Distribution'
        if main_category and main_category not in ['All Categories', 'all']:
            title += f' - {main_category}'

        fig.update_layout(
            barmode='stack',
            title=title,
            xaxis_title='Number of Reviews',
            yaxis_title='Brand',
            height=500,
            hovermode='y unified'
        )
    else:
        fig = go.Figure()
        fig.update_layout(
            title='No brands with sufficient reviews in this category',
            height=500
        )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


import pandas as pd
import pandas as pd
import plotly.graph_objects as go
import json
import plotly.utils

def process_title(title):
    """Process title to make it more readable and concise"""
    if not isinstance(title, str):
        return "Unknown Title"
    
    # Remove common suffixes and prefixes
    removals = [
        " - Amazon.com",
        ", Amazon Exclusive",
        " (Discontinued by Manufacturer)",
        " (Old Version)",
        " (Latest Model)",
        " (Latest Version)",
        " (NOT for",
        " with Auto Backup",
        " for The ",
        " (Frustration-Free Packaging)"
    ]
    for removal in removals:
        title = title.replace(removal, "")
    
    # Keep only first part of product name before extensive specifications
    if " - " in title:
        title = title.split(" - ")[0]
    
    # Truncate if still too long
    if len(title) > 40:
        title = title[:37] + "..."
        
    return title

def create_top_products_plot(df, overall_category=None, sentiment_type='positive'):
    """Create visualization of top 5 products by positive reviews and ratio"""
    filtered_df = df.copy()
    if overall_category and overall_category not in ['All Categories', 'all']:
        filtered_df = filtered_df[filtered_df['overall_category'] == overall_category]
    
    filtered_df = filtered_df[
        (filtered_df['title'].notna()) & 
        (filtered_df['title'] != '') & 
        (~filtered_df['title'].str.lower().str.contains('untitled', na=False))
    ]
    
    product_counts = filtered_df['asin'].value_counts()
    valid_products = product_counts[product_counts >= 5].index
    
    if len(valid_products) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="No products with sufficient reviews in this category",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        fig.update_layout(height=400)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    product_sentiment = []
    for asin in valid_products:
        product_data = filtered_df[filtered_df['asin'] == asin]
        sentiment_counts = product_data['sentiment'].value_counts()
        total = len(product_data)
        
        original_title = product_data['title'].iloc[0]
        processed_title = process_title(original_title)
        
        positive_count = sentiment_counts.get('positive', 0)
        neutral_count = sentiment_counts.get('neutral', 0)
        negative_count = sentiment_counts.get('negative', 0)
        
        # Calculate percentages
        positive_pct = (positive_count / total) * 100
        neutral_pct = (neutral_count / total) * 100
        negative_pct = (negative_count / total) * 100
        
        # Format ratio as counts
        if sentiment_type == 'positive':
            non_positive = neutral_count + negative_count
            ratio = f"{positive_count}:{non_positive}"
            score_ratio = positive_count / (non_positive if non_positive > 0 else 1)
            sentiment_score = positive_count * score_ratio
        else:
            non_negative = neutral_count + positive_count
            ratio = f"{negative_count}:{non_negative}"
            score_ratio = negative_count / (non_negative if non_negative > 0 else 1)
            sentiment_score = negative_count * score_ratio
        
        product_sentiment.append({
            'asin': asin,
            'title': processed_title,
            'original_title': original_title,
            'positive_count': positive_count,
            'neutral_count': neutral_count,
            'negative_count': negative_count,
            'positive_pct': positive_pct,
            'neutral_pct': neutral_pct,
            'negative_pct': negative_pct,
            'ratio': ratio,
            'sentiment_score': sentiment_score
        })
    
    product_df = pd.DataFrame(product_sentiment)
    if product_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No products meet the criteria",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        fig.update_layout(height=400)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
    top_products = product_df.nlargest(5, 'sentiment_score')
    
    # Create y-axis labels with title, ASIN, and ratio
    y_labels = [
        f"{row.title}<br>ASIN: {row.asin}<br>Ratio: {row.ratio}"
        for row in top_products.itertuples()
    ]
    
    fig = go.Figure()
    
    hover_templates = {
        'positive': "count: %{x}<br>percentage: %{customdata[0]:.1f}%",
        'neutral': "count: %{x}<br>percentage: %{customdata[0]:.1f}%",
        'negative': "count: %{x}<br>percentage: %{customdata[0]:.1f}%"
    }
    
    for sentiment in ['positive', 'neutral', 'negative']:
        count_col = f'{sentiment}_count'
        pct_col = f'{sentiment}_pct'
        
        fig.add_trace(go.Bar(
            name=sentiment,
            x=top_products[count_col],
            y=y_labels,  # Use formatted y-labels instead of positions
            orientation='h',
            marker_color={'positive': '#3498db', 'neutral': '#9b59b6', 'negative': '#1abc9c'}[sentiment],
            customdata=top_products[[pct_col]].values,
            hovertemplate=hover_templates[sentiment] + "<extra></extra>"
        ))
    
    # Add ratio explanation note
    note_text = "Note: Ratio refers to positive:(neutral + negative)" if sentiment_type == 'positive' else "Note: Ratio refers to negative:(positive + neutral)"
    fig.add_annotation(
        text=note_text,
        xref='paper',
        yref='paper',
        x=0.5,
        y=-0.15,
        showarrow=False,
        font=dict(size=10, color='gray'),
        align='center'
    )
    
    title_prefix = 'Top 5'
    title = f'{title_prefix} {sentiment_type.capitalize()} Products'
    if overall_category and overall_category not in ['All Categories', 'all']:
        title += f' - {overall_category}'
        
    fig.update_layout(
        barmode='stack',
        title=title + '<br><sup>Based on both review count and sentiment ratio</sup>',
        xaxis=dict(
            title='Number of Reviews',
            range=[0, None],
            zeroline=True,
        ),
        yaxis=dict(
            title='Products',
            tickmode='array',
            ticktext=y_labels,
            tickvals=list(range(len(y_labels)))
        ),
        height=500,
        width=1000,
        hovermode='y unified',
        margin=dict(l=300, r=20, t=80, b=80),
        legend_title_text='Sentiment Categories',
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
    brand_distribution = create_brand_sentiment_analysis_plot(df)
    rating_sentiment = create_rating_sentiment_plot(df)
    category_brand_distribution = create_brand_sentiment_analysis_plot(df)
    
    # Create and pass the top products plots
    top_positive_products = create_top_products_plot(df, sentiment_type='positive')
    top_negative_products = create_top_products_plot(df, sentiment_type='negative')
    
    return render_template(
        'index_3.html',
        overall_sentiment=overall_sentiment,
        rating_distribution=rating_sentiment_dist,
        category_distribution=category_distribution,
        brand_distribution=brand_distribution,
        category_sentiment=overall_sentiment,
        rating_sentiment=rating_sentiment,
        brand_sentiment=category_brand_distribution,
        main_categories=categories,
        top_positive_products=top_positive_products,  # Add these
        top_negative_products=top_negative_products   # Add these
    )

@app.route('/update_plots/<overall_category>')
def update_plots(overall_category):
    df = load_data()
    
    return jsonify({
        'overall_plot': create_overall_sentiment_plot(df, overall_category),
        'rating_plot': create_rating_sentiment_plot(df, overall_category),
        'brand_plot': create_brand_sentiment_analysis_plot(df, overall_category),
        'top_positive_plot': create_top_products_plot(df, overall_category, 'positive'),
        'top_negative_plot': create_top_products_plot(df, overall_category, 'negative')
    })

if __name__ == '__main__':
    app.run(debug=True)