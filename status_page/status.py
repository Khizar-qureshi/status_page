import flask
from flask import jsonify
import get_status 
from status_param import IP
from status_param import Https

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():
    vm1_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM1_IP) else 'status-circle-issue-container'
    vm2_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM2_IP) else 'status-circle-issue-container'
    http_status_circ = 'status-circle-healthy-container' if get_status.update_status() else 'status-circle-issue-container'
    login_status_circ = 'status-circle-healthy-container' if get_status.check_login_status()['status'] else 'status-circle-issue-container'
    register_status_circ = 'status-circle-healthy-container' if get_status.check_register_status() else 'status-circle-issue-container'
    overall_status = 'issue_container' if 'issue' in vm1_status_circ or 'issue' in vm2_status_circ or 'issue' in http_status_circ or 'issue' in login_status_circ or 'issue' in register_status_circ else 'healthy_container'

    vm1_check_mark = "✓" if get_status.ping_vm_good(IP.VM1_IP) else "✘"
    vm2_check_mark = "✓" if get_status.ping_vm_good(IP.VM2_IP) else "✘"
    http_check_mark = "✓" if get_status.update_status() else "✘"
    login_check_mark = "✓" if 'healthy' in login_status_circ else "✘"
    register_check_mark = "✓" if 'healthy' in register_status_circ else "✘"
    

    html_dict = {
        'overall_status': overall_status,
        'vm1_status_circ': vm1_status_circ,
        'vm2_status_circ': vm2_status_circ,
        'http_status_circ': http_status_circ,
        'login_status_circ': login_status_circ,
        'vm1_check_mark': vm1_check_mark,
        'vm2_check_mark': vm2_check_mark,
        'http_check_mark': http_check_mark,
        'login_status_mark': login_check_mark,
        'register_status_circ': register_status_circ,
        'register_check_mark': register_check_mark,
    }

    return flask.render_template('index.html', **html_dict)

@app.route('/status')
def status():
    get_status.update_status()
    home_status = get_status.status_data["home"]["status"]
    flask_status_code = home_status["code"]

    data = {
        "http_status_message": home_status["message"]
    }

    return jsonify(data), flask_status_code

if __name__ == '__main__':
    app.run(debug = True)