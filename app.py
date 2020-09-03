import os
import csv
import re
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, send_file, render_template
import pandas as pd
import numpy as np

UPLOAD_FOLDER = 'uploads/'

try:
    os.mkdir(UPLOAD_FOLDER)
except OSError:
    print("")
else:
    print("")

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/details')
def details():
    return render_template('details.html')
 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # print("saved file successfully")
            # print(filename)
            df = pd.read_csv(filename)
            df = pd.DataFrame(df)
            df.columns = df.columns.str.replace(' ', '_')
            data = df.loc[:, [
                'm/z', 'Retention_time_(min)', 'Accepted_Compound_ID']]
            print(data.dtypes)
            data['Accepted_Compound_ID'] = data['Accepted_Compound_ID'].str.replace(
                ":", "_")
            data['Accepted_Compound_ID'] = data['Accepted_Compound_ID'].str.replace(
                " ", "_")
            print(data['Accepted_Compound_ID'])
  
            search_pc = "PC"
            ids_with_pc = data['Accepted_Compound_ID'].str.endswith(
                search_pc, na=False)
            PC_dataset = data[ids_with_pc]
            PC_dataset.to_csv('uploads\metabolies_ending_with_PC.csv')
            # print(PC_dataset)

            search_lpc = "LPC"
            ids_with_pc = data['Accepted_Compound_ID'].str.endswith(
                search_lpc, na=False)
            LPC_dataset = data[ids_with_pc]
            LPC_dataset.to_csv('uploads\metabolies_ending_with_LPC.csv')
            # print(LPC_dataset)

            search_plasmalogen = "plasmalogen"
            ids_with_pc = data['Accepted_Compound_ID'].str.endswith(
                search_plasmalogen, na=False)
            Plasmalogen_dataset = data[ids_with_pc]
            Plasmalogen_dataset.to_csv(
                'uploads\metabolies_ending_with_Plasmalogen.csv')
            # print(Plasmalogen_dataset)
            # print(type(Plasmalogen_dataset))

            # 2

            RetentionRoundOff = data['Retention_time_(min)'].round(0)
            df['Retention_Rounded_off_(min)'] = RetentionRoundOff
            df.to_csv('uploads\original.csv')

            # 3
            data.drop(data.columns[[0, 2]], axis=1, inplace=True)
            data['Retention_time_(min)'] = data['Retention_time_(min)'].round(0)
            data['Retetion_time_mean']= data['Retention_time_(min)'].unique().mean()
            data.to_csv('uploads\sol3_data.csv')
            return render_template('details.html', value=filename)
    redirect('details.html')
 
    return render_template('upload_file.html')


@app.route('/one_pc', methods=['GET', 'POST'])
def one_pc():
    data = [] 
    with open('uploads/metabolies_ending_with_PC.csv') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            data.append(row)
    return render_template('one_pc.html', data=data)
    
@app.route('/one_lpc', methods=['GET', 'POST'])
def one_lpc():
    data = [] 
    with open('uploads/metabolies_ending_with_PC.csv') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            data.append(row)
    return render_template('one_lpc.html', data=data)

@app.route('/one_plasma', methods=['GET', 'POST'])
def one_plasma():
    data = [] 
    with open('uploads/metabolies_ending_with_Plasmalogen.csv') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            data.append(row) 
    return render_template('one_plasma.html', data=data)
    # return render_template('one_pc.html')


@app.route('/two', methods=['GET', 'POST'])
def two():
    data = []
    with open('uploads/original.csv') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            data.append(row)
    return render_template('two.html', data=data)
 
@app.route('/three', methods=['GET', 'POST'])
def three():
    data = []
    with open('uploads/sol3_data.csv') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            data.append(row)
    return render_template('three.html', data=data)

@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
    return render_template('download.html', value=filename)


@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')


if __name__ == "__main__":
    app.run(debug=True)
