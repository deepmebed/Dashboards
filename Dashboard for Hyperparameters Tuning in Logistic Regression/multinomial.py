import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

plt.style.use('fivethirtyeight')

st.sidebar.markdown("# Logistic Regression Classifier")

dataset = st.sidebar.selectbox(
    'Select Dataset',
    ('Iris', 'Tips')  # Added 'Tips' option
)

penalty = st.sidebar.selectbox(
    'Regularization',
    ('l2', 'l1', 'elasticnet', 'none')
)

c_input = float(st.sidebar.number_input('C', value=1.0))

solver = st.sidebar.selectbox(
    'Solver',
    ('newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga')
)

max_iter = int(st.sidebar.number_input('Max Iterations', value=100))

multi_class = st.sidebar.selectbox(
    'Multi Class',
    ('auto', 'ovr', 'multinomial')
)

l1_ratio = float(st.sidebar.number_input('l1 Ratio'))

def load_initial_graph(dataset, ax):
    if dataset == "Iris":
        iris = sns.load_dataset('iris')
        X, y = iris.iloc[:, :2], iris['species'].map({'setosa': 0, 'versicolor': 1, 'virginica': 2})
        ax.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, cmap='viridis')  # Use y directly
        return X, y
    elif dataset == "Tips":  # Load Tips dataset and handle binary classification
        tips = sns.load_dataset('tips')
        X, y = tips[['total_bill', 'tip']], tips['smoker'].map({'Yes': 1, 'No': 0})  # Map 'Yes' to 1 and 'No' to 0
        ax.scatter(X.iloc[:, 0], X.iloc[:, 1], c=y, cmap='viridis')
        return X, y



def draw_meshgrid(X):
    a = np.arange(start=X.iloc[:, 0].min() - 1, stop=X.iloc[:, 0].max() + 1, step=0.01)
    b = np.arange(start=X.iloc[:, 1].min() - 1, stop=X.iloc[:, 1].max() + 1, step=0.01)

    XX, YY = np.meshgrid(a, b)

    input_array = np.array([XX.ravel(), YY.ravel()]).T

    return XX, YY, input_array

# Load initial graph
fig, ax = plt.subplots()

# Plot initial graph
X, y = load_initial_graph(dataset, ax)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
orig = st.pyplot(fig)

if st.sidebar.button('Run Algorithm'):
    orig.empty()

    clf = LogisticRegression(penalty=penalty, C=c_input, solver=solver, max_iter=max_iter,
                             multi_class=multi_class, l1_ratio=l1_ratio)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    XX, YY, input_array = draw_meshgrid(X)
    labels = clf.predict(input_array)

    ax.contourf(XX, YY, labels.reshape(XX.shape), alpha=0.5, cmap='viridis')
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    orig = st.pyplot(fig)
    accuracy = accuracy_score(y_test, y_pred)
    st.subheader("Accuracy for Logistic Regression: " + str(round(accuracy, 2)))

    # Display the dataset
    st.subheader(f"{dataset} Dataset")
    st.write(X)  # Displaying only features for simplicity
