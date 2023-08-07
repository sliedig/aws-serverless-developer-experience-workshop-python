# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os

from unittest import mock
from importlib import reload

from .lambda_context import LambdaContext
from .helper import load_event, return_env_vars_dict, create_ddb_table_property_web


@mock.patch.dict(os.environ, return_env_vars_dict(), clear=True)
def test_property_approved(dynamodb, mocker):
    eventbridge_event = load_event('events/property_approved.json')
    property_id = eventbridge_event['detail']['property_id']

    import  approvals_service.publication_approved_event_handler as app
    reload(app) # Reload is required to prevent function setup reuse from another test 

    create_ddb_table_property_web(dynamodb)

    context = LambdaContext()
    ret = app.lambda_handler(apigw_event, context)  # type: ignore
    assert 'result' in ret
    result = ret['result']
    assert "success" in result.lower()
