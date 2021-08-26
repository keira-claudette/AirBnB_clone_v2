#!/usr/bin/python3
"""
- Generates a .tgz archive file from the contents of the web_static folder of
   the AirBnB project directory.
- Distributes the arhive to a web server
"""
from fabric.operations import local, run, put
from datetime import datetime
from fabric.api import env
import os
import re


env.hosts = ['35.229.69.71', '34.74.144.76']


def do_pack():
    """ This function compresses files """
    local("mkdir -p versions")
    filename = "versions/web_static_{}.tgz".format(datetime.strftime
                                                   (datetime.now(),
                                                    "%Y%m%d%H%M%S"))
    result = local("tar -cvzf {} web_static".format(filename))

    if result.failed:
        return None
    return filename


def do_deploy(archive_path):
    """Distributes an archive to server(s)"""
    if not os.path.exists(archive_path):
        return False
    path_list = archive_path.split('/')
    tar_filename = path_list[-1]
    prefix = tar_filename.split('.')[0]
    # print(path_list, "Tar_file is", tar_filename, "prefix is", prefix)
    result = put(archive_path, "/tmp/{}.tgz".format(prefix))
    if result.failed:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/".format(prefix))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(prefix, prefix))
    if result.failed:
        return False
    result = run("rm /tmp/{}.tgz".format(prefix))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(prefix, prefix))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(prefix))
    if result.failed:
        return False
    print("New version deployed")
    return True


def deploy():
    """ creates and distributes an archive to your web servers"""

    archive_pth = do_pack()
    if archive_pth is None:
        return False
    output = do_deploy(archive_pth)
    return output
