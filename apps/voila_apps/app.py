import IPython.display as ip
import ipywidgets as widgets
import pandas as pd
import qgrid
from awesome_analytics_apps import stack_overflow
from typing import Optional, List
import qgrid

IPYTHON_DISPLAY_DOCS = (
    "https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html"
)
IPYTHON_WIDGETS_DOCS = (
    "https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html"
)


def main():
    configure_pandas()
    ip.display(
        ip.Markdown(
            """# Awesome Analytics Apps in Jupyter Voila

## Introduction

You can use Python and Streamlit as shown in the code below to create a web app!
"""
        ),
        # Use https://gist.github.com/jiffyclub/5385501 to format code
        ip.Code(
            """
ip.display(
    ip.Markdown(
    "For more info watch the ***4 minutes introduction*** to Streamlit"
    ),
    ip.YouTubeVideo("VtchVpoSdoQ")
)
""",
            language="python3",
        ),
        ip.Markdown(
            "For more info watch the ***30 minutes introduction*** to Streamlit"
        ),
        ip.YouTubeVideo("VtchVpoSdoQ"),
    )

    schema = stack_overflow.read_schema()
    results = stack_overflow.read_results()

    stack_overflow_component(schema, results)


def configure_pandas():
    pd.set_option("display.max_columns", 1000)  # or 1000
    pd.set_option("display.max_rows", 100)  # or 1000
    pd.set_option("display.max_colwidth", -1)


def run_all_code_below(input):
    ip.display(ip.Javascript("IPython.notebook.execute_cells_below()"))


def run_all_code_below_button():
    button = widgets.Button(description="Re-run code")
    button.on_click(run_all_code_below)
    ip.display(button)


def stack_overflow_component(schema: pd.DataFrame, results: pd.DataFrame):
    """The Stack Overflow compontent writes the Questions, Results and a Distribution"""
    ip.display(
        ip.Markdown(
            f"""
## Stack Overflow 2019

You will be analyzing and providing insights from the Stack Overflow 2019 survey

<a href="{stack_overflow.SURVEY_2019_URL}" target="_blank">
<img src="{stack_overflow.IMAGE_2019_URL}"style="width:100%;">
</a>

Results: [{stack_overflow.SURVEY_2019_URL}]({stack_overflow.DATA_URL})

Data: [{stack_overflow.DATA_URL}]({stack_overflow.DATA_URL})
"""
        )
    )

    questions = stack_overflow_questions_component(schema)
    stack_overflow_answers_component(results, questions)


def stack_overflow_questions_component(schema: pd.DataFrame) -> widgets.SelectMultiple:
    """This component writes the Stack Overflow Developer Questions and returns a selected list of
    questions

    Arguments:
        schema {pd.DataFrame} -- A DataFrame of questions

    Returns:
        Optional[List[str]] -- [description]
    """
    ip.display(
        ip.Markdown(
            """\
# Stack Overflow Questions 2019


"""
        )
    )

    def show_questions(selected_questions, number_of_rows=10):
        schema_to_show = schema
        if selected_questions:
            schema_to_show = schema_to_show[
                schema_to_show["Column"].isin(selected_questions)
            ]
        schema_to_show = schema_to_show.head(number_of_rows)
        ip.display(qgrid.show_grid(schema_to_show))

    questions = widgets.SelectMultiple(
        options=sorted(schema["Column"].unique()),
        value=[],
        rows=10,
        description="Select questions",
        disabled=False,
    )
    questions_number_of_rows = widgets.RadioButtons(
        options=(10, 85), value=10, description="Select # of Questions", disabled=False
    )
    widgets.interact(
        show_questions,
        selected_questions=questions,
        number_of_rows=questions_number_of_rows,
    )

    return questions


def stack_overflow_answers_component(
    results, selected_questions: widgets.SelectMultiple
):
    """This component writes the Stack Overflow Developer Survey Questions

    Arguments:
        results {[type]} -- A DataFrame of the Results
        selected_questions {Optional[List[str]]} -- a list of questions to filter
    """

    ip.display(ip.Markdown("# Stack Overflow Results 2019"))
    out = widgets.Output()

    def h(number_of_rows_to_show: int, selected_questions: List[str]):
        results_to_show = results
        if selected_questions:
            results_to_show = results_to_show[selected_questions]
        results_to_show = results_to_show.head(number_of_rows_to_show)

        with out:
            ip.clear_output()
            ip.display(qgrid.show_grid(results_to_show))

    number_of_rows_to_show_widget = widgets.Dropdown(
        description="Select # Answers to show",
        options=[10, 50, 500, 5000, len(results)],
        value=10,
    )

    def f(number_of_rows_to_show):
        h(number_of_rows_to_show, list(selected_questions.value))

    widgets.interact(f, number_of_rows_to_show=number_of_rows_to_show_widget)

    def g(change):
        h(number_of_rows_to_show_widget.value, list(change["new"]))

    selected_questions.observe(handler=g, names="value")
    ip.display(out)


if __name__ == "__main__":
    main()
