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


def format_excel_sheet(writer, sheet_name, column_widths=None, header_format=None):
    """
    Helper to format Excel sheets: set column widths and header formatting.
    Args:
        writer (pd.ExcelWriter): ExcelWriter object
        sheet_name (str): Name of the sheet to format
        column_widths (dict): {col_idx: width}
        header_format (dict): Format options for header
    """
    worksheet = writer.sheets[sheet_name]
    if column_widths:
        for col_idx, width in column_widths.items():
            worksheet.set_column(col_idx, col_idx, width)
    if header_format:
        fmt = writer.book.add_format(header_format)
        worksheet.set_row(0, None, fmt)


def embed_chart_in_excel(writer, sheet_name, image_path, cell='B2'):
    """
    Helper to embed a chart image into an Excel sheet.
    Args:
        writer (pd.ExcelWriter): ExcelWriter object
        sheet_name (str): Name of the sheet to embed the image
        image_path (str): Path to the image file
        cell (str): Cell location to insert the image
    """
    worksheet = writer.sheets[sheet_name]
    worksheet.insert_image(cell, image_path)


def auto_adjust_column_widths(df, worksheet):
    """
    Auto-adjust column widths for all columns in a DataFrame when exporting to Excel.
    Args:
        df (pd.DataFrame): DataFrame being exported
        worksheet (xlsxwriter worksheet): Worksheet object
    """
    for i, col in enumerate(df.columns):
        max_len = max(
            df[col].astype(str).map(len).max(),
            len(str(col))
        ) + 2
        worksheet.set_column(i, i, max_len)


def add_summary_row(df, summary_type='total'):
    """
    Add a summary row (total or average) to a DataFrame before exporting to Excel.
    Args:
        df (pd.DataFrame): DataFrame to summarize
        summary_type (str): 'total' or 'average'
    Returns:
        pd.DataFrame: DataFrame with summary row appended
    """
    if summary_type == 'total':
        summary = df.sum(numeric_only=True)
        summary.name = 'Total'
    elif summary_type == 'average':
        summary = df.mean(numeric_only=True)
        summary.name = 'Average'
    else:
        raise ValueError("summary_type must be 'total' or 'average'")
    return pd.concat([df, pd.DataFrame([summary])])


def freeze_panes(writer, sheet_name, row=1, col=1):
    """
    Helper to freeze the top row and first column in an Excel worksheet.
    Args:
        writer (pd.ExcelWriter): ExcelWriter object
        sheet_name (str): Name of the sheet to freeze panes
        row (int): Row index to freeze (default 1)
        col (int): Column index to freeze (default 1)
    """
    worksheet = writer.sheets[sheet_name]
    worksheet.freeze_panes(row, col) 