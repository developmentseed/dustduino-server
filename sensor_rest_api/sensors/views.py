from django.shortcuts import render
from django.db import transaction
from rest_framework.authtoken.models import Token

from sensors.models import SensorVerification, Sensor
from api.v1.mailer import TokenEmail


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
                return render(
                    request,
                    'sensors/error.html',
                    {
                        'message': 'This verification code is already used. If you look for the API token, ' +
                                   'check your email.'
                    }
                )
            else:
                with transaction.atomic():
                    verify.verified = True
                    verify.save()
                    # Activate user account
                    verify.account.is_active = True
                    verify.account.save()

                    # Create token
                    token = Token.objects.get_or_create(user=verify.account)

                    # Send Token Email
                    sensor = Sensor.objects.get(account=verify.account)

                    mail = TokenEmail(verify.account.email, token[0].key, sensor.sensor_name)
                    mail.send()

                    return render(request, 'sensors/verify.html', {'verify': verify,
                                                                   'token': token[0].key,
                                                                   'sensor': sensor})

        except SensorVerification.DoesNotExist:
            return render(request, 'sensors/error.html',
                          {'message': 'The verification code is invalid'})


