from functools import lru_cache
from typing import List, Optional

import IPython.display as ip
import ipywidgets as widgets
import pandas as pd
import qgrid
from markdown import markdown
from plotly import express as px
import plotly.graph_objects as go
import styles
from awesome_analytics_apps import stack_overflow

IPYTHON_DISPLAY_DOCS = (
    "https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html"
)
IPYWIDGETS_DOCS = (
    "https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html"
)

QGRID_DOCS = "https://qgrid.readthedocs.io/en/latest/index.html"


def main():
    configure()

    app_layout = widgets.AppLayout(
        header=get_header(),
        left_sidebar=get_sidebar(),
        center=get_center(),
        right=widgets.VBox(),
        pane_widths=[2, 6, 1],
        pane_heights=["75px", 1, "75px"],
    )

    ip.display(app_layout)


def get_header():
    header = widgets.HTML(
        markdown("# Awesome Analytics Apps in Voila"),
        layout=widgets.Layout(height="100px"),
    )
    header.style.text_align = "center"
    return header


def get_sidebar():
    return widgets.HTML(
        markdown(
            f"""## Resources

- [IPython display Docs]({IPYTHON_DISPLAY_DOCS})
- [IPy Widgets Docs]({IPYWIDGETS_DOCS})
- [QGrid Docs]({QGRID_DOCS})
    """
        )
    )


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


def get_center():
    items = [get_resources(), get_stack_overflow()]
    return to_output_widget(items)
    # widgets.VBox((get_resources(), get_stack_overflow()))


def get_resources():
    items = [
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
    ]
    return to_output_widget(items)


def to_output_widget(items) -> widgets.Widget:
    out = widgets.Output()
    with out:
        for item in items:
            ip.display(item)
    return out


def run_all_code_below(input):
    ip.display(ip.Javascript("IPython.notebook.execute_cells_below()"))


def run_all_code_below_button():
    button = widgets.Button(description="Re-run code")
    button.on_click(run_all_code_below)
    ip.display(button)


@lru_cache(maxsize=2)
def get_data():
    return stack_overflow.read_schema(), stack_overflow.read_results()


def get_stack_overflow():
    """The Stack Overflow compontent writes the Questions, Results and a Distribution"""
    schema, results = get_data()

    questions_grid = stack_overflow_questions_grid(schema)
    items = [
        get_stack_overflow_intro(),
        ip.Markdown("""## Stack Overflow Questions 2019"""),
        questions_grid,
        ip.Markdown("## Stack Overflow Results 2019"),
        stack_overflow_results_grid(results, questions_grid),
        respondents_per_country_component(results),
    ]

    return to_output_widget(items)


def get_stack_overflow_intro():
    items = [
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
    ]
    return to_output_widget(items)


def stack_overflow_questions_grid(schema: pd.DataFrame) -> qgrid.QGridWidget:
    """This component writes the Stack Overflow Developer Questions

    Arguments:
        schema {pd.DataFrame} -- A DataFrame of questions

    Returns:
        qgrid.QGridWidget -- Returns the QGridWidget Grid used to show the questions.
        Can be used to filter answers later on.
    """
    questions_grid = qgrid.show_grid(
        schema,
        column_options=styles.RESULTS_GRID_COL_OPTIONS,
        column_definitions=styles.RESULTS_GRID_COL_DEFS,
    )
    # We select something so that some Answers are shown
    questions_grid.change_selection(rows=[0, 1])
    return questions_grid


def stack_overflow_results_grid(
    results, questions_grid: qgrid.QGridWidget
) -> widgets.Widget:
    """This component writes the Stack Overflow Developer Survey Questions

    Arguments:
        results {[type]} -- A DataFrame of the Results
        questions_grid {qgrid.QGridWidget} -- The table of questions
    """

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

    return to_output_widget([no_results_grid, results_grid])


def respondents_per_country_component(results):
    """This component writes a bar chart showing number of Respondants per Country

    Arguments:
        results {[type]} -- A DataFrame of the Results
    """
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
        width=1200,
    )
    return to_output_widget(
        [
            ip.Markdown(
                """### Respondents per Countrys
You can plot using matplot, seaborn, vega lite, plotly and other. Here we have chosen plotly
            """
            ),
            go.FigureWidget(fig),
        ]
    )


if __name__ == "__main__":
    main()
