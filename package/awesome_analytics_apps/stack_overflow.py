import pandas as pd
import pathlib
import zipfile


LOCAL_ROOT = pathlib.Path.cwd()
GITHUB_ROOT = (
    "https://raw.githubusercontent.com/MarcSkovMadsen/awesome-analytics-apps/master/"
)
DATA_STACK_OVERFLOW = "data/stackoverflow/"
ZIP_FILE_2019 = "developer_survey_2019.zip"
RESULTS_2019 = "survey_results_public.csv"
SCHEMA_2019 = "survey_results_schema.csv"
IMAGE_2019 = "assets/image/stack_overflow_survey_2019.png"


def get_zip_file() -> zipfile.ZipFile:
    return zipfile.ZipFile(LOCAL_ROOT / DATA_STACK_OVERFLOW / ZIP_FILE_2019)


def read_results() -> pd.DataFrame:
    with get_zip_file().open(RESULTS_2019) as file:
        return pd.read_csv(file)


def read_schema() -> pd.DataFrame:
    with get_zip_file().open(SCHEMA_2019) as file:
        return pd.read_csv(file)
