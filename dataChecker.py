import os
all_files = os.listdir("./data")    
csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))