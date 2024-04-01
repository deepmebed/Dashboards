import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer


# Function to load and preprocess data
def load_and_preprocess_data():
    dataset = pd.read_csv('Dataset_Clean_Climate_change_indicators_for_pakistan.csv')
    dataset = dataset.drop(['Sno', 'Country Name'], axis=1)
    # Replace NaN values with the mean of each column
    imputer = SimpleImputer(strategy='mean')
    dataset = pd.DataFrame(imputer.fit_transform(dataset), columns=dataset.columns)
    return dataset


# Function for data visualization page
def visualize_data(dataset, selected_indicators):
    st.title("Climate Change Indicators Visualization")
    # Include 'Year' column along with the selected indicators
    selected_columns = ['Year'] + selected_indicators
    st.write(dataset[selected_columns])

    for col in selected_indicators:
        if col != 'Year':
            st.subheader(col)
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(dataset['Year'], dataset[col], label=col)
            ax.set_title(col + " per year")
            ax.set_xlabel('Years')
            ax.set_ylabel(col)
            ax.legend()
            st.pyplot(fig)


# Function for all indicators page
def visualize_all_indicators(dataset, selected_graph):
    st.title("All Indicators Visualization")
    if selected_graph == "All Graphs":
        for col in dataset.columns:
            if col != 'Year':
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.plot(dataset['Year'], dataset[col], label=col)
                if col != 'RainFall Mean ()':  # Include rainfall part for all indicators except rainfall itself
                    ax.plot(dataset['Year'], dataset['RainFall Mean ()'], label='Rainfall', color='green', linestyle='--')
                ax.set_title(col + " per year")
                ax.set_xlabel('Years')
                ax.set_ylabel(col)
                ax.legend()
                st.pyplot(fig)
    else:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dataset['Year'], dataset[selected_graph], label=selected_graph)
        ax.plot(dataset['Year'], dataset['RainFall Mean ()'], label='Rainfall', color='green', linestyle='--')
        ax.set_title(selected_graph + " per year")
        ax.set_xlabel('Years')
        ax.set_ylabel(selected_graph)
        ax.legend()
        st.pyplot(fig)


# Function to perform machine learning
def perform_machine_learning(dataset, selected_regressor):
    st.title("Rainfall Prediction using Machine Learning")

    if selected_regressor == "Best Regressor":
        # Compare performance of all regressors
        regressors = {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(),
            "K-Nearest Neighbors": KNeighborsRegressor()
        }
        best_regressor = None
        best_score = -float('inf')
        for name, reg in regressors.items():
            X = dataset.drop(['Year', 'RainFall Mean ()'], axis=1)
            y = dataset['RainFall Mean ()']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

            reg.fit(X_train, y_train)
            pred = reg.predict(X_test)
            score = r2_score(y_test, pred)
            if score > best_score:
                best_score = score
                best_regressor = name

        # Plot graphs and scores of best regressor
        perform_machine_learning(dataset, best_regressor)
        return

    # Initialize the selected regressor
    if selected_regressor == "Linear Regression":
        regressor = LinearRegression()
    elif selected_regressor == "Ridge Regression":
        regressor = Ridge()
    elif selected_regressor == "K-Nearest Neighbors":
        regressor = KNeighborsRegressor()

    # Splitting data for machine learning
    X = dataset.drop(['Year', 'RainFall Mean ()'], axis=1)
    y = dataset['RainFall Mean ()']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Train the regressor
    regressor.fit(X_train, y_train)
    pred = regressor.predict(X_test)

    # Evaluate the regressor
    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)

    # Plot original vs predicted
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(list(y_test), label='Original', color='blue')
    ax.plot(pred, label='Predicted', color='orange')
    ax.legend()
    ax.set_title(selected_regressor + ' Original and Predicted Output')
    st.pyplot(fig)

    # Display evaluation scores
    st.subheader("Evaluation Scores:")
    st.write("R2 Score:", r2)
    st.write("Mean Absolute Error:", mae)
    st.write("Mean Squared Error:", mse)


# Main function to run the app
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Data Visualization", "All Indicators", "Machine Learning"])

    dataset = load_and_preprocess_data()

    if page == "Data Visualization":
        st.sidebar.title("Select Indicators")
        selected_indicators = st.sidebar.multiselect("Select indicators", dataset.columns[1:])
        visualize_data(dataset, selected_indicators)

    elif page == "Machine Learning":
        st.sidebar.title("Select Regressor")
        selected_regressor = st.sidebar.selectbox("Choose a regressor",
                                                  ["Linear Regression", "Ridge Regression", "K-Nearest Neighbors",
                                                   "Best Regressor"])
        perform_machine_learning(dataset, selected_regressor)

    elif page == "All Indicators":
        st.sidebar.title("Select Graph")
        selected_graph = st.sidebar.selectbox("Choose a graph", ["All Graphs"] + list(dataset.columns[1:]))
        visualize_all_indicators(dataset, selected_graph)


if __name__ == "__main__":
    main()
