from flask import Flask, render_template, request, session, redirect
from read_pcap_file import *
from os.path import exists

app = Flask(__name__)

@app.route('/')
def test():
    file_name = 'test.pcap'
    dataset = read_capture(file_name)[1]
    return render_template('pcap.html', pfname=file_name, data=dataset)

@app.route('/pcap/', methods=['GET'])
def get_pcap_file():
    return render_template('pcap.html')


@app.route('/pcap/', methods=['POST'])
def pcap_analysis():
    file_name = request.form['pcap_file_name_input']
    if "." not in file_name:
        file_name += ".pcap"

    dataset = read_capture(file_name)[1]
    if exists(file_name):
        return render_template('pcap.html', pfname=file_name, data=dataset)
    else:
        return render_template('error.html', message="Error, the file you have tried to use could not be found\n"+app.root_path+"\\"+file_name)




    
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8081)