import requests
from json import JSONDecodeError
import json
from flask import jsonify
class BadRequest(Exception):
    pass
 
#Here We used decorator to set up to handle these exceptions and return appropriate HTTP status codes and error messages.
def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
       

        #If We Pass Invalid Data, Invalid Request Invalid Token BadRequest Error Will Be Raised
        except BadRequest as e:
            return jsonify({"error": str(e)}), 400
        #To Handle The TypeError
        except TypeError as e:
            return jsonify({"error": "Invalid input: " + str(e)}), 400
       
        #To Handle The AttributeError
        except AttributeError as e:return jsonify({"error": "Internal error: " + str(e)}), 500
 
        #To Handle The Key Error
        except KeyError:
            return jsonify({"error": "The key does not exist in the request data"}), 400
       
        #To Handle The ValueError
        except ValueError as e:
            return jsonify({"error": "Invalid value: " + str(e)}), 400
       
        #If a request times out.
        except requests.exceptions.Timeout as e:
            return jsonify(f"Request timed out: {e}")
       
        #The server is not reachable or is down, The client is not connected to the internet, The request timed out.
        except requests.exceptions.RequestException as e:
            return jsonify({"error": str(e)}), 500
       
        #If we pass invalid json data, JSONDecodeError will be raised
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON"}), 500
       
        #If JSON file not found, FileNotFoundError will be raised
        except FileNotFoundError:
            return jsonify({"error": "JSON file not found"}), 404
       
        #Generic Exception
        except Exception as e:
            return jsonify({"error": str(e)}), 500
       
    return wrapper
