import pandas as pd
import json
import time
import os

def readFromFile(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        print(f"Contents of '{filename}':")
        return(data)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

def writeToFile(content):
    filename = "descriptive_stats_eval.txt"
    try:
        with open(filename, "x") as file:
            file.write("Descriptive Statistics by Model:\n\n")
            file.write(content)
    except FileExistsError:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        with open(new_filename, "x") as file:
            file.write("Descriptive Statistics by Model:\n\n")
            file.write(content)
        print(f"The file '{new_filename}' was created successfully.")
    else:
        print(f"The file '{filename}' was created successfully.")


data = readFromFile("resultsEval.json")
dataframe = pd.DataFrame(data, columns=["risk", "risk_impact", "risk_likeliness"])
dataframe['risk_impact'] = pd.to_numeric(dataframe['risk_impact'], errors='coerce')
dataframe['risk_likeliness'] = pd.to_numeric(dataframe['risk_likeliness'], errors='coerce')

overall_mean = dataframe[['risk_impact', 'risk_likeliness']].mean().to_frame().T
overall_std = dataframe[['risk_impact', 'risk_likeliness']].std().to_frame().T

grouped = dataframe.groupby("risk")
mean_stats = grouped.mean().reset_index()
std_stats = grouped.std().reset_index()
min_max_stats = grouped.agg(['min', 'max']).reset_index()
min_max_stats.columns = ['_'.join(col).strip('_') for col in min_max_stats.columns.values]

stats = pd.concat([mean_stats, std_stats, min_max_stats, overall_mean, overall_std], 
                  keys=['Mean', 'Std Dev', 'Min', 'Max', 'Overall Mean', 'Overall Std Dev'], 
                  axis=1)

stats_str = stats.to_string()
writeToFile(stats_str)