# myapp/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialToken

class LinkSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        """
        Called before allauth processes social login.
        We link the account to the logged-in user and ensure the token is saved.
        """
        if request.user.is_authenticated:
            # Connect the social account to the logged-in user
            sociallogin.connect(request, request.user)

            # Save the token manually if it's not saved
            token_obj = sociallogin.token
            if token_obj:
                SocialToken.objects.update_or_create(
                    account=sociallogin.account,
                    defaults={
                        'token': token_obj.token,
                        'token_secret': getattr(token_obj, 'token_secret', ''),
                        'expires_at': getattr(token_obj, 'expires_at', None),
                    }
                )
    