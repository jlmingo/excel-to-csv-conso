import pandas as pd
import os

def xlsx_to_csv(input_path, output_path, dtypes_sap):
    files_input = os.listdir(input_path)
    files_output = os.listdir(output_path)
    for f in files_input:
        file_name = str(f[:-4])
        if file_name+"csv" not in files_output:
            df = pd.read_excel(os.path.join(input_path, f), dtype=dtypes_sap)
            file_name = file_name+"csv"
            df.to_csv(os.path.join(output_path, file_name))
            print(str(file_name)+" created")

def read_path(input_all_paths, denomination):
    df = pd.read_excel(input_all_paths, sheet_name="inputs")
    return df[df.denomination==denomination].path.iloc[0]