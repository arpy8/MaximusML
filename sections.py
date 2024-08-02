import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

from constant import ML_MODELS
from train_model import compare_and_create_models, main as display_results
from utils import load_data, display_data, display_description, padding, plot_graph

from pycaret.regression import setup as reg_setup
from pycaret.classification import setup as clf_setup


def data_ingestion():
    uploaded_file = st.file_uploader(
        "Please upload a dataset", type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        st.session_state["uploaded_file"] = uploaded_file
        data = load_data(uploaded_file)
        display_data(data)
        display_description(data, uploaded_file)
        st.session_state["dataset"] = data

        st.session_state["dataset_description"] = {
            "rows": data.shape[0],
            "columns": data.shape[1],
            "missing_values": bool(data.isnull().sum().sum()),
            "memory_size": data.memory_usage(deep=True).sum(),
            "file_format": uploaded_file.name.split(".")[-1],
        }
    else:
        st.caption("Please upload a dataset to proceed.")
        padding()
        with st.columns([1, 1, 6.8])[-1]:
            st.image("static/images/1.png")


def data_transformation():
    global new_data

    new_data = st.session_state["dataset"]
    st.session_state["extra_columns"] = st.multiselect(
        label="Select Columns to Drop",
        options=new_data.columns,
        placeholder="Select extra columns to drop",
    )
    if st.session_state["extra_columns"] is not None:
        st.session_state["new_data"] = new_data.drop(
            st.session_state["extra_columns"], axis=1
        )
        # new_data = data.drop(st.session_state["extra_columns"], axis=1)
        # st.session_state["new_data"] = new_data

    with st.expander("Encode Columns", expanded=False, icon=":material/pin:"):
        st.session_state["encode_columns"] = st.selectbox(
            label="Select Columns to Encode",
            options=[
                "None",
                *[
                    i
                    for i in new_data.columns
                    if i not in st.session_state["extra_columns"]
                ],
            ],
            placeholder="Select column to encode",
        )
        st.session_state["encoding_type"] = st.radio(
            "Type of Encoding",
            ["Label Encoding", "One-Hot Encoding"],
            horizontal=True,
            disabled=not bool(st.session_state["encode_columns"]),
        )

        if st.session_state["encode_columns"] != "None" and st.button(
            "Encode Data", use_container_width=True
        ):
            encode_column = st.session_state["encode_columns"]
            if st.session_state["encoding_type"] == "Label Encoding":
                encoder = LabelEncoder()
                new_data[encode_column] = encoder.fit_transform(new_data[encode_column])
            else:
                encoder = OneHotEncoder(sparse_output=False)
                encoded_data = encoder.fit_transform(new_data[[encode_column]])
                encoded_df = pd.DataFrame(
                    encoded_data,
                    columns=[
                        f"{encode_column}_{cat}" for cat in encoder.categories_[0]
                    ],
                )
                new_data = new_data.drop(encode_column, axis=1)
                new_data = pd.concat([new_data, encoded_df], axis=1)
                st.session_state["new_data"] = new_data

    with st.expander(
        "Handle Missing Values", expanded=False, icon=":material/category:"
    ):
        st.session_state["numeric_imputation"] = st.selectbox(
            "Numeric Imputation Type", ["Mean", "Median", "Mode"]
        )
        st.session_state["categorical_imputation"] = st.selectbox(
            "Categorical Imputation Type", ["Mode", "Drop"]
        )
        st.caption(
            "Note: Imputation Changes may not be reflected in the above dataset preview, but will be reflected in the final dataset."
        )

    with st.expander("Data Normalization", expanded=False, icon=":material/bar_chart:"):
        st.session_state["normalization_type"] = st.selectbox(
            "Normalization Type", ["None", "MinMax", "Standardization"]
        )

    _1, _2 = st.columns([2, 1])
    with _1:
        with st.expander("Advanced Settings", expanded=False, icon=":material/build:"):
            st.session_state["handle_duplicate_values"] = st.checkbox(
                "Drop Duplicate Values", value=True
            )
            # st.session_state["normalize_data"] = st.checkbox(
            #     "Normalize Data", value=True
            # )
            st.session_state["remove_outliers"] = st.checkbox(
                "Remove Outliers", value=True
            )

    with _2:
        transform_data_button = st.button("Transform Data", use_container_width=True)

    if (
        transform_data_button and st.session_state["dataset"] is not None
    ) or st.session_state["updated_data"]:
        st.session_state["new_data"] = new_data.drop(
            st.session_state["extra_columns"], axis=1
        )
        if st.session_state["handle_duplicate_values"]:
            st.session_state["new_data"] = new_data.drop_duplicates()
        new_data = st.session_state["new_data"]

        print("New data before transformation:")
        print(new_data.head())

        for i in range(len(new_data.columns)):
            try:
                new_data = new_data.drop(st.session_state["extra_columns"], axis=1)
                _, new_data = reg_setup(
                    data=new_data,
                    target=new_data.iloc[:, i],
                    normalize=st.session_state["normalize_data"],  # bool
                    remove_outliers=st.session_state["remove_outliers"],  # bool
                    numeric_imputation=st.session_state["numeric_imputation"],  # string
                    categorical_imputation=st.session_state[
                        "categorical_imputation"
                    ],  # string
                )
                print("New data afte    r transformation:")
                print(new_data.head())

                st.session_state["updated_data"] = True
                if st.session_state["new_data"] is not None:
                    st.caption("Updated Data Description:")
                    display_data(new_data.head(10), height=100)
                break
            except Exception as e:
                print(f"Exception occurred: {e}")
                continue
    elif not transform_data_button and not st.session_state["updated_data"]:
        st.caption("No transformations applied.")
        display_data(st.session_state["dataset"], height=100)


def train_model_section():
    st.session_state["task_type"] = st.radio(
        "Type of Task",
        ["Regression", "Classification"],
        horizontal=True,
    )
    st.session_state["target_column"] = st.selectbox(
        label="Select Target Column",
        options=[
            i
            for i in st.session_state["new_data"].columns
            if i not in st.session_state["extra_columns"]
        ],
        placeholder="Select target column",
    )

    _1, _2 = st.columns([3, 1])
    # with _1:
    st.session_state["train_split_perc"] = st.slider("Train Split", 0.0, 1.0, 0.7)
    # with _2:
    #     chart = plot_graph(train_split_perc)
    #     st.plotly_chart(chart, use_container_width=True)
    # test_split_perc = st.slider(
    #     "Test Split", 0.0, 1.0, abs(1.0 - train_split_perc), disabled=True
    # )

    if st.session_state["train_split_perc"] < 0.5:
        st.toast("Train Split should be greater than Test Split")

    # st.write("Models to be trained")
    left, right = st.columns(2)

    with left:
        svm = "svm" if st.checkbox("Support Vector Machine", value=True) else None
        ada = "ada" if st.checkbox("AdaBoost", value=True) else None
        rf = (
            "rf"
            if st.checkbox(
                "Random Forest",
                value=False,
                disabled=st.session_state["lightning_mode"],
            )
            else None
        )
        # xgb = st.checkbox("XGBoost", value=True) else None

    with right:
        gbr = "gbr" if st.checkbox("Gradient Boosting", value=True) else None
        dt = "dt" if st.checkbox("Decision Tree", value=True) else None
        mlp = (
            "mlp"
            if st.checkbox(
                "Multi Layer Perceptron",
                value=False,
                disabled=st.session_state["lightning_mode"],
            )
            else None
        )
        # dt = st.checkbox("Stacking Algorithm", value=True)

    if not any([svm, rf, ada, gbr, mlp, dt]):
        st.toast("Please upload a dataset to proceed.", icon="🛈")
    # else:
    #     padding()

    models_to_train = [i for i in [svm, rf, ada, gbr, mlp, dt] if i]
    if models_to_train:
        st.session_state["models_to_train"] = models_to_train

    train_model_button = st.button(
        "Train Model", use_container_width=True, disabled=not bool(models_to_train)
    )

    if train_model_button and st.session_state["dataset"] is None:
        st.toast("Please upload a dataset to proceed.", icon="🛈")

    if (
        train_model_button and st.session_state["dataset"] is not None
        # and st.session_state["models_to_train"] is not None
    ):
        if st.session_state["dataset"] is None:
            st.write("Error fetching the dataset.")

        else:
            try:
                created_models = compare_and_create_models(
                    st.session_state["new_data"],
                    st.session_state["task_type"],
                    st.session_state["target_column"],
                    st.session_state["models_to_train"],
                )

                st.session_state["created_models"] = created_models

                # st.write(created_models)
                return created_models
            except ValueError:
                st.toast("Try selecting the other task type.")
            except Exception as e:
                st.error(e)
    if not train_model_button:
        st.caption("Please select the task type and target column.")
        # padding()
