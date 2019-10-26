"""This module provides general functionality to work with the Stack Overflow Developer Surveys"""
import pathlib
import zipfile

import pandas as pd

LOCAL_ROOT = pathlib.Path.cwd()
GITHUB_ROOT = (
    "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-analytics-apps/master/"
)
DATA_STACK_OVERFLOW = "data/stackoverflow/"
ZIP_FILE_2019 = "developer_survey_2019.zip"
RESULTS_2019 = "survey_results_public.csv"
SCHEMA_2019 = "survey_results_schema.csv"
IMAGE_2019_URL = "https://github.com/MarcSkovMadsen/awesome-analytics-apps/blob/master/assets/images/stack_overflow_survey_2019.png?raw=true" # pylint: disable=line-too-long
SURVEY_2019_URL = "https://insights.stackoverflow.com/survey/2019"
DATA_URL = "https://insights.stackoverflow.com/survey"


def _get_zip_file() -> zipfile.ZipFile:
    return zipfile.ZipFile(LOCAL_ROOT / DATA_STACK_OVERFLOW / ZIP_FILE_2019)


def read_results() -> pd.DataFrame:
    """The Stack Overflow Developer Survey Results

    Returns:
        pd.DataFrame -- A DataFrame containing the Stack Overflow Developer Survey Results
    """
    with _get_zip_file().open(RESULTS_2019) as file:
        return pd.read_csv(file)


def read_schema() -> pd.DataFrame:
    """The Stack Overflow Developer Survey Questions

    Returns:
        pd.DataFrame -- A DataFrame containing the Stack Overflow Developer Survey Questions
    """
    with _get_zip_file().open(SCHEMA_2019) as file:
        return pd.read_csv(file)
