import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_month_start_end_dates(year):
    """Returns the start and end dates for each month of the given year."""
    month_dates = {}
    for month in range(1, 13):
        # Start date is always the first of the month
        start_date = datetime(year, month, 1)
        # End date is the day before the first of the next month
        if month == 12:  # For December, the next month is January of the next year
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Formatting dates as 'yyyymmdd' and storing in dictionary
        month_dates[month] = {
            'start_date': start_date.strftime('%Y%m%d'),
            'end_date': end_date.strftime('%Y%m%d')
        }
    return month_dates


# Replace with your actual API endpoint
API_ENDPOINT = 'http://127.0.0.1:80//topics//get_k_topics_by_date'
EXCLUDE_PHRASES = ["two", "second", "night","friday", "morning", "first", "sunday", "thursday", "summer","saturday","monday", "1st", "today", "tonight", "one", "less than 24 hours", "tbt", "the day","1", "month of the year", "next week", "last day","one day", "this week","the week", "next year", "this year", "the year", "last night's" ,"last night", "all day","every day", "tomorrow", "yesterday", "the weekend", "this weekend","everyday" ,"last night","last week", "last year", "this day"]


# Loop through each month, make API calls, and generate word clouds
for year in range(2012,2018):
    month_dates_year = get_month_start_end_dates(year)
    for month, dates in month_dates_year.items():
        try:
            params = {
                'k': 25,
                'start_date': dates['start_date'],
                'end_date': dates['end_date']
            }
            # Making a GET request to the API
            response = requests.get(API_ENDPOINT, params=params)
            data = response.json()

            # Extract topics and their trend scores, excluding certain phrases
            word_frequencies = {item['topic']: item['trend_score'] for item in data if item['topic'] not in EXCLUDE_PHRASES}

            # Generate the word cloud
            wordcloud = WordCloud(width=800, height=400, stopwords=EXCLUDE_PHRASES).generate_from_frequencies(word_frequencies)

            # Display the word cloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            # Save the word cloud to a PNG file
            plt.savefig(f"top25-visoalization/top25_topics_of_year_{year}_month_{month}.png")
            plt.close()  # C
        except Exception as ex:
            print(f'failed to get top 25 topics for year:{year} and month:{month}. error: {ex}')

'''params = {
    'k': 25,
    'start_date': "20170201",
    'end_date': "20170228"
}
# Making a GET request to your API
response = requests.get(API_ENDPOINT, params=params)
data = response.json()

# Extracting topics and their trend scores
word_frequencies = {item['topic']: item['trend_score'] for item in data if item['topic'] not in EXCLUDE_PHRASES}

# Generating the word cloud
wordcloud = WordCloud(width=800, height=400, stopwords= EXCLUDE_PHRASES ).generate_from_frequencies(word_frequencies)

# Displaying the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()'''