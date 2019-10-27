import IPython.display as ip
import ipywidgets as widgets
import pandas as pd
import qgrid
from awesome_analytics_apps import stack_overflow
from typing import Optional, List
import qgrid
import styles
from plotly import express as px
from markdown import markdown

IPYTHON_DISPLAY_DOCS = (
    "https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html"
)
IPYWIDGETS_DOCS = (
    "https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html"
)

QGRID_DOCS = "https://qgrid.readthedocs.io/en/latest/index.html"


def main():
    configure()

    header_area = [widgets.HTML(markdown("# Awesome Analytics Apps in Voila"))]
    sidebar_area = [
        widgets.HTML(
            markdown(
                f"""
## Resources

- [IPython display Docs]({IPYTHON_DISPLAY_DOCS})
- [IPy Widgets Docs]({IPYWIDGETS_DOCS})
- [QGrid Docs]({QGRID_DOCS})
"""
            )
        )
    ]
    ip.display(*header_area)
    ip.display(*sidebar_area)

    ip.display(
        ip.Markdown(
            """## Introduction

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
        ip.Markdown("For more info watch the ***30 minutes introduction*** to Voila"),
        ip.YouTubeVideo("VtchVpoSdoQ"),
    )

    schema = stack_overflow.read_schema()
    results = stack_overflow.read_results()

    stack_overflow_component(schema, results)

    # layout_page(header_area, sidebar_area, main_area, footer_area)


def configure():
    pd.set_option("display.max_columns", 1000)  # or 1000
    pd.set_option("display.max_rows", 100)  # or 1000
    pd.set_option("display.max_colwidth", -1)

    # Todo: Change 1000 to styles.MAX_WIDTH
    ip.display(
        ip.HTML(
            """
    <style type="text/css">
    .q-grid-container {
        max-width: 1000 px;
    }
    </style>
    """
        )
    )


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
<img src="{stack_overflow.IMAGE_2019_URL}"style="height=300px;">
</a>

Results: [{stack_overflow.SURVEY_2019_URL}]({stack_overflow.DATA_URL})

Data: [{stack_overflow.DATA_URL}]({stack_overflow.DATA_URL})
"""
        )
    )

    questions_grid = stack_overflow_questions_component(schema)
    stack_overflow_answers_component(results, questions_grid)
    respondents_per_country_component(results)


def stack_overflow_questions_component(schema: pd.DataFrame) -> qgrid.QGridWidget:
    """This component writes the Stack Overflow Developer Questions

    Arguments:
        schema {pd.DataFrame} -- A DataFrame of questions

    Returns:
        qgrid.QGridWidget -- Returns the QGridWidget Grid used to show the questions.
        Can be used to filter answers later on.
    """
    ip.display(
        ip.Markdown(
            """\
# Stack Overflow Questions 2019


"""
        )
    )
    questions_grid = qgrid.show_grid(
        schema,
        column_options=styles.RESULTS_GRID_COL_OPTIONS,
        column_definitions=styles.RESULTS_GRID_COL_DEFS,
    )
    # We select something so that some Answers are shown
    questions_grid.change_selection(rows=[0, 1])
    ip.display(questions_grid)
    return questions_grid


def stack_overflow_answers_component(results, questions_grid: qgrid.QGridWidget):
    """This component writes the Stack Overflow Developer Survey Questions

    Arguments:
        results {[type]} -- A DataFrame of the Results
        questions_grid {qgrid.QGridWidget} -- The table of questions
    """

    ip.display(ip.Markdown("# Stack Overflow Results 2019"))

    def get_selected_questions(questions_grid):
        return list(questions_grid.get_selected_df()["Column"])

    results_grid = qgrid.show_grid(
        results[get_selected_questions(questions_grid)].head(10),
        column_options=styles.RESULTS_GRID_COL_OPTIONS,
        column_definitions=styles.RESULTS_GRID_COL_DEFS,
    )
    no_results_grid = ip.Markdown(
        "**Select one or more questions in the table above to show the results!**"
    )

    def update_results_grid():
        selected_questions = list(questions_grid.get_selected_df()["Column"])
        if selected_questions:
            results_to_show = results
            results_to_show = results_to_show[selected_questions]
            results_grid.df = results_to_show
        else:
            results_grid.df = pd.DataFrame()

    def questions_grid_handler(change):
        update_results_grid()

    questions_grid.observe(handler=questions_grid_handler, names="_selected_rows")

    ip.display(no_results_grid)
    ip.display(results_grid)


def respondents_per_country_component(results):
    """This component writes a bar chart showing number of Respondants per Country

    Arguments:
        results {[type]} -- A DataFrame of the Results
    """
    ip.display(
        ip.Markdown(
            """### Respondents per Countrys

You can plot using matplot, seaborn, vega lite, plotly and other. Here we have chosen plotly
"""
        )
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
        width=styles.MAX_WIDTH,
    )
    ip.display(fig)


if __name__ == "__main__":
    main()
