import streamlit as st
import awesome_analytics_apps.stack_overflow
import pandas as pd


def main():
    st.title("Awesome Analytics Apps in Streamlit")

    st.header("Introduction")
    st.markdown(
        """\
        The ***4 minutes introduction*** to Streamlit"""
    )
    st.video(data="https://www.youtube.com/watch?v=B2iAodr0fOo")

    st.header("Resources")
    st.markdown(
        """\
    - [Docs](https://streamlit.io/docs/)
    - [awesome-streamlit.org](http://awesome-streamlit.org/)
    """
    )

    st.header("Stack Overflow 2019")

    # st.markdown(![Stack Overflow 2019 Image])
    st.subheader("Stack Overflow Schema 2019")
    schema = read_stack_overflow_schema_2019()
    schema_table = st.empty()
    number_of_schema_rows = st.slider(
        "Select number of rows to show", min_value=0, max_value=len(schema), value=10
    )
    schema_table.table(schema.head(number_of_schema_rows))

    st.subheader("Results 2019")
    results = read_stack_overflow_results_2019()
    number_of_rows_to_show = st.selectbox(
        "Select number of rows to show",
        options=[5, 50, 500, 5000, len(results)],
        index=1,
    )
    st.dataframe(results.head(number_of_rows_to_show))


# The @st.cache annotation caches the dataframe so that it only takes time to read the first time.
@st.cache
def read_stack_overflow_results_2019() -> pd.DataFrame:
    """A dataframe of Stack Overflow Survey Results 2019

    Returns:
        pd.DataFrame -- A dataframe of Stack Overflow Surve Results 2019]
    """
    return awesome_analytics_apps.stack_overflow.read_results()


@st.cache
def read_stack_overflow_schema_2019() -> pd.DataFrame:
    """A dataframe containing the schema of the Stack Overflow Survey Results 2019

    Returns:
        pd.DataFrame -- A dataframe of the schema of the Stack Overflow Survey Results 2019
    """
    return awesome_analytics_apps.stack_overflow.read_schema()


main()
