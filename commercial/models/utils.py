import hashlib
import json

class utils():
  def hash(text):
    #use sha3_256
    return hashlib.sha3_256(text.encode('utf-8')).hexdigest()

  def reply(status, code, message):
    return json.dumps({'status': status, 'code': code, 'message': message})