#! /usr/bin/env python3

import paramiko
import json
import functools
import time
import os
# LOUIS's SSH connection accepts wired campus connections.
# You must make a "ssh_passwords.txt" file in the program directory with the text
# {"production": {"user": "correct_user", "password": "correct_pass", "host": "lsu.louislibraries.org"}, "test": {"user": "correct_user", "password": "correct_pass", "host": "lsu.test.louislibraries.org"}}


# An attempt was made to change the ssh commands, so that no file was created on the host machine.. that the output of the first command
# would be saved as a bash variable, then fed to the next command.  However, the bash command failed when given an list of 40000 items
# as an argument.  The previous process is preserved:  1) bash command >> file1, 2) bash command file1 >> file2, 3) sftp file2 to client.

def read_credentials(server='test'):
    with open('passwords.txt', 'r') as f:
        parsed_json = json.load(f)
        credentials = parsed_json['Symphony']
        server = credentials[server]
        return server["user"], server["password"], server["host"]


def send_an_ssh_command(host, user, pw, command):
    nbytes = 4096
    port = 22
    client = paramiko.Transport((host, port))
    client.connect(username=user, password=pw)

    stdout_data = []
    stderr_data = []
    session = client.open_channel(kind='session')
    session.exec_command(command)
    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
            break

    exit_status = session.recv_exit_status()
    session.close()
    client.close()
    stdout_text = ''.join(i.decode() for i in stdout_data)
    stderr_text = ''.join(i.decode() for i in stderr_data)
    return exit_status, stdout_text, stderr_text


def copy_an_ssh_file(host, user, pw, source_filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=pw)
    sftp = client.open_sftp()
    sftp.chdir('Xfer')
    callback_for_filename = functools.partial(my_callback, source_filename)
    target_filepath = os.path.join('CatalogFiles', source_filename)
    os.makedirs('CatalogFiles', exist_ok=True)
    sftp.get(source_filename, target_filepath, callback=callback_for_filename)
    client.close()


def my_callback(filename, bytes_so_far, bytes_total):
    pass
    print('Transfer of {} is at {}/{} bytes ({}%)'.format(
        filename, bytes_so_far, bytes_total, int(100 * bytes_so_far / bytes_total)))


def write_to_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def bash_list(stdout_text):
    cleaned_set = depipe_and_setify(stdout_text)
    return ' '.join(i for i in cleaned_set if i)


def depipe_and_setify(text):
    return {i for i in text.split('|\n')}


def generate_onlineISBN_file():
    if os.path.isfile(os.path.join('CatalogFiles', 'onlineISBN.txt')):
        return

    start = time.time()
    print(start)
    user, password, host = read_credentials(server='production')
    command_one = """cd Xfer ; ./lz0007 'selitem -lONLINE -oC >locationOnline'"""
    ssh_one = send_an_ssh_command(host, user, password, command_one)
    exit_status_one, stdout_one, stderr_one = ssh_one

    command_two_output_filename = 'onlineISBN.txt'
    command_two = """cd Xfer ; cat locationOnline | ./lz0007 'selcatalog -iC -oSe -e020 > {}'""".format(command_two_output_filename)
    ssh_two = send_an_ssh_command(host, user, password, command_two)
    exit_status_two, stdout_two, stderr_two = ssh_two

    copy_an_ssh_file(host, user, password, command_two_output_filename)

    command_three = """cd Xfer ; rm locationOnline ; rm onlineISBN.txt"""
    ssh_three = send_an_ssh_command(host, user, password, command_three)
    exit_status_three, stdout_three, stderr_three = ssh_three

    print(time.time() - start)


if __name__ == '__main__':
    generate_onlineISBN_file()
