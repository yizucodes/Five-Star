# Amazon Electronics Review Sentiment Analysis

A comprehensive sentiment analysis project analyzing Amazon Electronics product reviews using VADER and TextBlob sentiment analysis techniques, featuring an interactive visualization dashboard.

---

## Project Overview

This project conducts sentiment analysis on Amazon product reviews in the Electronics category. Using Natural Language Processing (NLP) techniques, VADER and TextBlob sentiment analyzers, we analyze customer sentiment patterns and derive insights from user feedback through an interactive dashboard.

### Summary of Key Insights

- **Sentiment Distribution**:
  - Positive sentiment: 82.9% of reviews
  - Neutral sentiment: 11% of reviews
  - Negative sentiment: 6.1% of reviews
- **Rating-Sentiment Correlation**:
  - Higher star ratings align strongly with positive sentiment.
  - Mixed sentiments are more common in 3-star reviews.
- **Category and Brand Insights**:
  - Certain product categories and brands exhibit consistently higher positive sentiment.
  - Technical products have more detailed sentiment patterns.
- **Product-Level Analysis**:
  - High-review-count products show balanced sentiment distribution.
  - Price and technical specifications are key drivers of sentiment.

---

## Key Findings

### Sentiment Distribution

- Majority of reviews show positive sentiment (82.9%).
- Neutral reviews account for 11% of total.
- Negative reviews represent 6.1% of the dataset.

### Rating-Sentiment Correlation

- Strong correlation between star ratings and sentiment analysis results.
- Higher star ratings consistently show more positive sentiment.
- Mixed sentiments appear more frequently in 3-star reviews.

### Category Insights

- Certain product categories show consistently higher positive sentiment.
- Technical products tend to have more detailed and nuanced sentiment patterns.
- Price sensitivity varies significantly across categories.

### Brand Performance

- Top brands maintain consistently higher positive sentiment ratios.
- Brand sentiment varies significantly by product category.
- Customer service and product reliability are key factors in brand sentiment.

---

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

---

## Data Overview

**Raw data source:** https://jmcauley.ucsd.edu/data/amazon/index_2014.html
**Processed reviews:** [final_sentiment_analysis_data.csv](https://github.com/yizucodes/Five-Star/blob/main/data/processed/final_sentiment_analysis_data.csv)

### Core Review Data

| Column Name | Description                         |
| ----------- | ----------------------------------- |
| reviewer_id | Unique identifier for each reviewer |
| asin        | Amazon product identifier           |
| review_text | Full text of the review             |
| overall     | Star rating (1-5 scale)             |
| summary     | Short review title/summary          |

### Metadata

| Column Name      | Description                          |
| ---------------- | ------------------------------------ |
| helpful          | List of [helpful_votes, total_votes] |
| helpful_ratio    | Ratio of helpful to total votes      |
| unix_review_time | Review timestamp (Unix format)       |
| review_time      | Review date (MM DD, YYYY)            |
| review_date      | Review date (YYYY-MM-DD)             |

### Text Analysis

| Column Name    | Description                                      |
| -------------- | ------------------------------------------------ |
| cleaned_text   | Preprocessed review text                         |
| processed_text | Tokenized/stemmed text                           |
| review_length  | Character count                                  |
| word_count     | Number of words                                  |
| sentiment      | Calculated sentiment (positive/neutral/negative) |

---

## Prerequisites and Installation

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
python -m spacy download en_core_web_sm
```

5. Verify the setup:

```bash
python -c "import pandas, numpy, matplotlib, seaborn, tqdm, wordcloud, flask, vaderSentiment, notebook, plotly, nbformat, textblob, spacy; print('Setup successful')"
```

---

## Analysis and Dashboard

### Usage Instructions

1. Start by exploring the Jupyter notebooks in the `notebooks/` directory:

```bash
jupyter notebook
```

2. Load and preprocess data using `02_preprocessing_reviews_data_part3.ipynb`.
3. Run sentiment analysis on desired product reviews using `03_sentiment_analysis_indepth_part2.ipynb`.

### Dashboard Features

The project includes an interactive Flask-based dashboard to visualize results.

- **Overall Sentiment Distribution**: Interactive pie charts showing sentiment breakdowns.
- **Rating Analysis**:
  - Sentiment distribution across star ratings.
  - Grouped bar charts showing sentiment patterns.
- **Category and Brand Analysis**:
  - Top categories/brands by review count.
  - Sentiment distribution within each category/brand.
- **Product Insights**:
  - Top 5 positive and negative products.
  - Sentiment ratios and review counts.

### Running the Dashboard

1. Activate the environment:

```bash
conda activate sentiment_analysis_env
```

2. Navigate to the `src` directory and run:

```bash
python3 04_data_visualization_advanced_part4.py
```

![Interactive Dashboard](/data/visuals/dashboard.png)

---

## Key Features of Analysis

- Sentiment classification using VADER and TextBlob.
- Word frequency analysis.
- Brand and product category sentiment trends.
- Temporal sentiment analysis.
- Review helpfulness correlation.

---

## Team Members

- [Nishtha Sawhney](https://github.com/sawhneyn)
- [Yi Zu](https://github.com/yizucodes/)

---

## License

This project is part of the DS5110 course at Northeastern University.

---

## References

- [VADER Sentiment Analysis Documentation](https://github.com/cjhutto/vaderSentiment)
- [TextBlob Documentation](https://textblob.readthedocs.io/en/dev/)
- [Original Dataset Paper](https://cseweb.ucsd.edu/~jmcauley/pdfs/recsys13.pdf)
