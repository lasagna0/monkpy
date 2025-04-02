# SMRetriever

**Survey Monkey Retriever** - A Python library for interacting with SurveyMonkey API through R integration.

This library was developed as part of the data analysis framework used in **Fundación Santo Domingo** to streamline the process of retrieving and processing SurveyMonkey survey data.

## Overview

SMRetriever provides a seamless interface between Python and R, allowing users to leverage the power of R's SurveyMonkey package while working in a Python environment. The library handles the complexities of the R-Python integration and properly manages NA values between both languages.

## Features

- Connect to SurveyMonkey API using R's surveymonkey package
- Retrieve list of available surveys
- Filter surveys by keywords
- Download complete survey data
- Process multiple surveys in batch
- Automatic handling of R NA values, converting them to appropriate pandas NA values
- Streamlined R package management

## Requirements

- Python 3.7+
- R 4.0+
- Required R packages:
  - tidyverse
  - surveymonkey
  - ggplot2
  - readxl


Basic usage example:

```python
from smretriever import SurveyMonkeyClient

# Initialize the client
client = SurveyMonkeyClient(oauth_token="your_oauth_token")

# Get available surveys
surveys = client.get_available_surveys()
print(surveys)

# Filter surveys by keyword
filtered_surveys = client.filter_surveys("Customer Satisfaction")
print(filtered_surveys)

# Download data from a specific survey
survey_data = client.download_survey_data(survey_id=123456789)
print(survey_data.head())

# Download multiple surveys
survey_ids = [123456789, 987654321]
multiple_surveys = client.download_multiple_surveys(survey_ids)
```

## Development Context

This library was created to support data analysis efforts at Fundación Santo Domingo, specifically for processing and analyzing survey data collected through SurveyMonkey. It's part of a broader initiative to leverage data for social impact measurement and program evaluation.

## License

MIT

## Author

Data Analytics Team @ Fundación Santo Domingo 