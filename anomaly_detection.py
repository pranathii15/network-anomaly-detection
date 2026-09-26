import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)


# ============================================================
# 1. PATHS
# ============================================================

TRAIN_PATH = "data/UNSW_NB15_training-set.parquet"
TEST_PATH = "data/UNSW_NB15_testing-set.parquet"

os.makedirs("results", exist_ok=True)
os.makedirs("models", exist_ok=True)


# ============================================================
# 2. LOAD DATA
# ============================================================

train = pd.read_parquet(TRAIN_PATH)
test = pd.read_parquet(TEST_PATH)

print("Training shape:", train.shape)
print("Testing shape:", test.shape)


# ============================================================
# 3. NORMAL TRAINING DATA ONLY
# ============================================================

normal_train = train[train["label"] == 0].copy()

print("\nNormal records:", len(normal_train))


# Split normal data into model-training and validation data
normal_model_train, normal_validation = train_test_split(
    normal_train,
    test_size=0.20,
    random_state=42
)

print("Model training records:", len(normal_model_train))
print("Validation records:", len(normal_validation))


# ============================================================
# 4. FEATURES
# ============================================================

drop_columns = ["attack_cat", "label"]

X_train = normal_model_train.drop(columns=drop_columns)

X_validation = normal_validation.drop(columns=drop_columns)

X_test = test.drop(columns=drop_columns)

y_test = test["label"]


categorical_features = [
    "proto",
    "service",
    "state"
]

numerical_features = [
    col for col in X_train.columns
    if col not in categorical_features
]


# ============================================================
# 5. PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            StandardScaler(),
            numerical_features
        ),
        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_features
        )
    ]
)


# ============================================================
# 6. ISOLATION FOREST
# ============================================================

model = IsolationForest(
    n_estimators=200,
    contamination="auto",
    random_state=42,
    n_jobs=-1
)


pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", model)
    ]
)


# ============================================================
# 7. TRAIN
# ============================================================

print("\nTraining Isolation Forest...")

pipeline.fit(X_train)

print("Training completed!")


# ============================================================
# 8. VALIDATION
# ============================================================

print("\nFinding threshold using validation data...")

validation_scores = -pipeline.decision_function(
    X_validation
)

# Since validation contains only normal traffic,
# choose a threshold that flags approximately 5%
# of normal validation traffic as anomalous.

threshold = np.percentile(
    validation_scores,
    95
)

print("Selected threshold:", threshold)


# ============================================================
# 9. FINAL TEST
# ============================================================

print("\nEvaluating on test set...")

test_scores = -pipeline.decision_function(X_test)

predictions = (
    test_scores >= threshold
).astype(int)


# ============================================================
# 10. RESULTS
# ============================================================

print("\nPrediction distribution:")

print(
    "Normal:",
    np.sum(predictions == 0)
)

print(
    "Anomaly:",
    np.sum(predictions == 1)
)


# ============================================================
# 11. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Normal",
            "Attack"
        ],
        zero_division=0
    )
)


# ============================================================
# 12. CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(
    y_test,
    predictions
)

print("\nConfusion Matrix:")
print(cm)


tn, fp, fn, tp = cm.ravel()

print("\nDetailed Results:")
print("True Negatives :", tn)
print("False Positives:", fp)
print("False Negatives:", fn)
print("True Positives :", tp)


# ============================================================
# 13. SAVE MODEL
# ============================================================

joblib.dump(
    {
        "pipeline": pipeline,
        "threshold": threshold
    },
    "models/isolation_forest.pkl"
)

print("\nModel saved:")
print("models/isolation_forest.pkl")


# ============================================================
# 14. SAVE RESULTS
# ============================================================

results = test.copy()

results["actual_label"] = y_test.values
results["prediction"] = predictions
results["anomaly_score"] = test_scores

results["prediction_name"] = results[
    "prediction"
].map({
    0: "Normal",
    1: "Anomaly"
})

results.to_csv(
    "results/anomaly_results.csv",
    index=False
)

print(
    "Results saved to results/anomaly_results.csv"
)


# ============================================================
# 15. CONFUSION MATRIX GRAPH
# ============================================================

plt.figure(figsize=(7, 5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Normal", "Anomaly"],
    yticklabels=["Normal", "Attack"]
)

plt.title("Network Anomaly Detection")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.tight_layout()

plt.savefig(
    "results/confusion_matrix.png",
    dpi=300
)

plt.close()


# ============================================================
# 16. TRAFFIC DISTRIBUTION
# ============================================================

normal_count = np.sum(predictions == 0)
anomaly_count = np.sum(predictions == 1)

plt.figure(figsize=(7, 5))

plt.bar(
    ["Normal", "Anomaly"],
    [normal_count, anomaly_count]
)

plt.title("Detected Network Traffic")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    "results/traffic_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 17. ANOMALY SCORE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    test_scores[y_test.values == 0],
    bins=50,
    alpha=0.6,
    label="Normal"
)

plt.hist(
    test_scores[y_test.values == 1],
    bins=50,
    alpha=0.6,
    label="Attack"
)

plt.axvline(
    threshold,
    linestyle="--",
    label="Detection Threshold"
)

plt.title("Anomaly Score Distribution")
plt.xlabel("Anomaly Score")
plt.ylabel("Records")
plt.legend()

plt.tight_layout()

plt.savefig(
    "results/anomaly_scores.png",
    dpi=300
)

plt.close()


# ============================================================
# 18. ATTACK CATEGORY ANALYSIS
# ============================================================

attack_results = results[
    results["actual_label"] == 1
]

category_detection = (
    attack_results
    .groupby("attack_cat")["prediction"]
    .mean()
    .sort_values(ascending=True)
)

print("\nAttack Category Detection Rate:")

print(
    (category_detection * 100).round(2)
)

plt.figure(figsize=(9, 6))

(category_detection * 100).plot(
    kind="barh"
)

plt.title("Detection Rate by Attack Category")
plt.xlabel("Detection Rate (%)")
plt.ylabel("Attack Category")

plt.tight_layout()

plt.savefig(
    "results/attack_categories.png",
    dpi=300
)

plt.close()


print("\n===================================")
print("MODEL BUILD COMPLETE")
print("===================================")