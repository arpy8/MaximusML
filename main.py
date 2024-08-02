import pandas as pd
import streamlit as st

from constant import ML_MODELS
from utils import init_app, padding
from sections import (
    data_ingestion,
    data_transformation,
    train_model_section,
    display_results,
)


def main():
    init_app()
    _1, _, logo = st.columns([1, 5, 1])

    with _1:
        st.session_state["lightning_mode"] = st.checkbox(
            "Lightning Mode",
            value=False,
            help="Enables faster model training by ignoring hefty models and assigning budget time to each model.",
        )
    with logo:
        st.image("static/images/logo.png")

    ingestion, tranformation, train = st.columns(3)
    temp_container = st.empty()

    with ingestion:
        with st.container(border=True):
            st.write(
                "<h4 style='color:#fff;font-weight:10px;padding-y:10px'>Data Ingestion</h4>",
                unsafe_allow_html=True,
            )
            data_ingestion()

    with tranformation:
        with st.container(border=True):
            st.write(
                "<h4 style='color:#fff;font-weight:10px;padding-y:10px'>Data Transformation</h4>",
                unsafe_allow_html=True,
            )

            if not st.session_state["dataset"].empty:
                data_transformation()
            else:
                st.caption("Please upload a dataset to proceed.")
                padding(5)
                with st.columns([1, 1, 6.8])[-1]:
                    st.image("static/images/2.png")
    with train:
        global created_models
        with st.container(border=True):
            st.write(
                "<h4 style='color:#fff;font-weight:10px;padding-y:10px'>Train Model</h4>",
                unsafe_allow_html=True,
            )

            if (
                not st.session_state["dataset"].empty
                or st.session_state["training_results"]
            ):
                try:
                    created_models = train_model_section()
                    if created_models is not None:
                        with temp_container.container(border=True):
                            # st.write(created_models)
                            display_results(created_models)

                        st.toast("Kindly scroll down to see the results.")
                        st.write(":green[Kindly scroll down to see the results.]")

                except Exception as e:
                    st.error(e)
            else:
                st.caption("Please upload a dataset to proceed.")
                padding(5)
                with st.columns([1, 1, 6.8])[-1]:
                    st.image("static/images/3.png")

    if st.session_state["training_results"] is not None:
        display_results(created_models)

    if st.session_state["training_results"] is not None:
        with st.container(border=True):
            with st.columns(2)[0]:
                st.dataframe(
                    st.session_state["training_results"], use_container_width=True
                )


if __name__ == "__main__":
    main()
