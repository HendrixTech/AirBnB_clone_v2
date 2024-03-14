#!/usr/bin/python3
"""A Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers, using the function do_deploy
"""

from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['34.224.16.103', '34.239.250.26']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        if not (path.exists(archive_path)):
            return False

        # upload archive to the /tmp/dir of web_server
        put(archive_path, '/tmp/')

        # create target dir
        file_datetime = archive_path[-18:-4]
        run('sudo mkdir -p /data/web_static/releases/web_static_{}/'.format(file_datetime))

        # uncompress archive and delete .tgz
        run('sudo tar -xzf /tmp/web_static_{}.tgz -C /data/web_static/releases/web_static_{}/'.format(file_datetime, file_datetime))

        # remove archive
        run('sudo rm /tmp/web_static_{}.tgz'.format(file_datetime))

        # move contents into host web_static
        run('sudo mv /data/web_static/releases/web_static_{}/web_static/* /data/web_static/releases/web_static_{}/'.format(file_datetime, file_datetime))

        # remove extraneous web_static dir
        run('sudo rm -rf /data/web_static/releases/web_static_{}/web_static'.format(file_datetime))

        # delete pre-existing sym link
        run('sudo rm -rf /data/web_static/current')

        # re-establish symbolic link
        run('sudo ln -s /data/web_static/releases/web_static_{}/ /data/web_static/current'.format(file_datetime))

        print('New version deployed!')
    except:
        return False

    # return True on success
    return True
