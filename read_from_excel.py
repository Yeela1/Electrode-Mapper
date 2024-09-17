import pandas as pd


def read_excel_table(file_path, sheet_name=None):
    """
    Reads data from an .xlsx file and returns it as a pandas DataFrame.

    Parameters:
    - file_path: str, path to the .xlsx file.
    - sheet_name: str, name of the sheet to read. Default is None, which reads the first sheet.

    Returns:
    - DataFrame containing the data from the specified .xlsx file and sheet.
    """
    try:
        # Read the Excel file
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        return data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def filter_table_by_acquisition_point(table, search_string):
    """
    Filters the rows of a DataFrame based on whether the 'acquisition_point' column
    contains a specific substring.

    Parameters:
    - table: pandas DataFrame, the table to filter.
    - search_string: str, the substring to search for within the 'acquisition_point' column.

    Returns:
    - A DataFrame containing only the rows where 'acquisition_point' contains the search string.
    """
    try:
        # Ensure 'acquisition_point' column exists
        if 'acq_description' not in table.columns:
            raise ValueError("The column 'acq_description' does not exist in the table.")

        # Filter rows where 'acquisition_point' contains the search string (case insensitive)
        filtered_table = table[table['acq_description'].str.contains(search_string, case=False, na=False)]

        return filtered_table

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def create_electrode_dict(table):
    """
    Creates a dictionary from a DataFrame, where each key is an electrode number,
    and the value is an array containing the x, y, and z coordinates.

    Parameters:
    - table: pandas DataFrame, the table containing electrode data.

    Returns:
    - A dictionary with keys as 'electrode_num' and values as arrays of ['x(brainLab)', 'y(brainLab)', 'z(brainLab)'].
    """
    try:
        # Ensure required columns exist in the DataFrame
        required_columns = ['electrode_num', 'x(brainLab)', 'y(brainLab)', 'z(brainLab)']
        for col in required_columns:
            if col not in table.columns:
                raise ValueError(f"The column '{col}' does not exist in the table.")

        # Initialize an empty dictionary
        electrode_dict = {}

        # Iterate through the DataFrame rows
        for _, row in table.iterrows():
            electrode_num = row['electrode_num']
            coordinates = [row['x(brainLab)'], row['y(brainLab)'], row['z(brainLab)']]
            electrode_dict[electrode_num] = coordinates

        return electrode_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def trans_p_to_XXYY(p, XXsize=6, YYsize=6):
    # Calculate x and y based on the given p, XXsize, and YYsize
    x = (p - 1) % XXsize
    y = YYsize - 1 - (p - 1) // XXsize
    return x, y


def trans_XXYY_to_p(XX, YY, yy_size=6):
    return (XX + 1) + (((yy_size-1) - YY) * yy_size)


def create_mat_from_dict(dict, mat_size=6):
    # init mat
    mat = [[ [['n','n','n'],False] for _ in range(mat_size)] for _ in range(mat_size)]
    keys = list(dict.keys())
    for key in keys:
        p2d = trans_p_to_XXYY(p=key, XXsize=6, YYsize=6)
        mat[p2d[0]][p2d[1]] = dict[key], True
    return mat


def print_mat(mat, size_mat=6):
    for y in range(size_mat):
        for x in range(size_mat):
            if mat[x][y][0] != ['n', 'n', 'n']:
                present_num = [round(num, 2) for num in mat[x][y][0]]
            else:
                present_num = mat[x][y][0]
            print(f"{str(present_num):30}", end=' ')
        print("")  # Move to the next line after each row


def print_positions_from_dict(positions):
    for key, (x, y, z) in positions.items():
        print(f"Electrode {key}: Position (x: {x:.2f}, y: {y:.2f}, z: {z:.2f})")


def get_electrodes_from_file(file_path=r'C:\Users\Yaela Sharon\Documents\LAB\Electrode Mapper\data\test3_Coordinates.xlsx'):
    sheet_name = "CortiQ"
    table = read_excel_table(file_path, sheet_name)

    #Grid
    search_string = 'grid'  # Replace with your actual search string

    if table is None:
        print("Error: Does not find the file (excel)")
        return

    # Filter the table based on acquisition point
    filtered_table = filter_table_by_acquisition_point(table, search_string)

    if filtered_table is None:
        print("Error: Does not find grid electrodes")
        return

    # Create a dictionary of electrode positions
    electrode_dict = create_electrode_dict(filtered_table)

    if electrode_dict is None:
        print("Error: Can not create a dictionary of electrode positions")
        return

    mat = create_mat_from_dict(electrode_dict, mat_size=6)

    return mat
