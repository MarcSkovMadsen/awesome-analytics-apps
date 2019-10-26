# Awesome Analytics Apps

A repository for sharing knowledge and resources on awesome analytics apps in Python.

I've started this project because there are a lot of emerging frameworks for creating awesome analytics apps in Python. These are

- [Bokeh](https://docs.bokeh.org/en/latest/index.html)
- [Dash](https://plot.ly/dash/)
- [Django-Dash](https://pypi.org/project/django-plotly-dash/)
- [Panel](https://panel.pyviz.org/)
- [Streamlit](https://streamlit.io)
- [Voila](https://github.com/voila-dashboards/voila)

And I wan't to share knowledge and the why, what, when and how of each because they are so awesome but different.

## Getting Started with this Repository

### Prerequisites

- An Operating System like Windows, OsX or Linux
- A working [Python](https://www.python.org/) installation.
  - We recommend using 64bit Python 3.7.4.
- a Shell
  - We recommend [Git Bash](https://git-scm.com/downloads) for Windows 8.1
  - We recommend [wsl](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux) for For Windows 10
- an Editor
  - We recommend [VS Code](https://code.visualstudio.com/) (Preferred) or [PyCharm](https://www.jetbrains.com/pycharm/).
- The [Git cli](https://git-scm.com/downloads)

### Installation

Clone the repo

```bash
git clone https://github.com/MarcSkovMadsen/awesome-analytics-apps.git
```

cd into the project root folder

```bash
cd awesome-analytics-apps-in-python
```

Then you should create a virtual environment named .venv

```bash
python -m venv .venv
```

and activate the environment.

On Linux, OsX or in a Windows Git Bash terminal it's

```bash
source .venv/Scripts/activate
```

or alternatively

```bash
source .venv/bin/activate
```

In a Windows terminal it's

```bash
.venv/Scripts/activate.bat
```

Then you should install the local requirements

```bash
pip install -r requirements_local.txt
```

### Build and run the Applications Locally

```bash
streamlit run streamlit/app.py
```

or as a Docker container via

```bash
invoke docker.build --rebuild
invoke docker.run-server
```
