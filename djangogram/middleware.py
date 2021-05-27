# Django
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

# Utils
from datetime import datetime, timedelta

class ProfileCompletion:
    """Profile completion middleware.

    Ensure every user that is interacting with the platform
    have their profile picture and biography.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                if not profile.picture or not profile.biography:
                    if request.path not in [reverse('users:update_profile'), reverse('users:logout')]:
                        return redirect('users:update_profile')

        response = self.get_response(request)
        return response


class AutoLogout:
    """Autologout middleware
    
    It closes the session after certain amount of minutes
    defined in the variable AUTO_LOGOUT_DELAY in settings
    """
    def __init__(self, get_response):
        self.response = get_response


    def __call__(self, request):
        if not request.user.is_authenticated:
            # Can't log out if not logged in
            response = self.response(request)
            return response

        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
                del request.session['last_touch']
                return redirect('users:logout')
        except KeyError:
            pass

        request.session['last_touch'] = datetime.now()

        response = self.response(request)
        return response