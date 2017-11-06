from __future__ import unicode_literals
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter
from klein import Klein
import json

interpreter = Interpreter.load('models/units/current',RasaNLUConfig('config_units.json'))
    

class Bot:
    '''bot'''
    app = Klein()

    def __init__(self):
        self.test = 'hi'

    @app.route('/parse',methods=['GET'])
    def parse(self, request):
        '''parser'''
        request.setHeader('Content-Type', 'application/json')
        request_params = {key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict')
                              for key, value in request.args.items()}
        text = str(request_params['q']).strip()
        resp = interpreter.parse(unicode(text, encoding="utf-8"))
        
        print(resp)
        
        if (float(resp['intent']['confidence']) > 0.5):
            reply = {"intent": resp['intent'], "entities": resp['entities']}
        else:
            reply = {"intent": { "name": "None" }, "entities": ""}

        return json.dumps(dict(reply), indent=4)


if __name__ == '__main__':
    mybot = Bot()
    mybot.app.run('0.0.0.0', 5000)


