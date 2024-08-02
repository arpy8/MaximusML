import pandas as pd
import streamlit as st
import plotly.express as px


def init_app():
    st.set_page_config(
        page_title="Maximus ML", layout="wide", page_icon=":material/construction:"
    )

    st.write(
        """
    <style>
    .plot-container {
        border: red !important;
        z-index: -1000; !important;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if "uploaded_file" not in st.session_state:
        st.session_state["uploaded_file"] = None

    if "dataset_description" not in st.session_state:
        st.session_state["dataset_description"] = {
            "rows": None,
            "columns": None,
            "missing_values": None,
            "memory_size": None,
            "file_format": None,
        }

    if "dataset" not in st.session_state:
        st.session_state["dataset"] = pd.DataFrame()
    if "handle_null_values" not in st.session_state:
        st.session_state["handle_null_values"] = None
    if "normalize_data" not in st.session_state:
        st.session_state["normalize_data"] = None
    if "train_test_split" not in st.session_state:
        st.session_state["train_test_split"] = None
    if "new_data" not in st.session_state:
        st.session_state["new_data"] = None
    if "task_type" not in st.session_state:
        st.session_state["task_type"] = "Regression"
    if "models_to_train" not in st.session_state:
        st.session_state["models_to_train"] = None
    if "final_dataset" not in st.session_state:
        st.session_state["final_dataset"] = None
    if "training_results" not in st.session_state:
        st.session_state["training_results"] = None
    if "ingest_data_button" not in st.session_state:
        st.session_state["ingest_data_button"] = False
    if "normalization_type" not in st.session_state:
        st.session_state["normalization_type"] = False
    if "lightning_mode" not in st.session_state:
        st.session_state["lightning_mode"] = False
    if "updated_data" not in st.session_state:
        st.session_state["updated_data"] = None


def load_data(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(".xls"):
        data = pd.read_excel(uploaded_file)
    else:
        data = pd.DataFrame()

    data.to_csv("output/temp.csv")
    return data


def display_data(data, height=180):
    if not data.empty:
        st.dataframe(data, height=height)


def display_description(data, uploaded_file):
    with st.container(border=True):
        left, right = st.columns(2)

        with left:
            st.write(
                f"""
                :gray[Row:] {data.shape[0]} <br>
                :gray[File Format:] {uploaded_file.name.split('.')[-1] if uploaded_file.name.split('.')[-1]!=None else "Unknown"} <br>
                :gray[Has Duplicates:] {bool(data.duplicated().sum().sum())}
            """,
                unsafe_allow_html=True,
            )

        with right:
            st.write(
                f"""
                :gray[Columns:] {data.shape[1]} <br>
                :gray[Memory Size:] {data.memory_usage(deep=True).sum()} bytes <br>
                :gray[Missing Values:] {bool(data.isnull().sum().sum())}
            """,
                unsafe_allow_html=True,
            )


def padding(n=1):
    st.write("<br>" * n, unsafe_allow_html=True)


def plot_graph(train_split):
    data = {
        "category": ["Test Split", "Train Split"],
        "values": [train_split, 1 - train_split],
    }

    fig = px.pie(
        data,
        names="category",
        values="values",
        color_discrete_sequence=["#272727", "#6d6d6e"],
    )
    fig.update_layout(
        height=60,
        width=60,
        margin=dict(t=10, b=0, l=0, r=70),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    fig.update_traces(textinfo="none", hoverinfo="none")

    return fig
