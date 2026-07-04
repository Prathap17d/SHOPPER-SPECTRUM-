# 🛒 Shopper Spectrum: Customer Segmentation & Product Recommendations

An end-to-end e-commerce data science project that applies unsupervised machine learning to transaction logs. The project delivers interactive customer profile grouping and real-time product affinity recommendations through a professional web dashboard.

🌐 **Live Streamlit App:** *([Paste your Streamlit Cloud link here once deployed](https://2ejpwy4utmgppydu6ca8mu.streamlit.app/))*

---

## 📁 Repository Structure

```text
shopper-spectrum/
│
├── data_cleaning.ipynb      # Step 1: Handling missing data, filtering anomalies, & preprocessing
├── EDA.ipynb                # Step 2: Extracting geographic, product, and temporal insights
├── app.py                   # Step 3: Streamlit multi-module application deployment script
├── requirements.txt         # Package dependencies for cloud hosting
├── README.md                # Documentation manual
│
└── models/                  # Saved machine learning assets & matrices
                             # Trained K-Means segmentation model
                             # StandardScaler instance for input vectors
                             # Cosine Similarity matrix for recommendations
