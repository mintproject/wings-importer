# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from importer.server.forms import AddForm
from importer.server.models import Server

from importer.utils import flash_errors

blueprint = Blueprint('server', __name__, url_prefix='/servers', static_folder='../static')


@blueprint.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    servers = current_user.servers.paginate(
        page, 20, False)
    next_url = url_for('index', page=servers.next_num) \
        if servers.has_next else None
    prev_url = url_for('index', page=servers.prev_num) \
        if servers.has_prev else None
    return render_template('servers/index.html', title='Home',
                           servers=servers.items, next_url=next_url,
                           prev_url=prev_url)


@blueprint.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    """Register new user."""
    form = AddForm(request.form)
    if form.validate_on_submit():
        Server.create(server_name=form.server_name.data, server_wings=form.server_wings.data,
                      server_mint=form.server_mint.data, endpoint_mint=form.endpoint_mint.data,
                      wings_username=form.wings_username.data, wings_password=form.wings_password.data,
                      wings_exporturl=form.wings_exporturl.data, user=current_user)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('server.index'))
    else:
        flash_errors(form)
    return render_template('servers/add.html', form=form)
