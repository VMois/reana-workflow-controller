# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2017, 2018, 2019, 2020, 2021 CERN.
#
# REANA is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Rest API endpoint for workflow management."""

from __future__ import absolute_import

import logging

from flask import Flask
from reana_commons.config import REANA_LOG_FORMAT, REANA_LOG_LEVEL
from reana_db.database import Session

from reana_db.models import Base  # isort:skip  # noqa


def create_app(config_mapping=None):
    """REANA Workflow Controller application factory."""
    logging.basicConfig(level=REANA_LOG_LEVEL, format=REANA_LOG_FORMAT)
    app = Flask(__name__)
    app.config.from_object("reana_workflow_controller.config")
    if config_mapping:
        app.config.from_mapping(config_mapping)

    app.secret_key = "super secret key"
    # Register API routes
    from reana_workflow_controller.rest import (
        workflows_session,
        workflows_status,
        workflows_workspace,
        workflows,
    )  # noqa

    app.register_blueprint(workflows_session.blueprint, url_prefix="/api")
    app.register_blueprint(workflows.blueprint, url_prefix="/api")
    app.register_blueprint(workflows_status.blueprint, url_prefix="/api")
    app.register_blueprint(workflows_workspace.blueprint, url_prefix="/api")
    app.session = Session
    return app
