from __future__ import unicode_literals
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter
from klein import Klein
import json
from enchant.checker import SpellChecker
from enchant import DictWithPWL
import difflib


def get_best_word(chkr, word):
  best_words = []
  best_ratio = 0
  a = set(chkr.suggest(word)[0:8])
  for b in a:
    tmp = difflib.SequenceMatcher(None, word, b).ratio()
    if tmp > best_ratio:
      best_words = [b]
      best_ratio = tmp
    elif tmp == best_ratio:
      best_words.append(b)
  print best_words
  return best_words[0]

interpreter = Interpreter.load('models/units/current',RasaNLUConfig('config_units.json'))
    

class Bot:
    '''bot'''
    app = Klein()
    my_dict = DictWithPWL("en_US", "words.txt")
    chkr = SpellChecker(my_dict)


    def __init__(self):
        self.test = 'hi'

    @app.route('/parse',methods=['GET'])
    def parse(self, request):
        '''parser'''
        request.setHeader('Content-Type', 'application/json')
        request_params = {key.decode('utf-8', 'strict'): value[0].decode('utf-8', 'strict')
                              for key, value in request.args.items()}
        text = str(request_params['q']).strip()
        self.chkr.set_text(text)
        
        for err in self.chkr:
          err.replace(get_best_word(self.chkr, err.word))
        
        spell_checked = self.chkr.get_text()
        resp = interpreter.parse(unicode(spell_checked, encoding="utf-8"))
        
        print(resp)
        
        if (float(resp['intent']['confidence']) > 0.5):
            reply = {"intent": resp['intent'], "entities": resp['entities']}
        else:
            reply = {"intent": { "name": "None" }, "entities": ""}


        return json.dumps(dict(reply), indent=4)


if __name__ == '__main__':
    mybot = Bot()
    mybot.app.run('0.0.0.0', 5000)


