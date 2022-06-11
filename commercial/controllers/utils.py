import flask

class utils():
  def check_session():
    #throw 403 if user is not logged in
    if flask.session.get('user_id') is None:
      flask.abort(403)