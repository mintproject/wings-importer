# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from importer.mint.forms import ImportComponentForm
from importer.server.models import Server
from wings import mint as mintAPI
from wings import wings as wingsAPI
import requests
import shutil

blueprint = Blueprint('mint', __name__, url_prefix='/mint', static_folder='../static')


@blueprint.route('/components/add', methods=['GET', 'POST'])
@login_required
def add():
    """Import a new component."""
    available_servers = Server.query.filter(Server.is_public | (Server.user == current_user)).all()
    form = ImportComponentForm(request.form)
    form.server.choices = [(i.id, i.server_name) for i in available_servers]
    if form.validate_on_submit() and form.server:
        server_id = form.server.data
        server = Server.query.filter_by(id=server_id).one()
        username = form.wings_username.data
        password = form.wings_password.data
        domain = form.wings_domain.data

        result = import_component(form.component.data, server, username, password, domain)
        if server and result['result']:
            flash('Component was imported.', 'success')
        return redirect(url_for('server.index'))
    return render_template('components/add.html', form=form)


def import_component(instance, server, wings_username, wings_password, wings_domain):
    mint_server = server.server_mint
    mint_endpoint = server.endpoint_mint

    wings_server = server.server_wings
    wings_user = wings_username
    wings_export_url = server.wings_exporturl

    mint_gather = mintAPI.Gather(mint_server, mint_endpoint)
    wings_data = wingsAPI.ManageData(wings_server, wings_export_url, wings_user, wings_domain)
    wings_component = wingsAPI.ManageComponent(wings_server, wings_export_url, wings_user, wings_domain)

    if not wings_data.login(wings_password):
        return {'result': False, 'json': None}

    wings_component.session = wings_data.session
    resource = instance
    resource_name = resource.split('/')[-1]
    component_id = resource_name
    component_type = component_id.capitalize()
    component_json = create_component(
        resource,
        wings_data,
        wings_component,
        component_type,
        component_id,
        mint_gather)
    return {'result': True, 'json': component_json}


def check_request(self, resp):
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    except requests.exceptions.RequestException as err:
        print(err)
    return resp


def exists(json, key):
    if key in json:
        return json[key]
    else:
        return None


def create_data(datatypes, wings):
    '''
    Create all data objects of a component.
    dataypes: all the datatypes
    wings: object that allow the operations
    '''
    # todo: fix hardcoding
    parent_type_id = 'http://www.wings-workflows.org/ontology/data.owl#DataObject'
    for data_type, value in datatypes.items():
        wings.new_data_type(data_type, parent_type_id)


def generate_data(resource, wingsData, mint):
    jsonRequest = {}
    jsonRequest['inputs'] = []
    jsonRequest['outputs'] = []

    description = mint.describeURI(resource)
    jsonRequest['rulesText'] = exists(description, 'hasRule')
    jsonRequest['documentation'] = exists(description, 'description')
    jsonRequest = mint.prepareParameters(resource, jsonRequest)

    jsonRequest, datatypes = mint.prepareInputOutput(
        resource, jsonRequest, wingsData.dcdom)
    create_data(datatypes, wingsData)
    return jsonRequest


def download_file(url):
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)
    return local_filename


def upload_component(resource, mint):
    description = mint.describeURI(resource)
    url = exists(description, 'hasComponentLocation')
    if url:
        return download_file(url)
    return None


def create_component(resource, wingsData, wingsComponent,
                     component_type, component_id, mint):
    parent_type = None
    component_json = generate_data(resource, wingsData, mint)
    upload_data_path = upload_component(resource, mint)
    wingsComponent.new_component_type(component_type, parent_type)
    wingsComponent.new_component(component_id, component_type)
    wingsComponent.save_component(component_id, component_json)
    if upload_data_path:
        wingsComponent.upload(upload_data_path, component_id)
    return component_json
