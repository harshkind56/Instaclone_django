from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied


class FilterRequestMiddleware(MiddlewareMixin):

    def process_request(self,request):

        print("inside process request.")

        allowed_ips = ['192.168.1.1']


        print(request.META.get('HTTP_USER_AGENT'))

        ip = request.META.get('REMOTE_ADDR')

        if ip not in allowed_ips:

            raise PermissionDenied
        
        return None
    


