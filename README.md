# Fast_API

This API was built for the backend of my React Web Development project (https://github.com/andrewckimball/React_Final_Project). The scripts in the 'Scraping' folder were written to scrape data from Wikipedia and other sources in order to gather biography information on United States senators. The API also uses a pretrained machine learning model for predicting Twitter authors among all 100 US senators. The model accepts as input a string of text (up to 280 characters) and returns the most likely senator to have authored the input.

To run this project locally, clone this repository and run "uvicorn main:app --reload" in the project folder.
