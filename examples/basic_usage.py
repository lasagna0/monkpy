#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basic usage example for the SMRetriever library.
Developed for Fundación Santo Domingo data analysis framework.
"""

import pandas as pd
from smretriever import SurveyMonkeyClient

def main():
    # Replace with your own token if needed
    oauth_token = "your_oauth_token_here"
    
    # Initialize the client
    print("Initializing SurveyMonkey client...")
    client = SurveyMonkeyClient(oauth_token=oauth_token)
    
    # Get available surveys
    print("Retrieving available surveys...")
    surveys = client.get_available_surveys(limit=50)
    print(f"Found {len(surveys)} surveys")
    
    if len(surveys) > 0:
        # Display the first 5 surveys
        print("\nFirst 5 surveys:")
        print(surveys.head())
        
        # Filter surveys by keyword
        keyword = "Satisfaction"
        print(f"\nFiltering surveys by keyword: '{keyword}'")
        filtered_surveys = client.filter_surveys(keyword)
        print(f"Found {len(filtered_surveys)} surveys matching the keyword")
        
        if len(filtered_surveys) > 0:
            # Get the first survey ID from the filtered list
            survey_id = filtered_surveys.iloc[0]['survey_id']
            
            # Download data from that survey
            print(f"\nDownloading data from survey ID: {survey_id}")
            survey_data = client.download_survey_data(survey_id)
            
            print(f"Successfully downloaded data. Shape: {survey_data.shape}")
            print("\nFirst 5 rows:")
            print(survey_data.head())
            
            # Check for NA values
            na_counts = survey_data.isna().sum()
            print("\nNA counts per column:")
            print(na_counts[na_counts > 0])  # Only show columns with NA values
            
            # Save to CSV
            output_file = f"survey_{survey_id}_data.csv"
            survey_data.to_csv(output_file, index=False)
            print(f"\nData saved to {output_file}")
    
    print("\nDone!")

if __name__ == "__main__":
    main() 