from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.utils.translation import gettext as _
from rest_framework.exceptions import ErrorDetail

def get_first_error_message(detail, field_name=None):
    """Extract the first error message from nested errors (now tracks field names)"""

    if isinstance(detail, list):
        for item in detail:
            result = get_first_error_message(item, field_name)
            if result and result != _("An error occurred"):
                return result
        return _("An error occurred")

    if isinstance(detail, dict):
        # Prioritize `non_field_errors` or `detail`
        for key in ['non_field_errors', 'detail']:
            if key in detail:
                result = get_first_error_message(detail[key], field_name)
                if result and result != _("An error occurred"):
                    return result

        # Process field-specific errors
        for key in detail:
            result = get_first_error_message(detail[key], key)  # Pass key as field name
            if result and result != _("An error occurred"):
                return result

        return _("An error occurred")

    if isinstance(detail, ErrorDetail):
        # Add field name to "required" errors
        if detail.code == 'required' and field_name:
            return _(f"The field '{field_name}' is required.")
        return str(detail)

    return _("An error occurred")


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        first_error = get_first_error_message(response.data)  # Extract main message
        response.data = {
            "message": first_error,  # Single-line user-friendly message
            "errors": response.data  # Full error details for debugging
        }

    return response






















































































# from rest_framework.views import exception_handler
# from rest_framework.response import Response
# from django.utils.translation import gettext as _
# from rest_framework.exceptions import ErrorDetail

# def get_first_error_message(detail, field_name=None):
#     """Extract the first error message from nested errors (now tracks field names)"""
#     print("$$$$$$$$$$$$$", detail)
#     if isinstance(detail, list):
#         for item in detail:
#             result = get_first_error_message(item, field_name)
#             if result != _("An error occurred"):
#                 return result
#         return _("An error occurred")
    
#     if isinstance(detail, dict):
#         # Check standard keys first
#         for key in ['non_field_errors', 'detail']:
#             if key in detail:
#                 result = get_first_error_message(detail[key], field_name)
#                 if result != _("An error occurred"):
#                     return result
#         # Process field-specific errors
#         for key in detail:
#             result = get_first_error_message(detail[key], key)  # Pass key as field name
#             if result != _("An error occurred"):
#                 return result
#         return _("An error occurred")
    
#     if isinstance(detail, ErrorDetail):
#         # Add field name to "required" errors
#         if detail.code == 'required' and field_name:
#             return _(f"The field {field_name} is required.")
#         return str(detail)
    
#     return _("An error occurred")





# def custom_exception_handler(exc, context):
#     response = exception_handler(exc, context)
    
#     if response is not None:
#         message = get_first_error_message(response.data)
#         response.data = {'message': message}
    
#     return response