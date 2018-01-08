
title: Binding and registering the device after verifying the activation code
description: As a new visitor I have to bind my device with activation code and phone number.

Given:

  url: /apiv1/devices/name: SM-12345678
  as: visitor
  verb: BIND
  form:
    activationCode: '746727'
    phone: '+9897654321'

Then status is 200 OK
And response content type is application/json
And response body is JSON like:

  {
    "id": 1,
    "name": "SM-12345678"
  }

And headers contains:
  - 'Content-Type: application/json; charset=utf-8'

