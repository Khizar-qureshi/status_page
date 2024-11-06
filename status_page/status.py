import flask
from flask import jsonify
import get_status 
from status_param import IP

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():
    vm1_status = 'current_status_container' if get_status.ping_vm_good(IP.VM1_IP) else 'issue_container'
    vm2_status = 'current_status_container' if get_status.ping_vm_good(IP.VM2_IP) else 'issue_container'
    http_status = 'current_status_container' if get_status.update_status() else 'issue_container'
        
    html_dict = {'vm1_status': vm1_status, 'vm2_status': vm2_status, 'http_status': http_status}
    return flask.render_template('index.html', **html_dict) 

@app.route('/status', methods=['GET'])
def get_status_data():
    vm1_status = 'current_status_container' if get_status.ping_vm_good(IP.VM1_IP) else 'issue_container'
    vm2_status = 'current_status_container' if get_status.ping_vm_good(IP.VM2_IP) else 'issue_container'
    http_status = 'current_status_container' if get_status.update_status() else 'issue_container'

    status_data = {
        'vm1_status': vm1_status,
        'vm2_status': vm2_status,
        'http_status': http_status
    }
    
    return jsonify(status_data)

if __name__ == '__main__':
    app.run(debug = True)