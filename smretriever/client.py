import pandas as pd
import os
import sys
import numpy as np

class SurveyMonkeyClient:
    """
    Client for interacting with SurveyMonkey API through R
    
    This client was developed as part of the data analysis framework 
    used in Fundación Santo Domingo to streamline the process of retrieving
    and processing SurveyMonkey survey data.
    """
    def __init__(self, oauth_token=None, r_home=None):
        """
        Initialize the SurveyMonkey client
        
        Args:
            oauth_token (str, optional): OAuth token for SurveyMonkey API
            r_home (str, optional): Path to R installation directory
        """
        # Set R_HOME environment variable
        if r_home is None:
            r_home = "C:/Program Files/R/R-4.3.3"
        
        os.environ["R_HOME"] = r_home
        
        # Check if R_HOME is properly set
        if not os.path.exists(r_home):
            print(f"Warning: R_HOME path '{r_home}' does not exist")
            print("Please install R or set the correct R_HOME path")
            
        try:
            # Import rpy2 modules after setting R_HOME
            import rpy2.robjects as robjects
            from rpy2.robjects.packages import importr
            import rpy2.rinterface as rinterface
            
            self.robjects = robjects
            self.rinterface = rinterface
            
            # Store NA values for later identification
            self.na_types = {
                'integer': rinterface.NA_Integer,
                'real': rinterface.NA_Real,
                'logical': rinterface.NA_Logical,
                'character': rinterface.NA_Character,
                'complex': rinterface.NA_Complex
            }
            
            # Initialize R package manager
            self.r_manager = RPackageManager()
            
            # Import required packages
            self.tidyverse = self.r_manager.import_package('tidyverse')
            self.ggplot2 = self.r_manager.import_package('ggplot2')
            self.surveymonkey = self.r_manager.import_package('surveymonkey')
            self.readxl = self.r_manager.import_package('readxl')
            
            # Set up token for SurveyMonkey API
            if oauth_token:
                robjects.r(f'options(sm_oauth_token = "{oauth_token}")')
            
        except Exception as e:
            print(f"Error initializing R environment: {str(e)}")
            print("Make sure R is installed and R_HOME is correctly set")
            sys.exit(1)
        
    def get_available_surveys(self, limit=200):
        """
        Retrieve available surveys from SurveyMonkey
        
        Args:
            limit (int): Maximum number of surveys to retrieve
            
        Returns:
            pandas.DataFrame: DataFrame containing survey information
        """
        r_surveys = self.robjects.r(f'browse_surveys({limit})')
        # Convert R dataframe to pandas dataframe
        surveys_df = pd.DataFrame(dict(zip(r_surveys.names, list(r_surveys))))
        return surveys_df
        
    def filter_surveys(self, keyword):
        """
        Filter surveys by keyword in title
        
        Args:
            keyword (str): Keyword to search for in survey titles
            
        Returns:
            pandas.DataFrame: Filtered DataFrame of surveys
        """
        r_code = f'''
        surveys %>%
            filter(title %>% str_detect("{keyword}"))
        '''
        filtered = self.robjects.r(r_code)
        return pd.DataFrame(dict(zip(filtered.names, list(filtered))))
        
    def download_survey_data(self, survey_id):
        """
        Download and parse survey data
        
        Args:
            survey_id (int): ID of the survey to download
            
        Returns:
            pandas.DataFrame: DataFrame containing survey responses
        """
        r_code = f'''
        df <- {survey_id} %>%
            fetch_survey_obj %>%
            parse_survey(fix_duplicates = 'none')
        
        df <- df %>% filter(response_status=="completed")
        df
        '''
        survey_data = self.robjects.r(r_code)
        
        # Convert R dataframe to pandas dataframe
        pandas_df = pd.DataFrame(dict(zip(survey_data.names, list(survey_data))))
        
        # Replace R NA values with pandas NA
        pandas_df = self._replace_r_na_with_pandas_na(pandas_df, survey_data)
        
        return pandas_df
        
    def _replace_r_na_with_pandas_na(self, pandas_df, r_dataframe):
        """
        Replace R NA values with pandas NA values
        
        Args:
            pandas_df (pandas.DataFrame): DataFrame converted from R
            r_dataframe (rpy2.robjects.DataFrame): Original R dataframe
            
        Returns:
            pandas.DataFrame: DataFrame with R NA values replaced with pandas NA
        """
        # Import utilities needed for NA checking
        from rpy2.robjects.vectors import NA_Character, NA_Integer, NA_Logical, NA_Real
        
        # Get column names from the R dataframe
        col_names = r_dataframe.names
        
        # Iterate through columns in the dataframe
        for i, col_name in enumerate(col_names):
            r_vector = r_dataframe[i]
            
            # Get the R vector's type
            vec_type = r_vector.rclass[0]
            
            # Different handling based on the vector type
            if vec_type == 'numeric' or vec_type == 'integer':
                # For numeric vectors
                for j in range(len(r_vector)):
                    try:
                        # Check for NA using the appropriate method
                        value = r_vector[j]
                        if value is NA_Real or value is NA_Integer:
                            pandas_df.loc[j, col_name] = np.nan
                    except Exception as e:
                        print(f"Error checking NA for {col_name} at index {j}: {str(e)}")
            
            elif vec_type == 'character':
                # For character vectors
                for j in range(len(r_vector)):
                    try:
                        # Check for NA using the appropriate method
                        value = r_vector[j]
                        if value is NA_Character:
                            pandas_df.loc[j, col_name] = pd.NA
                    except Exception as e:
                        print(f"Error checking NA for {col_name} at index {j}: {str(e)}")
            
            elif vec_type == 'logical':
                # For logical vectors
                for j in range(len(r_vector)):
                    try:
                        # Check for NA using the appropriate method
                        value = r_vector[j]
                        if value is NA_Logical:
                            pandas_df.loc[j, col_name] = pd.NA
                    except Exception as e:
                        print(f"Error checking NA for {col_name} at index {j}: {str(e)}")
                        
            elif vec_type == 'factor':
                # For factor vectors
                for j in range(len(r_vector)):
                    try:
                        value = r_vector[j]
                        # R factor NA is typically represented as the integer 0 in the 1-indexed system
                        if value <= 0:  # Any value <= 0 is not a valid factor level index in R
                            pandas_df.loc[j, col_name] = pd.NA
                    except Exception as e:
                        print(f"Error checking NA for {col_name} at index {j}: {str(e)}")
        
        return pandas_df

    def download_multiple_surveys(self, survey_ids):
        """
        Download and parse data for multiple surveys

        Args:
            survey_ids (list): List of survey IDs to download

        Returns:
            dict: Dictionary where keys are survey IDs and values are pandas DataFrames
                  containing survey responses for each survey.
        """
        survey_data_dict = {}
        for survey_id in survey_ids:
            try:
                print(f"Downloading data for survey ID: {survey_id}")
                df = self.download_survey_data(survey_id)
                survey_data_dict[survey_id] = df
                print(f"Successfully downloaded data for survey ID: {survey_id}")
            except Exception as e:
                print(f"Error downloading data for survey ID {survey_id}: {str(e)}")
                survey_data_dict[survey_id] = None  # Or handle error as needed
        return survey_data_dict


class RPackageManager:
    """
    Manages R package imports and installations
    """
    def __init__(self):
        # Import rpy2 modules
        import rpy2.robjects as robjects
        from rpy2.robjects.packages import importr
        
        # Import base R packages
        self.utils = importr('utils')
        self.base = importr('base')
        
        # Dictionary to store imported packages
        self.packages = {
            'utils': self.utils,
            'base': self.base
        }
        
    def import_package(self, package_name):
        """
        Import an R package, installing it if necessary
        
        Args:
            package_name (str): Name of the R package to import
            
        Returns:
            The imported R package
        """
        from rpy2.robjects.packages import importr
        
        if package_name in self.packages:
            return self.packages[package_name]
            
        try:
            package = importr(package_name)
        except:
            self.utils.install_packages(package_name)
            package = importr(package_name)
            
        self.packages[package_name] = package
        return package 
