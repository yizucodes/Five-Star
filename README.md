# Five-Star
DS5110 Final Project

Required packages

`pip install pandas numpy nltk jupyter matplotlib seaborn vaderSentiment`

Dataset: https://jmcauley.ucsd.edu/data/amazon/index_2014.html

## Dataset Column Descriptions

1. **`reviewer_id`**:
   - Unique identifier for the reviewer who wrote the review.

2. **`asin`**:
   - Amazon Standard Identification Number, a unique identifier for the product being reviewed.

3. **`reviewer_name`**:
   - Name of the reviewer, if provided.

4. **`helpful`**:
   - A list in the format `[helpful_votes, total_votes]`, showing the number of helpful votes and total votes cast for the review.

5. **`helpful_ratio`**:
   - A calculated value representing the ratio of helpful votes to total votes (`helpful_votes / total_votes`). Missing if `total_votes` is 0.

6. **`review_text`**:
   - The full text of the review written by the reviewer.

7. **`overall`**:
   - Star rating given to the product by the reviewer, typically ranging from 1 to 5.

8. **`summary`**:
   - A short title or summary provided by the reviewer to describe their review.

9. **`unix_review_time`**:
   - The timestamp of the review in Unix time format (seconds since 1970-01-01).

10. **`review_time`**:
    - The review date in `MM DD, YYYY` format.

11. **`review_date`**:
    - A cleaned or reformatted version of `review_time` in `YYYY-MM-DD` format.

12. **`cleaned_text`**:
    - The `review_text` after preprocessing steps like removing special characters, extra spaces, or unnecessary formatting.

13. **`processed_text`**:
    - Further processed version of `cleaned_text` for tasks like sentiment analysis, including tokenization or stemming.

14. **`formatted_date`**:
    - Another reformatted version of the review date, potentially standardized for specific analysis.

15. **`review_length`**:
    - The total number of characters in the `review_text`.

16. **`word_count`**:
    - The total number of words in the `review_text`.

17. **`category`**:
    - Specific sub-category of the product being reviewed.

18. **`main_category`**:
    - Broader category to which the product belongs (e.g., "Electronics", "Books").

19. **`description`**:
    - A brief description of the product, if available.

20. **`title`**:
    - Title of the product being reviewed.

21. **`brand`**:
    - Brand or manufacturer of the product.

22. **`price`**:
    - Price of the product at the time of the review. Missing values indicate the price was not available.

23. **`sentiment`**:
    - The overall sentiment derived from the `review_text` or `summary`, typically categorized as "positive", "negative", or "neutral".