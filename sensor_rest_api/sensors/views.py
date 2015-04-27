from django.shortcuts import render
from django.db import transaction
from rest_framework.authtoken.models import Token

from sensors.models import SensorVerification


def verify(request):

    code = request.GET.get('code')

    print code

    if code is None:
        return render(request, 'sensors/error.html',
                      {'message': 'The page requested was not found'})
    else:
        try:
            verify = SensorVerification.objects.get(verification_code=code)

            if verify.verified:
                return render(request, 'sensors/error.html',
                              {'message': 'This verification code is already used. If you look for the API token, check your email.'})
            else:
                with transaction.atomic():
                    verify.verified = True
                    verify.account.is_active = True
                    verify.save()
                    verify.account.save()

                    # Create token
                    token = Token.objects.get_or_create(user=verify.account)

                    # Activate user account

                    # Send Token Email

                    return render(request, 'sensors/verify.html', {'verify': verify, 'token': token[0].key})

        except SensorVerification.DoesNotExist:
            return render(request, 'sensors/error.html',
                          {'message': 'The verification code is invalid'})


