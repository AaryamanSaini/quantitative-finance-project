import pandas as pd

def create_excel_dashboard(sheets_dict, file_path):
    """
    Create an Excel dashboard with multiple sheets.
    Args:
        sheets_dict (dict): Sheet name to DataFrame or data
        file_path (str): Output Excel file path
    """
    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        for sheet, data in sheets_dict.items():
            if isinstance(data, pd.DataFrame):
                data.to_excel(writer, sheet_name=sheet)
            elif isinstance(data, dict):
                pd.DataFrame([data]).to_excel(writer, sheet_name=sheet)
            else:
                pd.DataFrame(data).to_excel(writer, sheet_name=sheet)
        writer.save() 