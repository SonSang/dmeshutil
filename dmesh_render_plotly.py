import os
from dmeshutil.dmesh import DMesh

# list all files in "data" folder
data_files = os.listdir("data")

for data_file in data_files:
    data_path = f"data/{data_file}"
    output_path = "output"

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    dmesh = DMesh.load(data_path)
    dmesh.render_plotly(0.01, f"output/{data_file.split('.')[0]}.html")