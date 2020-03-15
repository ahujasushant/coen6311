from app import __init__, db
from app.models import Volunteer, Organization, Post


@__init__.shell_context_processor
def make_shell_context():
    return {'db': db, 'Volunteer': Volunteer, 'Organization': Organization, 'Post': Post}