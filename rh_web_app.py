from flask import Flask
from flask import request
import rainbowhat as rh
app = Flask(__name__)

@app.route("/")
def hello():
    led = int(request.args.get('led', '-1'))
    rh.rainbow.set_all(0, 0, 0)
  
    if led >= 0 and led <= 6:
        rh.rainbow.set_pixel( led, 255, 0, 255 )
    
    rh.rainbow.show()
    
    return "Hello World!"

if __name__ == '__main__':
    app.run( debug = True, host='0.0.0.0' )