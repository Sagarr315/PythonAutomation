
import pandas as pd

from .config import EMPLOYEE_EXCEL, OUTPUT_DIR, SALES_EXCEL


# 1. Read Excel using pandas
def read_excel_data(file_path, sheet_name=0):

    dataframe = pd.read_excel(
        file_path,
        sheet_name=sheet_name
    )

    print(dataframe)

    return dataframe


# 2. Filter records
def filter_records(file_path, department):

    dataframe = pd.read_excel(file_path)

    filtered_data = dataframe[
        dataframe["Department"] == department
    ]

    print(filtered_data)

    return filtered_data


# 3. Sort records
def sort_records(file_path, column_name):

    dataframe = pd.read_excel(file_path)

    sorted_data = dataframe.sort_values(
        by=column_name
    )

    print(sorted_data)

    return sorted_data


# 4. Remove duplicates
def remove_duplicates(file_path, output_file):

    dataframe = pd.read_excel(file_path)

    cleaned_data = dataframe.drop_duplicates()

    cleaned_data.to_excel(output_file, index=False)

    print("Duplicate records removed.")


# 5. Merge Excel files
def merge_excel_files(file_paths, output_file):

    dataframes = [
        pd.read_excel(file_path)
        for file_path in file_paths
    ]

    combined_data = pd.concat(
        dataframes,
        ignore_index=True
    )

    combined_data.to_excel(
        output_file,
        index=False
    )

    print("Excel files merged successfully.")


# 6. Main execution
if __name__ == "__main__":

    print("\n--- Read Excel ---")
    read_excel_data(EMPLOYEE_EXCEL)

    print("\n--- Filter IT Employees ---")
    filter_records(EMPLOYEE_EXCEL, "IT")

    print("\n--- Sort Employees by Salary ---")
    sort_records(EMPLOYEE_EXCEL, "Salary")

    print("\n--- Remove Duplicates ---")
    remove_duplicates(
        EMPLOYEE_EXCEL,
        OUTPUT_DIR / "Cleaned_Employees.xlsx"
    )

    print("\n--- Merge Excel Files ---")
    merge_excel_files(
        [EMPLOYEE_EXCEL, SALES_EXCEL],
        OUTPUT_DIR / "Merged_Data.xlsx"
    )

    print("\nExcel processing completed!")
