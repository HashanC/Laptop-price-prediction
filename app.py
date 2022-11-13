from flask import Flask, render_template, request
import pickle
import numpy as np

# setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    # return "Hello World"
    pred_value = 0
    if request.method == 'POST':
        ram = request.form['ram']
        weight = request.form['weight']

        x_res =float(request.form['x_res'])
        y_res =float(request.form['y_res'])
        inches =float(request.form['inches'])


        hardware_capacity= request.form['hardware_capacity']
        hdd = request.form.getlist('hdd')
        ssd = request.form.getlist('ssd')

        

        def applyHard (hdd_ , ssd_ , capacity):
            HDD =0
            SSD =0
            if hdd_==1:
                HDD=capacity
            elif ssd_==1:
                SSD=capacity
            else:
                HDD =0
                SSD =0
            return HDD,SSD

        hard= list(applyHard(len(hdd),len(ssd),hardware_capacity))

        HDD = hard[0]
        SSD = hard[1]




        # HDD = request.form['HDD']
        # SSD = request.form['SSD']

        company = request.form['company']
        typename = request.form['typename']
        opsys = request.form['opsys']
        cpu = request.form['cpuname']
        gpu = request.form['gpuname']
        touchscreen = request.form.getlist('touchscreen')
        ips = request.form.getlist('ips')
        
        feature_list = []

        feature_list.append(int(ram))
        feature_list.append(float(weight))
        
        feature_list.append(len(touchscreen))
        feature_list.append(len(ips))

        ppi = (np.square((x_res*x_res) + (y_res*y_res)))/inches 

        feature_list.append(float(ppi))
        feature_list.append(int(HDD))
        feature_list.append(int(SSD))

        company_list = ['acer','apple','asus','dell','hp','lenovo','msi','other','toshiba']
        typename_list = ['2in1convertible','gaming','netbook','notebook','ultrabook','workstation']
        opsys_list = ['os_Others/No OS/Linux','mac','windows']
        cpu_list = ['amd','intelcorei3','intelcorei5','intelcorei7','other']
        gpu_list = ['amd','intel','nvidia']

        # for item in company_list:
        #     if item == company:
        #         feature_list.append(1)
        #     else:
        #         feature_list.append(0)

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        
        traverse_list(company_list, company)
        traverse_list(typename_list, typename)
        traverse_list(opsys_list, opsys)
        traverse_list(cpu_list, cpu)
        traverse_list(gpu_list, gpu)

        pred_value = prediction(feature_list)
        
        pred_value = np.exp(pred_value)*321 
        pred_value = np.round(pred_value[0],2)   

    return render_template('index2.html', pred_value=pred_value)


if __name__ == '__main__':
    app.run(debug=True)
      