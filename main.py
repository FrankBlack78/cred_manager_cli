#!/usr/bin/env/ python3

import click
import configparser
import keyring

# Global variables
VALID_SVC = list()


@click.group()
@click.version_option(package_name='cm')
def cli():
    """
    (C)ommand (L)ine (I)nterface

    Manage keyring credentials.
    """
    # DEFAULT config.ini
    config = configparser.ConfigParser()
    config['DEFAULT'] = {}
    config['VALID SERVICES'] = {'test': 'false',
                                'test1': 'true'}
    # Check if config.ini is available and if it isn't create it with default values
    try:
        with open('config.ini', 'x') as configfile:
            config.write(configfile)
    except FileExistsError:
        pass


@cli.group()
def kr():
    """
    Manage keyring credentials.
    """


@kr.command()
@click.argument('service', type=str, nargs=1)
def init(service):
    """
    Initialize a new keyring entry for a specified service.
    """
    # Create list of valid services from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'VALID SERVICES' not in config:
        click.echo('File config.ini is corrupted. No section [VALID SERVICES]')
        return 1
    for key in config['VALID SERVICES']:
        if config['VALID SERVICES'].getboolean(key):
            VALID_SVC.append(key)
    # Check if argument 'service' is in the list of valid services
    if service not in VALID_SVC:
        click.echo('No valid service.')
        return 1
    # Check if service is already registered
    if service in config:
        click.echo('Service is already registered.')
        return 1
    # User confirmation to add credentials to os keyring
    click.echo('You are about to add credentials to your os keyring.')
    confirmation = click.confirm('Proceed?')
    if confirmation is False:
        click.echo('Process terminated.')
        return 1
    # Collect credentials for the service
    svc = service
    usr = click.prompt('Enter a valid username', type=str)
    pwd = click.prompt('Enter a valid password', type=str, hide_input=True)
    # Create new section in config.ini and add user
    config[svc] = {'Username': usr}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    # Write credentials to os keyring
    keyring.set_password(service_name=svc, username=usr, password=pwd)
    click.echo('Saved credentials in os keyring.')
    return 0


@kr.command()
@click.argument('service', type=str, nargs=1)
def show(service):
    """
    Show a keyring entry for a specified service.
    """
    svc = service
    # Read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Check if service is registered
    if svc not in config:
        click.echo('Service is not registered.')
        return 1
    # User confirmation to add credentials to os keyring
    click.echo('You are about to show your credentials on screen (including password).')
    confirmation = click.confirm('Proceed?')
    if confirmation is False:
        click.echo('Process terminated.')
        return 1
    # Retrieve credentials from keyring
    cred = keyring.get_credential(service_name=svc, username=None)
    # Print out retrieved credentials
    click.echo('User name is {}'.format(cred.username))
    click.echo('Password is {}'.format(cred.password))
    return 0


@kr.command()
def alter():
    click.echo('Hello World!')


@kr.command()
@click.argument('service', type=str, nargs=1)
def delete(service):
    """
    Delete a keyring entry for a specified service.
    """
    # Read config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    # Check if service is registered
    if service not in config:
        click.echo('Service is not registered.')
        return 1
    # User confirmation to delete credentials from os keyring
    click.echo('You are about to delete credentials from your os keyring.')
    confirmation = click.confirm('Proceed?')
    if confirmation is False:
        click.echo('Process terminated.')
        return 1
    # Gather information from config.ini
    svc = service
    usr = config[service].get('username')
    # Delete section from config.ini
    config.remove_section(svc)
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    # Delete credentials from os keyring (Deactivated temporary)
    keyring.delete_password(service_name=svc, username=usr)
    click.echo('Deleted credentials from os keyring.')
    return 0
