import click
from fabfile import minify, init_database, local_backup


def bake():
    """
    Initialize the database from the backup and minify JS files to configure ("cook") the app.
    Uses the functions already written in the fabfile.
    """
    init_database('bombolone')
    minify()

def serve():
    """
    Serve the "cooked" app.
    """
    import app
    app.main()

def refrigerate():
    """
    Makes a local backup of the database, using the function already written in the fabfile.
    """
    local_backup()


COMMANDS = {
    'bake': bake,
    'serve': serve,
    'refrigerate': refrigerate
}


@click.command()
@click.argument('command')
def main(command):
    """
    Bake, serve and refrigerate your Bombolone app!

    :param command: [bake|refrigerate|serve]

    `bake`: Initialize your Bombolone app, restoring the database from a backup.

    `refrigerate`: Put your Bombolone app in the fridge, making a local backup of the database.

    `serve`: Serve your Bombolone app!
    """
    if command not in COMMANDS.keys():
        raise click.BadParameter('%s is not something you can do with Bombolone!' % command)
    COMMANDS[command]()

