import pickle
import pandas as pd
import streamlit as st
from pycaret.regression import (
    setup as reg_setup,
    pull as reg_pull,
    compare_models as reg_compare_models,
    create_model as reg_create_model,
    tune_model as reg_tune_model,
    predict_model as reg_predict_model,
)
from pycaret.classification import (
    setup as clf_setup,
    pull as clf_pull,
    compare_models as clf_compare_models,
    create_model as clf_create_model,
    tune_model as clf_tune_model,
    predict_model as clf_predict_model,
)


def tune_model_wrapper(model, task_type):
    try:
        if task_type == "Regression":
            #     _ = reg_setup(dataset, target=target_column)
            # model = reg_create_model(model, verbose=True)
            _ = reg_tune_model(model, verbose=True)
        else:
            # _ = clf_setup(dataset, target=target_column)
            # model = clf_create_model(model, verbose=True)
            _ = clf_tune_model(model, verbose=True)
        return model
    except Exception as e:
        st.error(f"Error tuning model {model}: {e}")
    # else:
    # global data_editor_container
    # st.data_editor(model.get_params())


def create_model_wrapper(model, task_type):
    try:
        if task_type == "Regression":
            created_model = reg_create_model(model, verbose=True)
        else:
            created_model = clf_create_model(model, verbose=True)
        return created_model

    except Exception as e:
        st.error(f"Error creating {model}: {e}")


def compare_and_create_models(dataset, task_type, target_column, models_to_train):
    with st.spinner("Creating models, please wait..."):
        if task_type == "Regression":
            _ = reg_setup(dataset, target=target_column)
            compared_models = reg_compare_models(
                include=models_to_train,
                sort="RMSE",
                budget_time=2.0 if st.session_state["lightning_mode"] else None,
                n_select=9,
            )
        else:
            _ = clf_setup(dataset, target=target_column)
            compared_models = clf_compare_models(
                include=models_to_train,
                sort="Accuracy",
                budget_time=2.0 if st.session_state["lightning_mode"] else None,
                n_select=9,
            )

    if st.session_state["lightning_mode"]:
        created_models = [
            (
                create_model_wrapper(model, task_type),
                prediction_wrapper(model, task_type),
            )
            for model in compared_models
        ]
    else:
        created_models = [
            (
                tune_model_wrapper(create_model_wrapper(model, task_type), task_type),
                prediction_wrapper(model, task_type),
            )
            for model in compared_models
        ]
    # for model in compared_models:
    #     try:
    #         created_models.append((tune_model_wrapper(create_model_wrapper(model, task_type), task_type), prediction_wrapper(model, task_type)))
    #     except Exception as e:
    #         st.error(f"Error creating model {model}: {e}")

    return created_models


def grrrrr():
    st.toast("grrrrr")


def reset_model_state(model, data_editor_container):
    st.session_state[f"current_hyperparams_{model}"] = st.session_state[
        f"initial_hyperparams_{model}"
    ].copy()
    st.session_state[f"button_state_{model}"] = True
    data_editor_container.data_editor(
        st.session_state[f"current_hyperparams_{model}"], key=f"{model}_data_editor"
    )


def prediction_wrapper(model, task_type):
    try:
        if task_type == "Regression":
            reg_predict_model(model, verbose=True)
            output = reg_pull()
        else:
            clf_predict_model(model, verbose=True)
            output = clf_pull()

        return output

    except Exception as e:
        st.error(f"Error training model {model}: {e}")


# Function to train a custom model
def train_custom_model(model, task_type, hyperparams):
    try:
        # hyperparams = hyperparams.drop(columns=["random_state"])
        hyperparams = hyperparams.drop(columns=["random_state"])
        st.write(hyperparams)
        st.write(hyperparams.dtypes)

        model.set_params(**hyperparams.to_dict("records")[0])

        if task_type == "Regression":
            _ = reg_setup(model, verbose=True)
            model = reg_create_model(model, verbose=True)
        else:
            _ = clf_setup(model, verbose=True)
            model = clf_create_model(model, verbose=True)

        st.session_state[f"current_hyperparams_{model}"] = model.get_params()
        st.success(f"Model retrained: {model}")

        return model

    except Exception as e:
        st.error(f"Error training custom model {model}: {e}")


def main(created_models):
    with st.spinner("Creating models, please wait..."):
        for model, metrics in created_models:
            model_name = str(model).split("(")[0]

            if f"initial_hyperparams_{model}" not in st.session_state:
                st.session_state[f"initial_hyperparams_{model}"] = pd.DataFrame(
                    model.get_params(), index=["Values"]
                )
            if f"button_state_{model}" not in st.session_state:
                st.session_state[f"button_state_{model}"] = True

            with st.container(border=True):
                left, right = st.columns([3, 1])
                with left:
                    st.write(f"#### {model_name}")
                    st.caption("Hyperparameters")
                    hyperparams = pd.DataFrame(model.get_params(), index=["Values"])
                    data_editor_container = st.empty()
                    st.session_state[f"current_hyperparams_{model}"] = (
                        data_editor_container.data_editor(hyperparams)
                    )

                    # st.session_state[f"current_hyperparams_{model}"] = hyperparams.copy()
                    dataframes_equal = st.session_state[
                        f"current_hyperparams_{model}"
                    ].equals(
                        # hyperparams
                        st.session_state[f"initial_hyperparams_{model}"]
                    )
                    st.session_state[f"button_state_{model}"] = dataframes_equal

                    _1, _2, _3, _4 = st.columns(4)
                    temp_container = st.empty()

                    with _1:
                        download_simple = st.download_button(
                            f"Download Tuned Model",
                            pickle.dumps(model),
                            file_name=f"{model_name}_model.pkl",
                            key=f"{model}_download_simple_download_button",
                            use_container_width=True,
                        )
                    # with _2:
                    # tune_button = st.button(
                    #     "Tune Model",
                    #     use_container_width=True,
                    #     on_click=lambda: tune_model_wrapper(model, task_type, dataset, target_column),
                    #     key=f"{model}_tune_model"
                    # )
                    with _2:
                        train = st.button(
                            "Train Custom Model",
                            use_container_width=True,
                            # disabled=not st.session_state[f"button_state_{model}"],
                            # on_click=lambda: train_custom_model(model, task_type),
                            key=f"{model}_train",
                            disabled=True,
                        )

                        if train:
                            train_custom_model_response = train_custom_model(
                                model, task_type, hyperparams
                            )
                            temp_container.write(train_custom_model_response)
                    with _3:
                        download_custom = st.button(
                            "Download Custom Model",
                            use_container_width=True,
                            # disabled=st.session_state[f"button_state_{model}"],
                            # on_click=grrrrr,
                            key=f"{model}_download_custom",
                            disabled=True,
                        )

                    with _4:
                        reset_button = st.button(
                            "Reset Hyperparameters",
                            use_container_width=True,
                            key=f"{model}_reset_button",
                            disabled=True,
                        )
                        if reset_button:
                            reset_model_state(model, data_editor_container)

                    # with _4:
                    #     reset_button = st.button(
                    #         "Reset Hyperparameters",
                    #         use_container_width=True,
                    #         # disabled=st.session_state[f"button_state_{model}"],
                    #         # on_click=grrrrr,
                    #         key=f"{model}_reset_button",
                    #     )
                    #     if reset_button:
                    #         st.session_state[f"current_hyperparams_{model}"] = st.session_state[
                    #             f"initial_hyperparams_{model}"
                    #         ]
                    #         hyperparams = st.session_state[f"current_hyperparams_{model}"]
                    #         data_editor_container.empty()
                    #         data_editor_container.data_editor(hyperparams, key=f"{model}_data_editor")

                with right:
                    with st.container():
                        st.write("#### Metrics")
                        st.caption(f"Performance metrics for {model_name}")
                        st.dataframe(
                            metrics[
                                [
                                    i
                                    for i in metrics.columns
                                    if i not in ["RMSLE", "Model"]
                                ]
                            ],
                            hide_index=True,
                            use_container_width=True,
                        )
                        spinner_container = st.empty()
                        # st.write(st.session_state[f"button_state_{model}"])


if __name__ == "__main__":
    st.set_page_config(page_title="Model Tuning", page_icon="🔨", layout="wide")

    target_column = "Age (Years)"
    models_to_train = ["svm", "dt", "ada", "gbr"]
    task_type = "Regression"
    dataset = pd.read_csv("static/data/cats_dataset.csv")

    if "created_models" not in st.session_state:
        st.session_state.created_models = compare_and_create_models(
            dataset, task_type, target_column, models_to_train
        )

    created_models = st.session_state.created_models
    main(created_models)
