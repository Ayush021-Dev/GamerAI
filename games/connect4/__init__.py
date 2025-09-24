from flask import Blueprint

# Create the blueprint with the URL prefix
# This is the key change!
connect4_bp = Blueprint(
    'connect4', 
    __name__,
    template_folder='templates',
    url_prefix='/connect4'
)

# Import routes after blueprint creation to avoid circular imports
from . import routes