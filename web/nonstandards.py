#!/usr/bin/env python

import flask
import ConfigParser
import sys
import os

import cPickle as pickle

DEBUG = True
SECRET_KEY = 'yodawg'

HMM = None

# construct application object
app = flask.Flask(__name__)
app.config.from_object(__name__)

def loadConfig(server_ini):
    P       = ConfigParser.RawConfigParser()

    P.optionxform    = str
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

    return [num_to_chord[x] for x in H.sample(n)[0]]

@app.route('/health-check', methods=['GET'])
def healthcheck():
    return {'status': 'OK'}


@app.route('/')
def index():
    '''Top-level web page'''

    return flask.make_response(flask.render_template('index.html'))

@app.route('/lead')
def lead():
    '''Lead-sheet generator'''

    A = make_chord_sequence(HMM['H'], 8, HMM['num_to_chord'])
    B = make_chord_sequence(HMM['H'], 8, HMM['num_to_chord'])

    sequence = [A, A, B, A]
    return str(sequence)

def loadHMM(filepath):

    global HMM

    with open(filepath, 'r') as f:
        HMM = pickle.load(f)


# Main block
if __name__ == '__main__':
    CFG = loadConfig(sys.argv[1])
#     run()
    loadHMM(app.config['hmm'])

    port = 5000
    if os.environ.get('ENV') == 'production':
        port = 80

    run(host='0.0.0.0', port=port)

