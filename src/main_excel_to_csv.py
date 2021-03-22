import os
from functions_excel_to_csv import *
from variables_excel_to_csv import *

def main():
    #ask if csv files should be removed (in case new excel files have been uploaded)
    options = ["y", "n"]
    trigger=True
    while trigger==True:
        erase_csv = input("Do you want to remove CSV files? (y/n): ").lower()
        if erase_csv in options:
            trigger=False

    #defining variables

    xlsx_path = read_path(input_all_paths, "xlsx_files")
    csv_path = read_path(input_all_paths, "csv_output")
    output_path = read_path(input_all_paths, "output")
    check_path = read_path(input_all_paths, "check_txt")

    #delete files in csv in case there are any
    if erase_csv=="y":
        for f in os.listdir(csv_path):
            os.remove(os.path.join(csv_path, f))
    
    #convert all files to csv
    xlsx_to_csv(xlsx_path, csv_path, dtypes_sap, fechas)

    #defining path for check txt
    check_file = os.path.join(check_path, "check.txt")

    #deleting previous reports
    for f in os.listdir(check_path):
        os.remove(os.path.join(check_path, f))

    #open and concat all files
    list_df = []
    for f in os.listdir(csv_path):
        print(f"Processing {f}")
        path_file = os.path.join(csv_path, f)
        df = pd.read_csv(path_file, dtype=dtypes_sap, parse_dates=fechas)

        #checking if file name is equal to column Posición liquidez
        file_name = f[:-4]
        posicion_liquidez=list(df['Liquidity Item'].unique())
        with open(check_file, "a") as txt:
            if len(posicion_liquidez) > 1:
                txt.write(f+" Posición liquidez tiene más de un valor único.\n")
            elif len(posicion_liquidez) == 0:
                txt.write(f+" Posición liquidez no tiene valores.\n")
            elif file_name != posicion_liquidez[0]:
                txt.write(f+" Posición liquidez no coincide con nombre fichero. Valor encontrado: "+posicion_liquidez[0]+"\n")

        print(f"{f} processed.")
        #appending df to list
        list_df.append(df)

    df_final = pd.concat(list_df)

    print("Generating csv...")
    final_file_path=os.path.join(output_path, "OA_consolidated.csv")
    df_final.to_csv(final_file_path, index=False)
    print("CSV Generated.")

if __name__=="__main__":
    main()