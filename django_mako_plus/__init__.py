#
#   Author:  Conan Albrecht <ca&byu,edu>
#   License: Apache Open Source License
#


# pointer to our app config
# Django looks for this exact variable name
default_app_config = 'django_mako_plus.Config'


# the version
from .version import __version__


# our app config
from .apps import Config


# the exceptions
from .exceptions import InternalRedirectException
from .exceptions import RedirectException


# the router
from .router import view_function
from .router import route_request


# the middleware
from .middleware import RequestInitMiddleware


# the template engine
from .template import MakoTemplates
from .template import get_template_lookup
from .template import get_app_template_lookup
