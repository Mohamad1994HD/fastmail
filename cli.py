import click
import os
import email_sender

env_vars = {'host': '_HOST_NAME_',
           'port': '_PORT_NO_',
           'username': '_USER_EMAIL_',
           'password': '_USER_PASS_',
           'tls': 'USE_TLS'}

@click.group()
def config_group():
    pass


@click.command('config', help='Set configurations')
@click.option('--host',
              help='smtp host service provider (e.g smtp.gmail.com)')
@click.option('--port',
              help='smtp port (e.g 589)')
@click.option('--email',
              help='User email address (sender)')
@click.option('--password',
              help='User email password')
@click.option('--layer',
              type=click.Choice(['ssl', 'tls']),
              help='Choose transport layer')
def configs(host, port, email, password, layer):
    if host:
        os.environ[env_vars['host']] = host
        click.echo(os.environ.get(env_vars['host']))
    if port:
        os.environ[env_vars['port']] = port
        click.echo(os.environ.get(env_vars['port']))

    if email:
        os.environ[env_vars['username']] = email
        click.echo(os.environ.get(env_vars['username']))
    if password:
        os.environ[env_vars['password']] = password
        click.echo(os.environ.get(env_vars['password']))
    if layer:
        os.environ[env_vars['tls']] = '1' if layer == 'tls' else '0'
        click.echo(os.environ.get(env_vars['tls']))


@click.group()
def action_group():
    pass


@click.command('send', help='Send email')
def send():
    to = click.prompt('Reciever email')
    subject = click.prompt('Subject')
    message = click.prompt('message')

    try:
        email_sender.Mail(port=os.environ.get(env_vars['port']),
                          host=os.environ.get(env_vars['host']),
                          usermail=os.environ.get(env_vars['username']),
                          password=os.environ.get(env_vars['password']),
                          tls=bool(int(os.environ.get(env_vars['tls'])))
                          ).send(subject=subject,
                                 body=message,
                                 to=to)
        click.echo("Success!")
    except email_sender.MailException as e:
        click.echo('Error: ' + str(e))


action_group.add_command(send)
config_group.add_command(configs)
cli = click.CommandCollection(sources=[action_group, config_group])

if __name__ == '__main__':
    cli()


