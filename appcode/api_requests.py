from flask import request
from flask import Blueprint

from config import Constants
import appcode.credentials as credentials
import appcode.scrappers.sabadell_scrapper as sabadell_scrapper

from appcode.exceptions import ValidationException
from appcode.exceptions import ParameterException
from appcode.exceptions import isException

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/set-credentials", methods=['GET'])
def setCredentials():
    expectedArgs = ['bank', 'user', 'pass']
    action = credentials.encryptCredentials
    return _sendRequest(request.args, expectedArgs, action)

@api_bp.route("/get-transactions", methods=['GET'])
def getBankMovements():
    expectedArgs = None
    action = sabadell_scrapper.getTransactions
    return _sendRequest(request.args, expectedArgs, action)

def _getRequestArgs(requestArgs, expectedArgs):

    # If there are no expected args, returns None
    if expectedArgs is None: return None

    # Get list of args
    args = {}

    for expectedArg in expectedArgs:
        arg = requestArgs.get(expectedArg)

        # Checks if any parameter is missing or blank
        if (arg is None):
            return ParameterException('Missing parameter.')
        if (arg == ""):
            return ParameterException('Parameters cannot be blank.')

        # Appends the arg as expected
        args[expectedArg] = arg

    return args

def _validateApiToken(requestToken):
    # Checks the facilitated API Token against the one stored in the secrets file
    apiToken = Constants.get('API_TOKEN', "s")

    if (apiToken is None):
        return ValidationException('API Token is missing. Check your APP configuration!')
    if (requestToken == "" or requestToken != apiToken):
        return ValidationException('Wrong API Token. Get out, creep!')

def _sendRequest(requestArgs, expectedArgs, action):

    # Validates the access token
    validation = _validateApiToken(requestArgs.get('token'))
    if isException(validation): return validation

    # Gets the request args
    args = _getRequestArgs(request.args, expectedArgs)
    if isException(args): return args

    return action(args)

