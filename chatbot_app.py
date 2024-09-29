from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Data preprocessing and analysis functions here

def preprocess_data(file_path):
    """
    Load and preprocess data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Preprocessed data.
    """
    df = pd.read_csv(file_path)

    # Clean and convert data to numeric
    df.columns = df.columns.str.strip()
    numeric_cols = ['Total Revenue($ millions)', 'Net Income', 'Total Assets', 'Total Liabilities', 'CFFO']

    for col in numeric_cols:
        # Check if the column contains strings
        if df[col].dtype == 'object':
            # Remove commas and convert to numeric
            df[col] = pd.to_numeric(df[col].str.replace(',', ''), errors='coerce')
        else:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Calculate year-over-year changes for each financial metric
    df['Revenue Growth (%)'] = df.groupby('Company')['Total Revenue($ millions)'].pct_change(fill_method=None) * 100
    df['Net Income Growth (%)'] = df.groupby('Company')['Net Income'].pct_change(fill_method=None) * 100

    return df

def get_apple_roa_latest_fiscal_year(dataframe):
    """
    Get Apple's Return on Assets (ROA) for the latest fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.

    Returns:
        str: Apple's ROA for the latest fiscal year.
    """
    apple_df = dataframe[dataframe['Company'] == 'Apple']
    latest_year = apple_df['Fiscal Year'].max()
    latest_data = apple_df[apple_df['Fiscal Year'] == latest_year]
    roa = (latest_data['Net Income'].values[0] / latest_data['Total Assets'].values[0]) * 100
    return f"Apple's ROA for the latest fiscal year ({latest_year}) is {roa:.2f}%."

def get_total_revenue_for_year(dataframe, year):
    """
    Get the total revenue for a specific year across all companies.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Total revenue for the specified year.
    """
    total_revenue = dataframe[dataframe['Fiscal Year'] == year]['Total Revenue($ millions)'].sum()
    return f"The total revenue for the year {year} is {total_revenue:.2f} million."

def get_microsoft_net_income(dataframe, year):
    """
    Get Microsoft's Net Income for a specific fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Microsoft's Net Income for the specified fiscal year.
    """
    net_income = dataframe[(dataframe['Company'] == 'Microsoft') & (dataframe['Fiscal Year'] == year)]['Net Income'].iloc[0]
    return f"Microsoft's Net Income in Fiscal Year {year} is {net_income:.2f} million."

def get_tesla_total_assets(dataframe, year):
    """
    Get Tesla's Total Assets for a specific fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Tesla's Total Assets for the specified fiscal year.
    """
    total_assets = dataframe[(dataframe['Company'] == 'Tesla') & (dataframe['Fiscal Year'] == year)]['Total Assets'].iloc[0]
    return f"Tesla's Total Assets in Fiscal Year {year} are {total_assets:.2f} million."

def get_apple_total_revenue(dataframe, year):
    """
    Get Apple's Total Revenue for a specific fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Apple's Total Revenue for the specified fiscal year.
    """
    total_revenue = dataframe[(dataframe['Company'] == 'Apple') & (dataframe['Fiscal Year'] == year)]['Total Revenue($ millions)'].iloc[0]
    return f"Apple's Total Revenue in Fiscal Year {year} is {total_revenue:.2f} million."

def get_tesla_cffo(dataframe, year):
    """
    Get Tesla's Cash Flow from Operations (CFFO) for a specific fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Tesla's CFFO for the specified fiscal year.
    """
    cffo = dataframe[(dataframe['Company'] == 'Tesla') & (dataframe['Fiscal Year'] == year)]['CFFO'].iloc[0]
    return f"Tesla's Cash Flow from Operations (CFFO) in Fiscal Year {year} is {cffo:.2f} million."

def get_microsoft_total_liabilities(dataframe, year):
    """
    Get Microsoft's Total Liabilities for a specific fiscal year.

    Args:
        dataframe (pd.DataFrame): DataFrame containing financial data.
        year (int): Fiscal year.

    Returns:
        str: Microsoft's Total Liabilities for the specified fiscal year.
    """
    total_liabilities = dataframe[(dataframe['Company'] == 'Microsoft') & (dataframe['Fiscal Year'] == year)]['Total Liabilities'].iloc[0]
    return f"Microsoft's Total Liabilities in Fiscal Year {year} are {total_liabilities:.2f} million."

# Preprocess the data once and store it globally to avoid redefining 'df'
CSV_FILE_PATH = r'C:\Users\HP\Documents\Data Analysis\BCG\Task 1 - 10-K_Analysis\10-K Filings.csv'
df = preprocess_data(CSV_FILE_PATH)

predefined_queries = {
    "What was Microsoft's Net Income in Fiscal Year 2022?": lambda: get_microsoft_net_income(df, 2022),
    "What were Tesla's Total Assets in Fiscal Year 2021?": lambda: get_tesla_total_assets(df, 2021),
    "What was Apple's Total Revenue in Fiscal Year 2023?": lambda: get_apple_total_revenue(df, 2023),
    "What was Tesla's Cash Flow from Operations (CFFO) in Fiscal Year 2022?": lambda: get_tesla_cffo(df, 2022),
    "What were Microsoft's Total Liabilities in Fiscal Year 2021?": lambda: get_microsoft_total_liabilities(df, 2021)
}

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """
    Handle query requests and return the appropriate response.
    """
    user_query = request.form['query']

    if user_query in predefined_queries:
        response = predefined_queries[user_query]()
    else:
        response = "Sorry, I can only provide information on predefined queries."

    return render_template('index.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
