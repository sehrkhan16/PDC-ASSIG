import pandas as pd
import datetime
from multiprocessing import Pool

# Load the fee structure CSV file
df_fee = pd.read_csv('fee.csv')

# Function to calculate the most common date
def calculate_most_common_date(dates):
    date_counts = {}
    for date in dates:
        date_counts[date] = date_counts.get(date, 0) + 1
    most_common_date = max(date_counts, key=date_counts.get)
    return most_common_date

# Function to retrieve fee dates for a student (linear processing)
def retrieve_fees_linear(student_name):
    # Normalize the input and column name for case and whitespace
    student_name = student_name.strip().lower()
    df_fee['Name'] = df_fee['Name'].str.strip().str.lower()

    # Filter the student data
    student_data = df_fee[df_fee['Name'] == student_name]
    
    if student_data.empty:
        return f"No data found for student: {student_name}"

    # Collect all fee submission dates
    fee_dates = []
    for column in student_data.columns:
        if "Fee Submission Date" in column:
            fee_dates.extend(student_data[column].dropna().tolist())

    if not fee_dates:
        return f"No fee dates available for student: {student_name}"

    # Calculate the most common fee submission date
    most_common_date = calculate_most_common_date(fee_dates)
    return f"Student: {student_name}\nFee Dates: {fee_dates}\nMost Common Date: {most_common_date}"

# Helper function for parallel processing (one student)
def process_student_parallel(student_name):
    return retrieve_fees_linear(student_name)

# Function to retrieve fee dates for a student (parallel processing)
def retrieve_fees_parallel(student_name):
    with Pool(1) as pool:  # Using one process as an example for parallelization
        result = pool.apply(process_student_parallel, args=(student_name,))
    return result

# Main program
if __name__ == "__main__":
    student_name = input("Enter the name of the student: ")

    print("\n--- Linear Processing ---")
    linear_result = retrieve_fees_linear(student_name)
    print(linear_result)

    print("\n--- Parallel Processing ---")
    parallel_result = retrieve_fees_parallel(student_name)
    print(parallel_result)
