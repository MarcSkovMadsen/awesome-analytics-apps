import IPython.display as ip
import ipywidgets as widgets

MAX_WIDTH = 2000
RESULTS_GRID_COL_OPTIONS = {"width": 200, "maxWidth": 500}
RESULTS_GRID_COL_DEFS = {
    "index": {"width": 50},
    "QuestionText": {"width": 300},
    "Respondent": {"width": 120},
    "MainBranch": {"width": 200},
}


def layout_app(header, sidebar, main_, footer):
    header_area = widgets.HBox(
        children=header,
        layout=widgets.Layout(
            width="auto", grid_area="header", justify_content="center"
        ),
    )
    sidebar_area = widgets.HBox(
        children=sidebar, layout=widgets.Layout(width="auto", grid_area="sidebar")
    )
    main_area = widgets.HBox(
        children=main_, layout=widgets.Layout(width="auto", grid_area="main")
    )
    footer_area = widgets.HBox(
        children=footer,
        layout=widgets.Layout(
            width="auto", grid_area="footer", justify_content="center"
        ),
    )

    page = widgets.GridBox(
        children=[header_area, main_area, sidebar_area, footer_area],
        layout=widgets.Layout(
            width="95%",
            grid_template_rows="auto auto auto",
            grid_template_columns="25% 25% 25% 25%",
            grid_template_areas="""
                "header header header header"
                "sidebar main main main "
                "footer footer footer footer"
                """,
        ),
    )
    ip.display(page)
