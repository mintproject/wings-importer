# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from importer.mint.forms import ImportComponentForm
from importer.server.models import Server
blueprint = Blueprint('mint', __name__, url_prefix='/mint', static_folder='../static')


@blueprint.route('/components/')
@login_required
def index():
    grlc = "http://ontosoft.isi.edu:8001/api/mintproject/MINT-ModelCatalogQueries/getModelConfigurations?endpoint"
    endpoint = "http://ontosoft.isi.edu:3030/ds/query"
    headers = {'accept': 'application/json'}
    url = "%s=%s" %(grlc, endpoint)
    resp = self.session.get(url, headers=headers)
    self.check_request(resp)
    return resp.json()


def import_component(instance, server, password):
    return True


@blueprint.route('/components/add')
@login_required
def add():
    """Import a new component."""
    available_servers = current_user.servers.all()
    form = ImportComponentForm(request.form)
    form.server.choices = [(i.id, i.server_name) for i in available_servers]
    if form.validate_on_submit():
        if import_component(form.component, form.component):
            flash('Component was imported.', 'success')
        return redirect(url_for('server.index'))


    return render_template('components/add.html', form=form)


def check_request(self, resp):
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.RequestException as err:
        print(err)
    return resp
