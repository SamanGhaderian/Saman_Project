from data_loader import load_patient_data

patient_path = r"c:\users\saman\desktop\sample\252"

df = load_patient_data(patient_path)

print(type(df))
print(df.head())
print(df.columns)