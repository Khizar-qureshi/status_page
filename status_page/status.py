import flask
from flask import jsonify
import get_status 
from status_param import IP
from status_param import Https

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():
    #Evantually the vm1_status, vm2_Status, and http_status will be deleted 
    vm1_status = 'healthy_container' if get_status.ping_vm_good(IP.VM1_IP) else 'issue_container'
    vm2_status = 'healthy_container' if get_status.ping_vm_good(IP.VM2_IP) else 'issue_container'
    http_status = 'healthy_container' if get_status.update_status() else 'issue_container'
    overall_status = 'issue_container' if vm1_status == 'issue_container' or vm2_status == 'issue_container' or http_status == 'issue_container' else 'healthy_container'
     
    vm1_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM1_IP) else 'status-circle-issue-container'
    vm2_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM2_IP) else 'status-circle-issue-container'
    http_status_circ = 'status-circle-healthy-container' if get_status.update_status() else 'status-circle-issue-container' 
     
       
    html_dict = {'overall_status': overall_status, 'vm1_status': vm1_status, 'vm2_status': vm2_status, 'http_status': http_status, 
                 'vm1_status_circ' : vm1_status_circ, 'vm2_status_circ': vm2_status_circ, 'http_status_circ': http_status_circ}
    return flask.render_template('index.html', **html_dict) 


# Useful for refresh every hour for the bots, will have to be updated later.
@app.route('/status', methods=['GET'])
def get_status_data():
    http_status_info = get_status.check_http_status(Https.url_home)
    status_data = {
        'vm1_status': 'healthy_container' if get_status.ping_vm_good(IP.VM1_IP) else 'issue_container',
        'vm2_status': 'healthy_container' if get_status.ping_vm_good(IP.VM2_IP) else 'issue_container',
        'http_status': 'healthy_container' if get_status.update_status() else 'issue_container',
        'http_status_message': http_status_info['message'] 
    }
    return jsonify(status_data)

if __name__ == '__main__':
    app.run(debug = True)