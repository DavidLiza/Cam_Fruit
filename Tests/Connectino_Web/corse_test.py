from bottle import Bottle, request, run
from truckpad.bottle.cors import CorsPlugin, enable_cors

app = Bottle()

@app.get('/')
def index():
    """
    CORS is disabled for this route
    """
    return "cors is disabled here"

@enable_cors
@app.post('/endpoint_1')
def endpoint_1():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by the plugin itself
    """
    print ('Cors Enabled')
    return "cors is enabled, OPTIONS handled by plugin"

@enable_cors
@app.route('/endpoint_2', method=['GET', 'POST', 'OPTIONS'])
def endpoint_2():
    """
    CORS is enabled for this route. 
    OPTIONS requests will be handled by *you*
    """
    if request.method == 'OPTIONS':
        # do something here?
        pass
    return "cors is enabled, OPTIONS handled by you!"

app.install(CorsPlugin(origins=['*']))

run(app)
