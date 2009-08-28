import warnings
warnings.simplefilter('ignore', Warning)

from django.conf import settings

from core.tests.backends import *
from core.tests.fields import *
from core.tests.forms import *
from core.tests.indexes import *
from core.tests.models import *
from core.tests.query import *
from core.tests.sites import *
from core.tests.views import *

if settings.HAYSTACK_SEARCH_ENGINE in ('solr',):
    from core.tests.templatetags import *
