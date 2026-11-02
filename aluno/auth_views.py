from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


class UsernameOrEmailAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            if "@" in username:
                users = list(
                    get_user_model()._default_manager.filter(
                        email__iexact=username
                    )[:2]
                )
                if len(users) == 1:
                    username = users[0].get_username()

            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class RememberMeLoginView(LoginView):
    authentication_form = UsernameOrEmailAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        self.request.session.set_expiry(
            None if self.request.POST.get("remember") == "1" else 0
        )
        return response
