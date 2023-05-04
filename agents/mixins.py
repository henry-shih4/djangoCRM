from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


class OrganisorAndLoginRequiredMixin(AccessMixin):
        ##verify that current user is authenticated and is an organisor##
        def dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated or not request.user.is_organisor:
                return redirect('leads:leadList')
            return super().dispatch(request, *args, **kwargs)
