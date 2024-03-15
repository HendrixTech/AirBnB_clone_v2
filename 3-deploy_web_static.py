#!/usr/bin/python3
from os.path import exists, isdir, getsize
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['34.224.16.103', '34.239.250.26']
env.key_filename = '~/.ssh/id_rsa'
env.user = 'ubuntu'

def do_pack():
    """Create a tar zipped archive of the dir web_static"""
    dt_now = datetime.utcnow()
    dt = dt_now.strftime('%Y%m%d%H%M%S')
    file = "versions/web_static_{}.tgz".format(dt)

    if isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    f_size = getsize('versions/web_static_{}.tgz'.format(dt))
    print('web_static packed: versions/web_static_{}.tgz -> {}Bytes'.format(dt, f_size))
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """

    if exists(archive_path) is False:
        return False
    try:
        file_path = archive_path.split("/")[-1]
        no_ext = file_path.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_ext))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(file_path, path, no_ext))
        run('sudo rm /tmp/{}'.format(file_path))
        run('sudo mv {0}{1}/web_static/* {0}{1}'.format(path, no_ext))
        run('sudo rm -rf {}{}/web_static'.format(path, no_ext))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    print('New version deployed!')
    return do_deploy(file)
