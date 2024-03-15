#!/usr/bin/python3
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ['34.224.16.103', '34.239.250.26']
env.key_filename = '~/.ssh/id_rsa'
env.user = 'ubuntu'

def do_pack():
    """Create a tar zipped archive of the dir web_static"""
    dt_now = datetime.utcnow()
    dt = dt_now.strftime('%Y%m%d%H%M%S')
    file = "versions/web_static_{}.tgz".format(dt)

    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    f_size = os.path.getsize('versions/web_static_{}.tgz'.format(dt))
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
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("sudo rm /tmp/{}".format(file)).failed is True:
        return False
    if run("sudo mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/current").failed is True:
        return False
    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    print('New version deployed!')
    return do_deploy(file)
