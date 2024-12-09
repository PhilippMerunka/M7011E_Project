from django.shortcuts import redirect

def verify_2fa_for_oauth(backend, user, **kwargs):
    if user and hasattr(user, 'profile') and user.profile.two_fa_enabled:
        # Save the user ID in the session for 2FA verification
        backend.strategy.request.session['pre_2fa_user'] = user.id
        return redirect('verify_2fa')  # Redirect to your 2FA verification view
