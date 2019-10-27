"""This module contains the Streamlit app"""
# pylint: disable=no-member
from typing import List, Optional

import pandas as pd
import streamlit as st
from plotly import express as px

import awesome_analytics_apps.stack_overflow as stack_overflow


def main():
    """This is the main function of the app."""
    st.title("Awesome Analytics Apps in Streamlit")

    st.header("Introduction")

    st.info(
        "You can use Python and Streamlit as shown in the code below to create a web app."
    )

    with st.echo():
        st.markdown("For more info watch the ***4 minutes introduction*** to Streamlit")
        st.video(data="https://www.youtube.com/watch?v=B2iAodr0fOo")

    resources_component()

    with st.spinner("Loading data from Stack Overflow ..."):
        schema = read_stack_overflow_schema_2019()
        results = read_stack_overflow_results_2019()

    stack_overflow_component(schema, results)

    # Insert your app code below


def resources_component():
    """The Resources Component writes a list of resources links"""
    st.sidebar.header("Resources")
    st.sidebar.markdown(
        """\
    - [Streamlit](https://streamlit.io/)
    - [Streamlit Docs](https://streamlit.io/docs/)
    - [Streamlit Forum](https://discuss.streamlit.io/)
    - [Streamlit GitHub](https://github.com/streamlit/streamlit)
    - [Awesome Streamlit Gallery](http://awesome-streamlit.org/)
    - [Awesome Streamlit GitHub](https://github.com/marcskovmadsen/awesome-streamlit)
    - [Awesome Streamlit Docs](https://github.com/marcskovmadsen/awesome-streamlit)
    - [Awesome Analytics Apps GitHub](https://github.com/MarcSkovMadsen/awesome-analytics-apps)
    """
    )


def stack_overflow_component(schema: pd.DataFrame, results: pd.DataFrame):
    """The Stack Overflow compontent writes the Questions, Results and a Distribution"""
    st.header("Stack Overflow 2019")

    st.markdown(
        "You will be analyzing and providing insights from the Stack Overflow 2019 survey"
    )
    st.markdown(
        f"""
        <a href="{stack_overflow.SURVEY_2019_URL}" target="_blank">
        <img src="{stack_overflow.IMAGE_2019_URL}"style="width:100%;">
        </a>

        Results: [{stack_overflow.SURVEY_2019_URL}]({stack_overflow.DATA_URL})

        Data: [{stack_overflow.DATA_URL}]({stack_overflow.DATA_URL})
        """,
        unsafe_allow_html=True,
    )
    selected_questions = stack_overflow_questions_component(schema)
    stack_overflow_answers_component(results, selected_questions)
    respondents_per_country_component(results)

def stack_overflow_questions_component(schema: pd.DataFrame) -> Optional[List[str]]:
    """This component writes the Stack Overflow Developer Questions and returns a selected list of
    questions

    Arguments:
        schema {pd.DataFrame} -- A DataFrame of questions

    Returns:
        Optional[List[str]] -- [description]
    """
    st.subheader("Stack Overflow Questions 2019")
    questions = st.multiselect(
        "Select questions", options=sorted(schema["Column"].unique())
    )
    if questions:
        schema_to_show = schema[schema["Column"].isin(questions)]
    else:
        number_of_schema_rows = st.radio(
            "Select # Questions to show?", options=[10, len(schema)], index=0
        )
        schema_to_show = schema.head(number_of_schema_rows)

    st.table(schema_to_show)
    return questions

def stack_overflow_answers_component(results, selected_questions: Optional[List[str]]):
    """This component writes the Stack Overflow Developer Survey Questions

    Arguments:
        results {[type]} -- A DataFrame of the Results
        selected_questions {Optional[List[str]]} -- a list of questions to filter
    """

    st.subheader("Answers 2019")
    # We st.empty() to position the dataframe and then later fill it
    st_answers_dataframe = st.empty()

    number_of_rows_to_show = st.selectbox(
        "Select # Answers to show", options=[10, 50, 500, 5000, len(results)], index=0
    )
    results_to_show = results
    if selected_questions:
        results_to_show = results_to_show[selected_questions]
    results_to_show = results_to_show.head(number_of_rows_to_show)

    if len(results_to_show.columns) > 2:
        st_answers_dataframe.dataframe(results_to_show)
    else:
        st_answers_dataframe.table(results_to_show)

def respondents_per_country_component(results):
    """This component writes a bar chart showing number of Respondants per Country

    Arguments:
        results {[type]} -- A DataFrame of the Results
    """
    st.subheader("Respondents per Country")
    st.info(
        """You can plot using matplot, seaborn, vega lite, plotly and other.
    Here we have chosen plotly"""
    )
    distributions = (
        (results[["Country", "Respondent"]].groupby("Country").count().reset_index())
        .sort_values("Respondent")
        .tail(50)
    )
    fig = px.bar(
        distributions,
        x="Respondent",
        y="Country",
        title="Count",
        orientation="h",
        height=1000,
    )
    st.plotly_chart(fig, height=1000)

# The @st.cache annotation caches the dataframe
# so that it only takes time to read the first time.
@st.cache
def read_stack_overflow_results_2019() -> pd.DataFrame:
    """A dataframe of Stack Overflow Survey Results 2019

    Returns:
        pd.DataFrame -- A dataframe of Stack Overflow Surve Results 2019]
    """
    return stack_overflow.read_results()


# The @st.cache annotation caches the dataframe
# so that it only takes time to read the first time.
@st.cache
def read_stack_overflow_schema_2019() -> pd.DataFrame:
    """A dataframe containing the schema of the Stack Overflow Survey Results 2019

    Returns:
        pd.DataFrame -- A dataframe of the schema of the Stack Overflow Survey Results 2019
    """
    return stack_overflow.read_schema()


main()
