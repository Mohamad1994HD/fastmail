import click
import email_sender
import pickle
import ast
import template_loader

env_vars = {'host': '_HOST_',
            'port': '_PORT_',
            'username': '_USRMAIL_',
            'password': '_PASS_',
            'tls': '_TLS_'}

_conf_file_ = 'config.p'


@click.group()
def config_group():
    pass


@click.command('info', help='Display configurations')
def info():
    try:
        with open(_conf_file_, 'rb') as f:
            conf = pickle.load(f)

        click.echo(
            {"username": conf[env_vars['username']],
             "port": conf[env_vars['port']],
             "host": conf[env_vars['host']],
             "layer tls": conf[env_vars['tls']]}
        )
    except IOError as e:
        click.echo("Error: " + str(e))


@click.command('config', help='Set configurations')
@click.option('--host',
              help='smtp host service provider (e.g smtp.gmail.com)')
@click.option('--port', type=int,
              help='smtp port (e.g 589)')
@click.option('--email',
              help='User email address (sender)')
@click.option('--password',
              help='User email password')
@click.option('--layer',
              type=click.Choice(['ssl', 'tls']),
              help='Choose transport layer')
def configs(host, port, email, password, layer):
    if not (host or port or email or password or layer):
        click.echo("Enter command [option]")
        return

    try:
        with open(_conf_file_, 'rb') as f:
            conf = pickle.load(f)

            if host:
                conf[env_vars['host']] = host
                click.echo(conf[env_vars['host']])
            if port:
                conf[env_vars['port']] = port
                click.echo(conf[env_vars['port']])
            if email:
                conf[env_vars['username']] = email
                click.echo(conf[env_vars['username']])
            if password:
                conf[env_vars['password']] = password
                click.echo(conf[env_vars['password']])
            if layer:
                conf[env_vars['tls']] = 1 if layer == 'tls' else 0
                click.echo(conf[env_vars['tls']])

        with open(_conf_file_, 'wb') as f:
            pickle.dump(conf, f)
    except IOError as e:
        click.echo(str(e))


@click.group()
def action_group():
    pass


@click.command('send', help='Send email')
@click.option('--t/--n', default=False,
              help="With predefined (t)emplate/ (n)o template")
def send(t):
    to = click.prompt('Receiver email')
    subject = click.prompt('Subject')
    message = click.prompt('body msg:')

    if t:
        # get the path of the template file
        template_path = click.prompt("Please enter the full path of the template(.txt) file")
        import json
        key_pairs = ast.literal_eval(
            json.loads(
                click.prompt("Please enter the keywords & their corresponding values of"
                             " the template as JSON object ")
            )
        )
        key_pairs['message'] = message

        deli = click.prompt("Please enter the delimiter you used in your template (e.g $)")

        #create template object & matcher
        template_obj = template_loader.TemplateLoader(delimiter=deli, filepath=template_path, keys=key_pairs)
        message = template_obj.get_outtext()

    conf = pickle.load(open(_conf_file_, "rb"))
    port = conf[env_vars['port']]
    host = conf[env_vars['host']]
    usermail = conf[env_vars['username']]
    password = conf[env_vars['password']]
    tls = conf[env_vars['tls']]

    try:
        click.echo("Sending...")

        email_sender.Mail(port=port,
                          host=host,
                          usermail=usermail,
                          password=password,
                          tls=tls
                          ).send(subject=subject,
                                 body=message,
                                 to=to)
        click.echo("Success!")
    except email_sender.MailException as e:
        click.echo('Error: ' + str(e))


@click.command('init', help='Initialize fastmail')
def init():
    try:
        with open(_conf_file_, "wb") as f:
            pickle.dump({env_vars['port']: 0,
                         env_vars['host']: '',
                         env_vars['username']: '',
                         env_vars['password']: '',
                         env_vars['tls']: False}, file=f)
        click.echo("Initialized!")
        return
    except IOError as e:
        click.echo(str(e))


action_group.add_command(send)
action_group.add_command(init)
config_group.add_command(configs)
config_group.add_command(info)

cli = click.CommandCollection(sources=[action_group, config_group])

if __name__ == '__main__':
    cli()
