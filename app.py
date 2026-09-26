# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import os


# # ============================================================
# # PAGE CONFIGURATION
# # ============================================================

# st.set_page_config(
#     page_title="Network Anomaly Detector",
#     page_icon="🛡️",
#     layout="wide"
# )


# # ============================================================
# # CUSTOM CSS
# # ============================================================

# st.markdown("""
# <style>

#     .main {
#         background-color: #0b1120;
#     }

#     .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#     }

#     .title {
#         font-size: 42px;
#         font-weight: 700;
#         color: #ffffff;
#         margin-bottom: 5px;
#     }

#     .subtitle {
#         font-size: 17px;
#         color: #94a3b8;
#         margin-bottom: 30px;
#     }

#     .metric-card {
#         background: #111827;
#         border: 1px solid #1e293b;
#         border-radius: 15px;
#         padding: 20px;
#         text-align: center;
#     }

#     .metric-title {
#         color: #94a3b8;
#         font-size: 14px;
#     }

#     .metric-value {
#         color: #ffffff;
#         font-size: 30px;
#         font-weight: 700;
#     }

#     .section-title {
#         color: #ffffff;
#         font-size: 24px;
#         font-weight: 600;
#         margin-top: 30px;
#         margin-bottom: 15px;
#     }

# </style>
# """, unsafe_allow_html=True)


# # ============================================================
# # HEADER
# # ============================================================

# st.markdown(
#     '<div class="title">🛡️ Network Anomaly Detector</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">'
#     'UNSW-NB15 • Unsupervised Learning • Isolation Forest'
#     '</div>',
#     unsafe_allow_html=True
# )


# # ============================================================
# # LOAD RESULTS
# # ============================================================

# results_path = "results/anomaly_results.csv"

# if not os.path.exists(results_path):

#     st.error(
#         "Results file not found. "
#         "Run anomaly_detection.py first."
#     )

#     st.stop()


# results = pd.read_csv(results_path)


# # ============================================================
# # BASIC STATISTICS
# # ============================================================

# total_records = len(results)

# normal_count = (
#     results["prediction"] == 0
# ).sum()

# anomaly_count = (
#     results["prediction"] == 1
# ).sum()

# anomaly_percentage = (
#     anomaly_count / total_records
# ) * 100


# # ============================================================
# # METRIC CARDS
# # ============================================================

# col1, col2, col3, col4 = st.columns(4)


# with col1:

#     st.markdown(
#         f"""
#         <div class="metric-card">
#             <div class="metric-title">TOTAL TRAFFIC</div>
#             <div class="metric-value">{total_records:,}</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# with col2:

#     st.markdown(
#         f"""
#         <div class="metric-card">
#             <div class="metric-title">NORMAL TRAFFIC</div>
#             <div class="metric-value">{normal_count:,}</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# with col3:

#     st.markdown(
#         f"""
#         <div class="metric-card">
#             <div class="metric-title">ANOMALIES</div>
#             <div class="metric-value">{anomaly_count:,}</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# with col4:

#     st.markdown(
#         f"""
#         <div class="metric-card">
#             <div class="metric-title">ANOMALY RATE</div>
#             <div class="metric-value">{anomaly_percentage:.1f}%</div>
#         </div>
#         """,
#         unsafe_allow_html=True
#     )


# # ============================================================
# # MODEL PERFORMANCE
# # ============================================================

# st.markdown(
#     '<div class="section-title">📊 Model Performance</div>',
#     unsafe_allow_html=True
# )

# col1, col2, col3 = st.columns(3)


# with col1:

#     st.metric(
#         "Attack Precision",
#         "90%"
#     )


# with col2:

#     st.metric(
#         "Attack Recall",
#         "35%"
#     )


# with col3:

#     st.metric(
#         "Attack F1 Score",
#         "51%"
#     )


# # ============================================================
# # VISUALIZATIONS
# # ============================================================

# st.markdown(
#     '<div class="section-title">📈 Detection Analysis</div>',
#     unsafe_allow_html=True
# )

# col1, col2 = st.columns(2)


# with col1:

#     if os.path.exists(
#         "results/confusion_matrix.png"
#     ):

#         st.image(
#             "results/confusion_matrix.png",
#             caption="Confusion Matrix",
#             use_container_width=True
#         )


# with col2:

#     if os.path.exists(
#         "results/traffic_distribution.png"
#     ):

#         st.image(
#             "results/traffic_distribution.png",
#             caption="Detected Network Traffic",
#             use_container_width=True
#         )


# # ============================================================
# # ANOMALY SCORE
# # ============================================================

# st.markdown(
#     '<div class="section-title">🔎 Anomaly Score Distribution</div>',
#     unsafe_allow_html=True
# )

# if os.path.exists(
#     "results/anomaly_scores.png"
# ):

#     st.image(
#         "results/anomaly_scores.png",
#         use_container_width=True
#     )


# # ============================================================
# # ATTACK CATEGORY
# # ============================================================

# st.markdown(
#     '<div class="section-title">🚨 Attack Category Analysis</div>',
#     unsafe_allow_html=True
# )

# if os.path.exists(
#     "results/attack_categories.png"
# ):

#     st.image(
#         "results/attack_categories.png",
#         use_container_width=True
#     )


# # ============================================================
# # SUSPICIOUS TRAFFIC
# # ============================================================

# st.markdown(
#     '<div class="section-title">🚨 Suspicious Network Traffic</div>',
#     unsafe_allow_html=True
# )

# suspicious = results[
#     results["prediction"] == 1
# ].copy()


# # Sort by anomaly score

# suspicious = suspicious.sort_values(
#     "anomaly_score",
#     ascending=False
# )


# # Select useful columns

# display_columns = [
#     "proto",
#     "service",
#     "state",
#     "dur",
#     "sbytes",
#     "dbytes",
#     "anomaly_score"
# ]

# available_columns = [
#     col
#     for col in display_columns
#     if col in suspicious.columns
# ]


# st.dataframe(
#     suspicious[
#         available_columns
#     ].head(50),
#     use_container_width=True,
#     height=400
# )


# # ============================================================
# # SIDEBAR
# # ============================================================

# st.sidebar.title("🛡️ System Information")

# st.sidebar.info(
#     """
#     Model: Isolation Forest

#     Dataset: UNSW-NB15

#     Learning Type:
#     Unsupervised Anomaly Detection

#     Training:
#     Normal traffic only

#     Purpose:
#     Identify unusual network traffic
#     """
# )


# st.sidebar.markdown("---")

# st.sidebar.write(
#     "### Detection Logic"
# )

# st.sidebar.write(
#     """
#     The model learns patterns from normal
#     network traffic. Traffic that deviates
#     significantly from these patterns is
#     flagged as anomalous.
#     """
# )


# st.sidebar.markdown("---")

# st.sidebar.caption(
#     "Cybersecurity ML Project"
# )
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Network Anomaly Detector",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #ffffff;
}

.subtitle {
    font-size: 17px;
    color: #94a3b8;
    margin-bottom: 30px;
}

.metric-card {
    background: #111827;
    border: 1px solid #1e293b;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
}

.metric-title {
    color: #94a3b8;
    font-size: 14px;
}

.metric-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: 700;
}

.section-title {
    color: #ffffff;
    font-size: 24px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = "models/isolation_forest.pkl"

if not os.path.exists(MODEL_PATH):

    st.error(
        "Trained model not found. "
        "Please run anomaly_detection.py first."
    )

    st.stop()


model_data = joblib.load(MODEL_PATH)

pipeline = model_data["pipeline"]
threshold = model_data["threshold"]


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">🛡️ Network Anomaly Detector</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'UNSW-NB15 • Unsupervised Learning • Isolation Forest'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛡️ System Information")

st.sidebar.info(
    """
Model: Isolation Forest

Dataset: UNSW-NB15

Learning Type:
Unsupervised Anomaly Detection

Training:
Normal traffic only

Purpose:
Identify unusual network traffic
"""
)

st.sidebar.markdown("---")

st.sidebar.write("### Detection Logic")

st.sidebar.write(
    """
The model learns patterns from normal
network traffic.

Traffic that deviates significantly
from learned patterns is flagged
as anomalous.
"""
)

st.sidebar.markdown("---")

st.sidebar.write("### Detection Threshold")

st.sidebar.code(
    f"{threshold:.6f}"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Cybersecurity ML Project"
)


# ============================================================
# TABS
# ============================================================

tab1, tab2 = st.tabs(
    [
        "📊 Dashboard",
        "🔍 Analyze New Traffic"
    ]
)


# ============================================================
# TAB 1 — EXISTING RESULTS
# ============================================================

with tab1:

    results_path = "results/anomaly_results.csv"

    if not os.path.exists(results_path):

        st.warning(
            "Results file not found. "
            "Run anomaly_detection.py first."
        )

    else:

        results = pd.read_csv(results_path)

        total_records = len(results)

        normal_count = (
            results["prediction"] == 0
        ).sum()

        anomaly_count = (
            results["prediction"] == 1
        ).sum()

        anomaly_percentage = (
            anomaly_count / total_records
        ) * 100


        # ----------------------------------------------------
        # METRICS
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        TOTAL TRAFFIC
                    </div>
                    <div class="metric-value">
                        {total_records:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        NORMAL TRAFFIC
                    </div>
                    <div class="metric-value">
                        {normal_count:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        ANOMALIES
                    </div>
                    <div class="metric-value">
                        {anomaly_count:,}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">
                        ANOMALY RATE
                    </div>
                    <div class="metric-value">
                        {anomaly_percentage:.1f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📊 Model Performance'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Attack Precision",
                "90%"
            )

        with col2:
            st.metric(
                "Attack Recall",
                "35%"
            )

        with col3:
            st.metric(
                "Attack F1 Score",
                "51%"
            )


        # ----------------------------------------------------
        # GRAPHS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📈 Detection Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            if os.path.exists(
                "results/confusion_matrix.png"
            ):

                st.image(
                    "results/confusion_matrix.png",
                    caption="Confusion Matrix",
                    use_container_width=True
                )

        with col2:

            if os.path.exists(
                "results/traffic_distribution.png"
            ):

                st.image(
                    "results/traffic_distribution.png",
                    caption="Detected Network Traffic",
                    use_container_width=True
                )


        # ----------------------------------------------------
        # ANOMALY SCORE
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🔎 Anomaly Score Distribution'
            '</div>',
            unsafe_allow_html=True
        )

        if os.path.exists(
            "results/anomaly_scores.png"
        ):

            st.image(
                "results/anomaly_scores.png",
                use_container_width=True
            )


        # ----------------------------------------------------
        # ATTACK CATEGORY
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🚨 Attack Category Analysis'
            '</div>',
            unsafe_allow_html=True
        )

        if os.path.exists(
            "results/attack_categories.png"
        ):

            st.image(
                "results/attack_categories.png",
                use_container_width=True
            )


        # ----------------------------------------------------
        # SUSPICIOUS TRAFFIC
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🚨 Suspicious Network Traffic'
            '</div>',
            unsafe_allow_html=True
        )

        suspicious = results[
            results["prediction"] == 1
        ].copy()

        suspicious = suspicious.sort_values(
            "anomaly_score",
            ascending=False
        )

        display_columns = [
            "proto",
            "service",
            "state",
            "dur",
            "sbytes",
            "dbytes",
            "anomaly_score"
        ]

        available_columns = [
            col
            for col in display_columns
            if col in suspicious.columns
        ]

        st.dataframe(
            suspicious[
                available_columns
            ].head(50),
            use_container_width=True,
            height=400
        )


# ============================================================
# TAB 2 — ANALYZE NEW TRAFFIC
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        '🔍 Analyze New Network Traffic'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
Upload a network traffic dataset in CSV or Parquet format.
The trained Isolation Forest model will classify each
record as Normal or Anomaly.
"""
    )


    uploaded_file = st.file_uploader(
        "Upload Network Traffic Dataset",
        type=["csv", "parquet"]
    )


    if uploaded_file is not None:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        try:

            # -----------------------------------------------
            # READ FILE
            # -----------------------------------------------

            if uploaded_file.name.endswith(".csv"):

                uploaded_data = pd.read_csv(
                    uploaded_file
                )

            else:

                uploaded_data = pd.read_parquet(
                    uploaded_file
                )


            st.write(
                f"Dataset contains "
                f"**{len(uploaded_data):,} records**."
            )


            # -----------------------------------------------
            # SHOW DATA
            # -----------------------------------------------

            with st.expander(
                "👁️ Preview Uploaded Data"
            ):

                st.dataframe(
                    uploaded_data.head(10),
                    use_container_width=True
                )


            # -----------------------------------------------
            # ANALYZE BUTTON
            # -----------------------------------------------

            if st.button(
                "🔍 Analyze Traffic",
                type="primary",
                use_container_width=True
            ):

                with st.spinner(
                    "Analyzing network traffic..."
                ):

                    # Remove labels if present
                    prediction_data = uploaded_data.copy()

                    columns_to_remove = [
                        "label",
                        "attack_cat",
                        "actual_label",
                        "prediction",
                        "prediction_name",
                        "anomaly_score"
                    ]

                    for column in columns_to_remove:

                        if column in prediction_data.columns:

                            prediction_data = (
                                prediction_data.drop(
                                    columns=[column]
                                )
                            )


                    # ---------------------------------------
                    # PREDICT
                    # ---------------------------------------

                    scores = -pipeline.decision_function(
                        prediction_data
                    )

                    predictions = (
                        scores >= threshold
                    ).astype(int)


                    # ---------------------------------------
                    # RESULTS
                    # ---------------------------------------

                    analysis_results = (
                        uploaded_data.copy()
                    )

                    analysis_results[
                        "anomaly_score"
                    ] = scores

                    analysis_results[
                        "prediction"
                    ] = predictions

                    analysis_results[
                        "prediction_name"
                    ] = np.where(
                        predictions == 1,
                        "Anomaly",
                        "Normal"
                    )


                    # Save to session state

                    st.session_state[
                        "analysis_results"
                    ] = analysis_results


        except Exception as e:

            st.error(
                "Unable to analyze this dataset."
            )

            st.code(
                str(e)
            )


    # ========================================================
    # DISPLAY ANALYSIS RESULTS
    # ========================================================

    if "analysis_results" in st.session_state:

        analysis_results = st.session_state[
            "analysis_results"
        ]


        normal_count = (
            analysis_results["prediction"] == 0
        ).sum()

        anomaly_count = (
            analysis_results["prediction"] == 1
        ).sum()

        total = len(analysis_results)


        st.markdown("---")

        st.markdown(
            '<div class="section-title">'
            '📊 Analysis Results'
            '</div>',
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # RESULT METRICS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Records",
                f"{total:,}"
            )

        with col2:

            st.metric(
                "Normal",
                f"{normal_count:,}"
            )

        with col3:

            st.metric(
                "Anomalies",
                f"{anomaly_count:,}"
            )


        # ----------------------------------------------------
        # ANOMALY RATE
        # ----------------------------------------------------

        anomaly_rate = (
            anomaly_count / total * 100
        )

        st.progress(
            min(anomaly_rate / 100, 1.0)
        )

        st.write(
            f"Anomaly rate: **{anomaly_rate:.2f}%**"
        )


        # ----------------------------------------------------
        # SCORE DISTRIBUTION
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📈 Anomaly Score Distribution'
            '</div>',
            unsafe_allow_html=True
        )

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.hist(
            analysis_results[
                "anomaly_score"
            ],
            bins=50
        )

        ax.axvline(
            threshold,
            linestyle="--",
            label="Detection Threshold"
        )

        ax.set_xlabel(
            "Anomaly Score"
        )

        ax.set_ylabel(
            "Number of Records"
        )

        ax.set_title(
            "Uploaded Traffic Anomaly Scores"
        )

        ax.legend()

        st.pyplot(fig)


        # ----------------------------------------------------
        # SUSPICIOUS RECORDS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🚨 Detected Anomalies'
            '</div>',
            unsafe_allow_html=True
        )

        suspicious = analysis_results[
            analysis_results["prediction"] == 1
        ].copy()

        suspicious = suspicious.sort_values(
            "anomaly_score",
            ascending=False
        )


        st.dataframe(
            suspicious.head(100),
            use_container_width=True,
            height=450
        )


        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        csv_data = analysis_results.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Analysis Results",
            data=csv_data,
            file_name="network_anomaly_results.csv",
            mime="text/csv",
            use_container_width=True
        )