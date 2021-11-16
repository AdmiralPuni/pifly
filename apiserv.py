import flask
import json
import sql

# Create the application.
APP = flask.Flask(__name__)

# Create a URL route in our application for "/"
@APP.route('/')
def home():
  return flask.render_template('index.html')

@APP.route('/chart')
def chart():
  return flask.render_template('chart.html')

@APP.route('/coindata')
def coindata():
  coin = flask.request.args.get('symbol')
  data = sql.select_by_symbol_limit(coin)
  return json.dumps(data)

if __name__ == '__main__':
  APP.run()
