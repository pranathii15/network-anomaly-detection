# 🛡️ Network Anomaly Detection using Isolation Forest

A machine learning-based cybersecurity project that detects unusual network traffic using **Isolation Forest**, an unsupervised anomaly detection algorithm.

The system is trained using normal network traffic from the **UNSW-NB15 dataset** and identifies traffic that significantly deviates from learned normal behavior.


Now available: https://detectnetworkanomaly.streamlit.app/
---

## 📌 Project Overview

Network attacks can produce traffic patterns that differ significantly from normal network communication. Traditional rule-based security systems may fail to detect previously unseen or unusual attacks.

This project implements an **unsupervised/one-class network anomaly detection system** using Isolation Forest.

The model learns the characteristics of normal network traffic and assigns an anomaly score to new network records.

The project also provides an interactive **Streamlit dashboard** where users can upload network traffic data in CSV or Parquet format and receive anomaly predictions.

---

## 🎯 Objectives

- Detect abnormal network traffic using machine learning.
- Learn normal network behavior without training on attack records.
- Identify suspicious network connections using Isolation Forest.
- Analyze anomaly scores and detection patterns.
- Evaluate the model using standard classification metrics.
- Provide an interactive dashboard for network traffic analysis.
- Allow users to upload new network traffic datasets for analysis.

---

## 📊 Dataset

### UNSW-NB15

The project uses the **UNSW-NB15 network intrusion detection dataset**.

The dataset contains network traffic records with features describing network connections and their behavior.

### Dataset features include:

- Duration
- Protocol
- Service
- Connection state
- Source and destination packet counts
- Source and destination bytes
- Network traffic rate
- Load
- Packet loss
- Jitter
- TCP-related features
- HTTP/FTP-related features
- Connection statistics

The dataset also contains labels identifying normal and attack traffic.

### Dataset split used

| Dataset | Records |
|---|---:|
| Training | 175,341 |
| Testing | 82,332 |

During model training, only the **56,000 normal training records** were used.

Attack records were excluded from model training to simulate an anomaly detection scenario where the model learns normal behavior.

---

## 🧠 Machine Learning Approach

### Isolation Forest

Isolation Forest is an unsupervised anomaly detection algorithm.

Instead of learning a classification boundary between normal and attack traffic, the model learns patterns in normal traffic and identifies observations that are easier to isolate.

### Workflow

```text
UNSW-NB15 Dataset
        ↓
Data Loading
        ↓
Data Preprocessing
        ↓
Separate Normal Training Traffic
        ↓
Categorical Feature Encoding
        ↓
Feature Preparation
        ↓
Train Isolation Forest
        ↓
Learn Normal Network Behavior
        ↓
Calculate Anomaly Scores
        ↓
Select Detection Threshold
        ↓
Normal / Anomaly Prediction
        ↓
Streamlit Dashboard

Details::

🔧 Data Preprocessing

The dataset contains both numerical and categorical features.

Categorical features
proto
service
state

These categorical features are encoded before being provided to the machine learning model.

Numerical features

The remaining network traffic features are processed as numerical inputs.

Attack records are excluded from model training.

Normal training records: 56,000
Attack records excluded: 119,341

The normal training data is further divided into training and validation subsets for threshold selection.

Model training records: 44,800
Validation records: 11,200


⚙️ Detection Threshold

Isolation Forest produces an anomaly score for each network record.

A validation-based threshold is selected to convert anomaly scores into final predictions.

The threshold used in the current model is approximately:

-0.006378

Records crossing the selected threshold are classified as anomalous.

📈 Model Performance

The trained model was evaluated on the complete UNSW-NB15 testing set.

Results
Metric	    Normal	    Attack
Precision	55%	        90%
Recall	    95%	        35%
F1 Score	69%	        51%

Overall accuracy: 62%

Detection results
Total test records: 82,332
Normal predicted:   64,476
Anomalies detected: 17,856

Anomaly rate: 21.69%
Confusion Matrix
                    Predicted
                 Normal   Anomaly
Actual Normal     35150     1850
Actual Attack     29326    16006

Interpretation
True Negatives: 35,150 normal records correctly identified.
False Positives: 1,850 normal records incorrectly flagged as anomalies.
False Negatives: 29,326 attack records not detected.
True Positives: 16,006 attack records detected as anomalies.

The model demonstrates that anomaly detection can identify a substantial portion of attack traffic while being trained only on normal traffic.

🚨 Attack Category Analysis

The UNSW-NB15 dataset contains multiple attack categories.

The current Isolation Forest model produced the following detection rates:

Attack Category	      Detection Rate
Generic	              74.69%
Worms	              13.64%
Exploits	          10.10%
Fuzzers	              7.77%
DoS	                  5.84%
Backdoor	          4.46%
Analysis              2.81%
Reconnaissance	      0.74%
Shellcode	          0.00%

These results show that anomaly detection performance varies considerably across attack categories.

🖥️ Streamlit Dashboard

The project includes an interactive Streamlit web application.

Dashboard features
📊 Network traffic overview
🔍 Anomaly detection results
📈 Anomaly score distribution
🚨 Suspicious traffic table
📁 CSV/Parquet file upload
📥 Downloadable analysis results
📊 Detection statistics
🔬 Attack category analysis

Application workflow
Upload CSV / Parquet
        ↓
Validate Dataset
        ↓
Apply Preprocessing
        ↓
Load Trained Model
        ↓
Generate Anomaly Scores
        ↓
Apply Detection Threshold
        ↓
Display Results
        ↓
Download Results

📂 Project Structure
cns/
│
├── app.py
├── anomaly_detection.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── UNSW_NB15_training-set.parquet
│   └── UNSW_NB15_testing-set.parquet
│
├── models/
│   └── isolation_forest.pkl
│
└── results/
    ├── anomaly_results.csv
    ├── confusion_matrix.png
    ├── prediction_distribution.png
    ├── anomaly_score_distribution.png
    └── attack_category_detection.png

🛠️ Technologies Used

Programming
Python
Machine Learning
Scikit-learn
Isolation Forest
Pandas
NumPy
Data Visualization
Matplotlib
Seaborn
Web Application
Streamlit
Dataset
UNSW-NB15
Development
VS Code
Git
GitHub

📦 Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL
cd cns

Install the required dependencies:

pip install -r requirements.txt

▶️ Running the Project
Run the anomaly detection model
python anomaly_detection.py

This trains the Isolation Forest model and generates the detection results.

Run the Streamlit dashboard
streamlit run app.py

The application will open in the browser, usually at:

http://localhost:8501

🔍 Using the Dashboard
Start the Streamlit application.
Open the Analyze New Traffic section.
Upload a network traffic dataset in CSV or Parquet format.
Click Analyze Traffic.
The trained Isolation Forest model processes the uploaded records.
The application displays:
Total records
Normal records
Anomalous records
Anomaly rate
Anomaly score distribution
Detected suspicious traffic
Download the generated analysis results if required.

🔐 Cybersecurity Relevance

The system demonstrates how machine learning can be applied to network security for detecting unusual traffic patterns.

Potential applications include:

Network intrusion detection
Security monitoring
Suspicious traffic identification
Security operations center (SOC) support
Network behavior analysis
Detection of previously unseen traffic patterns

⚠️ Limitations

The current implementation has several limitations:

Isolation Forest may miss some attack types.
Detection performance varies between attack categories.
False negatives are still present.
The system is evaluated using the UNSW-NB15 dataset and may behave differently on real-world network traffic.
The current system performs batch analysis rather than real-time packet monitoring.
Anomaly detection does not automatically identify the exact type of attack.
🚀 Future Enhancements

Possible future improvements include:

Implementing an Autoencoder-based anomaly detector.
Comparing Isolation Forest with One-Class SVM.
Combining multiple anomaly detection models.
Real-time network traffic monitoring.
Integration with packet capture tools such as Wireshark/tshark.
Real-time alerts for suspicious traffic.
Attack-category classification after anomaly detection.
Improved feature engineering.
Deployment as a cloud-based security monitoring application.
📌 Conclusion

This project demonstrates an unsupervised/one-class machine learning approach for network anomaly detection using Isolation Forest.

The model learns patterns from normal network traffic and identifies traffic that deviates from those patterns. The Streamlit dashboard provides an interactive interface for analyzing network traffic and visualizing detected anomalies.

The project provides a practical demonstration of applying machine learning techniques to cybersecurity and network intrusion detection.

👩‍💻 Author

Pranathi

Cybersecurity & Machine Learning Project
