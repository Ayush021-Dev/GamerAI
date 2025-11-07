from flask import Blueprint

# Create the blueprint with the URL prefix
tic_tac_toe_bp = Blueprint(
    'tic_tac_toe', 
    __name__,
    template_folder='templates',
    url_prefix='/tic-tac-toe'
)

# Import routes
from . import routes