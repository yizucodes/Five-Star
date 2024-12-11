# Amazon Electronics Review Sentiment Analysis

A comprehensive sentiment analysis project analyzing Amazon Electronics product reviews using VADER and TextBlob sentiment analysis techniques, featuring an interactive visualization dashboard.

## Project Overview

This project conducts sentiment analysis on Amazon product reviews in the Electronics category. Using Natural Language Processing (NLP) techniques, VADER and TextBlob sentiment analyzers, we analyze customer sentiment patterns and derive insights from user feedback through an interactive dashboard.

### Key Features

- Sentiment analysis using VADER and TextBlob
- Interactive visualizations of sentiment trends
- Keyword analysis and feature extraction
- Product and brand-level sentiment insights
- Comprehensive data preprocessing pipeline

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Conda (Anaconda/Miniconda)
- Git (for cloning the repository)

### Required Packages

```yaml
name: sentiment_analysis_env
dependencies:
  - python=3.9
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - tqdm
  - wordcloud
  - flask
  - scikit-learn
  - spacy
  - pip
  - pip:
      - vaderSentiment
      - notebook
      - plotly
      - nbformat
      - textblob
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Five-Star.git
cd Five-Star
```

2. Create the Conda environment:

```bash
conda env create -f environment.yml
```

3. Activate the environment:

```bash
conda activate sentiment_analysis_env
```

4. Install the spaCy language model:

```bash
# First verify spaCy installation
python -c "import spacy; print(spacy.__version__)"

# Download the English language model
python -m spacy download en_core_web_sm

# Verify the language model installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy language model installed successfully')"
```

If you encounter any errors during the spaCy language model installation:

- For Windows users:
  ```bash
  pip install --no-cache-dir spacy
  python -m spacy download en_core_web_sm
  ```
- For Unix/Mac users:
  ```bash
  pip install --upgrade spacy
  python -m spacy download en_core_web_sm
  ```

5. Start Jupyter Notebook:

```bash
jupyter notebook
```

6. Verify the complete installation:

```bash
python -c "import pandas, numpy, matplotlib, seaborn, tqdm, wordcloud, flask, vaderSentiment, notebook, plotly, nbformat, textblob, spacy; import en_core_web_sm; print('Setup successful')"
```

## Project Structure

```
Five-Star/
├── data/                    # Data files and analysis results
├── docs/                    # Project documentation and rubrics
├── notebooks/              # Jupyter notebooks for analysis
├── src/                    # Python source code files
├── templates/              # HTML templates
├── .gitignore             # Git ignore file
├── environment.yml        # Conda environment configuration
├── Final_SA_Amazon_Presentation.pptx  # Final presentation
└── README.md              # Project documentation
```

## Data Sources

The project uses the Amazon Product Reviews dataset from 2014, available at:
https://jmcauley.ucsd.edu/data/amazon/index_2014.html

### Review Information

#### Core Review Data

| Column Name | Description                         |
| ----------- | ----------------------------------- |
| reviewer_id | Unique identifier for each reviewer |
| asin        | Amazon product identifier           |
| review_text | Full text of the review             |
| overall     | Star rating (1-5 scale)             |
| summary     | Short review title/summary          |

#### Review Metadata

| Column Name      | Description                          |
| ---------------- | ------------------------------------ |
| helpful          | List of [helpful_votes, total_votes] |
| helpful_ratio    | Ratio of helpful to total votes      |
| unix_review_time | Review timestamp (Unix format)       |
| review_time      | Review date (MM DD, YYYY)            |
| review_date      | Review date (YYYY-MM-DD)             |
| formatted_date   | Standardized date format             |

#### Text Analysis

| Column Name    | Description                                      |
| -------------- | ------------------------------------------------ |
| cleaned_text   | Preprocessed review text                         |
| processed_text | Tokenized/stemmed text                           |
| review_length  | Character count                                  |
| word_count     | Number of words                                  |
| sentiment      | Calculated sentiment (positive/neutral/negative) |

#### Product Information

| Column Name   | Description           |
| ------------- | --------------------- |
| category      | Raw product category  |
| main_category | Main product category |
| description   | Product description   |
| title         | Product name          |
| brand         | Manufacturer          |
| price         | Product price in USD  |

## Dashboard

The project includes an interactive Flask-based visualization dashboard that provides comprehensive insights into review sentiments.

### Features

- **Overall Sentiment Distribution**: Interactive pie charts showing sentiment breakdowns
- **Rating Analysis**:
  - Sentiment distribution across different star ratings
  - Grouped bar charts showing sentiment patterns
- **Category Analysis**:
  - Top 10 product categories by review count
  - Interactive category filtering
  - Sentiment distribution within each category
- **Brand Analysis**:
  - Top 10 brands by review volume
  - Sentiment distribution for each major brand
  - Category-specific brand performance
- **Product Performance**:
  - Top 5 positive and negative products
  - Detailed sentiment ratios and review counts
  - Product identification by ASIN and title

### Running the Dashboard

1. Activate your environment:

```bash
conda activate sentiment_analysis_env
```

2. Navigate to the `src` directory and run:

```bash
python3 04_data_visualization_advanced_part4.py
```

### Interactive Features

- Filter visualizations by product category
- Hover over charts for detailed information
- Dynamic updates based on category selection
- Color-coded sentiment indicators (blue for positive, purple for neutral, turquoise for negative)

![Interactive Dashboard](/data/visuals/dashboard.png)

## Key Findings

Our analysis revealed several important insights about Amazon Electronics reviews:

### Sentiment Distribution

- Majority of reviews show positive sentiment (82.9%)
- Neutral reviews account for 11% of total
- Negative reviews represent 6.1% of the dataset

### Rating-Sentiment Correlation

- Strong correlation between star ratings and sentiment analysis results
- Higher star ratings consistently show more positive sentiment
- Mixed sentiments appear more frequently in 3-star reviews

### Category Insights

- Certain product categories show consistently higher positive sentiment
- Technical products tend to have more detailed and nuanced sentiment patterns
- Price sensitivity varies significantly across categories

### Brand Performance

- Top brands maintain consistently higher positive sentiment ratios
- Brand sentiment varies significantly by product category
- Customer service and product reliability are key factors in brand sentiment

### Product-Level Analysis

- Products with high review counts tend to show more balanced sentiment distribution
- Price point correlates with sentiment patterns
- Technical specifications and ease of use are frequent sentiment drivers

## Analysis Features

- Sentiment classification using VADER and TextBlob
- Word frequency analysis
- Brand and product category sentiment trends
- Temporal sentiment analysis
- Review helpfulness correlation

## Usage

1. Start by exploring the Jupyter notebooks in the `notebooks/` directory
2. Load and preprocess data using provided scripts
3. Run sentiment analysis on desired product reviews
4. Generate visualizations and insights

## Maintenance

To update the environment with new dependencies:

```bash
conda env update -f environment.yml --prune
```

To deactivate the environment:

```bash
conda deactivate
```

## Team Members

- [Nishtha Sawhney](https://github.com/sawhneyn)
- [Yi Zu](https://github.com/yizucodes/)

## License

This project is part of the DS5110 course at Northeastern University.

## References

- [VADER Sentiment Analysis Documentation](https://github.com/cjhutto/vaderSentiment)
- [TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)
- [Original Dataset Paper](https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys13.pdf)
