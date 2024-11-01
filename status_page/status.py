import flask
import get_status


VM1_IP = '52.225.235.130'
VM2_IP = '65.52.239.81'
app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/') 
def home():
    if (get_status.ping_vm_good(VM1_IP)):
        vm1_status = 'current_status_container'
    else:
        vm1_status = 'issue_container'
        
    if (get_status.ping_vm_good(VM2_IP)):
        vm2_status = 'current_status_container'
    else:
        vm2_status = 'issue_container'
        
    html_dict = {'vm1_status': vm1_status, 'vm2_status': vm2_status}
    return flask.render_template('index.html', **html_dict)


    

if __name__ == '__main__':
    app.run(debug = True)