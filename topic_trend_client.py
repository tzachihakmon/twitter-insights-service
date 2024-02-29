import requests
import matplotlib.pyplot as plt


for year in range(2012,2018):
    params = {
        'k': 50,
        'start_date': f'{year}0101',
        'end_date': f'{year}1231',
    }
    try:
        get_top_k_of_the_year_url = f'http://127.0.0.1:80//topics//get_k_topics_by_date'
        response = requests.get(get_top_k_of_the_year_url, params=params)
        topic_items = response.json()
        for item in topic_items:
            try:
                topic = item['topic']
                url = f'http://127.0.0.1:80/topics/{topic}?year={year}'
                response = requests.get(url)
                data = response.json()
                # Prepare the data for plotting
                months = sorted(data.keys(), key=int)  # Sort the months as integers but keys are strings
                scores = [data[month] for month in months]

                # Convert month numbers to integers for plotting
                months_int = [int(month) for month in months]

                # Create the plot
                plt.figure(figsize=(10, 6))
                plt.plot(months_int, scores, marker='o', linestyle='-', color='b')

                # Set the title and labels
                plt.title(f'Trend Score by Month for {topic} in 2016')
                plt.xlabel('Month')
                plt.ylabel('Trend Score')
                plt.xticks(months_int)  # Ensure only integer months are used as ticks

                # Show the plot
                plt.savefig(f"topics_trends_over_the_year/{year}/{topic}.png")
                plt.close()         
            except Exception as ex:
                print(f"Fail to create trend to topic:{topic} in year: {year}. Error: {ex}")

    except Exception as ex:
        print(f"Fail to get topics for year: {year}. Error: {ex}")
        continue

'''# Define the API endpoint
url = 'http://127.0.0.1:80/topics/hillaryclinton?year=2016'

# Send a GET request to the API
response = requests.get(url)
data = response.json()

# Prepare the data for plotting
months = sorted(data.keys(), key=int)  # Sort the months as integers but keys are strings
scores = [data[month] for month in months]

# Convert month numbers to integers for plotting
months_int = [int(month) for month in months]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(months_int, scores, marker='o', linestyle='-', color='b')

# Set the title and labels
plt.title('Trend Score by Month for "hillaryclinton" in 2016')
plt.xlabel('Month')
plt.ylabel('Trend Score')
plt.xticks(months_int)  # Ensure only integer months are used as ticks

# Show the plot
plt.savefig(f"top25-visoalization/top25_topics_of_year_{year}_month_{month}.png")
plt.close()  # C'''