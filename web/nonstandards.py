#!/usr/bin/env python

import flask
import ConfigParser
import sys

import cPickle as pickle

DEBUG = True
SECRET_KEY = 'yodawg'

HMM = None

# construct application object
app = flask.Flask(__name__)
app.config.from_object(__name__)

def loadConfig(server_ini):
    P       = ConfigParser.RawConfigParser()

    P.opionxform    = str
    P.read(server_ini)

    CFG = {}
    for section in P.sections():
        CFG[section] = dict(P.items(section))

    for (k, v) in CFG['server'].iteritems():
        app.config[k] = v
    
    return CFG


def run(**kwargs):
    app.run(**kwargs)

def make_chord_sequence(H, n, num_to_chord):
    '''Sample a chord progression
    
    Arguments:
        H  -- (sklearn.hmm.MultinomialHMM)  the trained model
        n  -- (int>0) length of the progression to generate
        num_to_chord -- (list) mapping of chord numbers to labels

    Returns:
        S  -- (list of str) the generated sequence
    '''

    return map(lambda x: num_to_chord[x], H.sample(n)[0])

@app.route('/', methods=['GET'])
def index():
    '''Top-level web page'''

    return flask.make_response(flask.render_template('index.html'))

@app.route('/lead')
def lead():
    '''Lead-sheet generator'''

    return str(make_chord_sequence(HMM['H'], 8, HMM['num_to_chord']))

def loadHMM(filepath):

    global HMM

    with open(filepath, 'r') as f:
        HMM = pickle.load(f)


# Main block
if __name__ == '__main__':
    CFG = loadConfig(sys.argv[1])
#     run()
    loadHMM(app.config['hmm'])

    run(host='0.0.0.0')

