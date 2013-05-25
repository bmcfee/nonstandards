#!/usr/bin/env python

import flask
import ConfigParser
import sys

DEBUG = True
SECRET_KEY = 'yodawg'

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


@app.route('/', methods=['GET'])
def index():
    '''Top-level web page'''

    return flask.make_response(flask.render_template('index.html'))


# Main block
if __name__ == '__main__':
    CFG = loadConfig(sys.argv[1])
#     run()
    run(host='0.0.0.0')


