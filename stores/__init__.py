import os

# Keep a setting for the path to the templates in case a project subclasses the
# models and still needs to use the templates
#
# Imitate how django-oscar did it. But in djaon-oscar,
#   1.) use the default behavior of django.template.loaders.app_directories.Loader
#   2.) OSCAR_MAIN_TEMPLATE_DIR
#
# However, in stores case, the stores app may not be loaded into the main application.
#

OSCAR_STORES_DEFAULT_TEMPLATE_DIR      = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates')

OSCAR_STORES_MAIN_TEMPLATE_DIR      = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'templates/oscar')