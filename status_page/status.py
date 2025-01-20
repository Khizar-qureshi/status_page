import flask
from flask import jsonify
import get_status 
from status_param import IP
from status_param import Https

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():

    status_history_list = get_status.get_status_history(12)
    status_history_list_length = len(status_history_list)
    status_history_percentage = round((sum(status_history_list) / status_history_list_length) * 100, 2) if status_history_list_length > 0 else 0

    vm1_status = 'healthy_container' if get_status.ping_vm_good(IP.VM1_IP) else 'issue_container'
    vm2_status = 'healthy_container' if get_status.ping_vm_good(IP.VM2_IP) else 'issue_container'
    http_status = 'healthy_container' if get_status.update_status() else 'issue_container'
    overall_status = 'issue_container' if vm1_status == 'issue_container' or vm2_status == 'issue_container' or http_status == 'issue_container' else 'healthy_container'

    vm1_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM1_IP) else 'status-circle-issue-container'
    vm2_status_circ = 'status-circle-healthy-container' if get_status.ping_vm_good(IP.VM2_IP) else 'status-circle-issue-container'
    http_status_circ = 'status-circle-healthy-container' if get_status.update_status() else 'status-circle-issue-container'
    login_status_circ = 'status-circle-healthy-container' if get_status.check_login_status() else 'status-cricle-issue-container'

    vm1_check_mark = "✓" if get_status.ping_vm_good(IP.VM1_IP) else "✘"
    vm2_check_mark = "✓" if get_status.ping_vm_good(IP.VM2_IP) else "✘"
    http_check_mark = "✓" if get_status.update_status() else "✘"
    login_status_mark = "✓" if get_status.check_login_status() else "✘"

    html_dict = {
        'overall_status': overall_status,
        'vm1_status': vm1_status,
        'vm2_status': vm2_status,
        'http_status': http_status,
        'vm1_status_circ': vm1_status_circ,
        'vm2_status_circ': vm2_status_circ,
        'http_status_circ': http_status_circ,
        'login_status_circ': login_status_circ,
        'vm1_check_mark': vm1_check_mark,
        'vm2_check_mark': vm2_check_mark,
        'http_check_mark': http_check_mark,
        'login_status_mark': login_status_mark,
        'status_history_list': status_history_list,
        'status_history_list_length': status_history_list_length,
        'status_history_percentage': status_history_percentage,
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