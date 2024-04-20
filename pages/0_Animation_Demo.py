# Import necessary libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Define countries with latitude and longitude data
countries = {
    'Nigeria': {'lat': 9.082, 'lon': 8.675},
    'Ivory Coast': {'lat': 7.54, 'lon': -5.5471},
    'Kenya': {'lat': 1.2921, 'lon': 36.8219},
    'Mozambique': {'lat': -18.665695, 'lon': 35.529562},
    'Ivory Coast (Côte d\'Ivoire)': {'lat': 7.54, 'lon': -5.5471}  # Adding for Ivory Coast alias
}

# Function to load data from GitHub
def load_data_from_github(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {str(e)}")
        return None

# Function to plot percentage bar chart
def plot_percentage_bar_chart(data, column):
    category_percentage = data[column].value_counts(normalize=True) * 100
    fig = px.bar(category_percentage, x=category_percentage.index, y=category_percentage.values,
                 labels={'x': f'{column}', 'y': 'Percentage'},
                 title=f'Percentage of {column} by Category',
                 color=category_percentage.index,
                 color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_traces(texttemplate='%{y:.0f}%', textposition='outside')
    fig.update_layout(xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig)

# Main function for Streamlit app
def main():
    st.set_page_config(
        page_title="Impact of COVID-19 in Sub-Saharan Africa",
        page_icon="🌍"
    )

    st.title("Exploratory Data Analysis")

    # Get URL of the dataset on GitHub
    github_url = "https://raw.githubusercontent.com/NAKIBINGEGIDEON/data-analysis-and-visualization-project/92354269f67066df75a9fb6e47cbdcc820cbfc78/data.csv"

    # Load the dataset
    data = load_data_from_github(github_url)

    if data is not None:
        st.header("Dataset Preview:")
        st.write(data.head())

    # Filter countries
    selected_country = st.multiselect("Select Countries", list(countries.keys()), default=list(countries.keys()))

    # Filter columns
    if data is not None:
        selected_columns = st.multiselect("Select Columns", data.columns)

        if selected_country:
            filtered_data = data[data['Country'].isin(selected_country)]
        else:
            filtered_data = data

        if selected_columns:
            filtered_data = filtered_data[selected_columns]

        # Display filtered data
        st.subheader("Filtered Data")
        st.write(filtered_data)

        # Plot interactive bar charts showing percentages
        if not filtered_data.empty and selected_columns:
            for column in selected_columns:
                st.subheader(f"Percentage of {column} by Category")
                plot_percentage_bar_chart(filtered_data, column)

# Entry point of the Streamlit app
if __name__ == "__main__":
    main()
