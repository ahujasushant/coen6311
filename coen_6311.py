from coen_6311 import __init__, db
from coen_6311.models import Volunteer, Organization, Post, History


@__init__.shell_context_processor
def make_shell_context():
    return {'db': db, 'Volunteer': Volunteer, 'Organization': Organization, 'Post': Post, 'History': History}
