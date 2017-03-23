#! /usr/bin/env python3

import paramiko
import json
import time
import functools
# # LOUIS's SSH connection accepts wired campus connections.


def get_credentials(server='test'):
    with open('ssh_passwords.txt', 'r') as f:
        credentials = json.load(f)
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


def copy_an_ssh_file(host, user, pw, filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=pw)

    def my_callback(filename, bytes_so_far, bytes_total):
        print('Transfer of %r is at %d/%d bytes (%.1f%%)' % (
            filename, bytes_so_far, bytes_total, 100. * bytes_so_far / bytes_total))

    sftp = client.open_sftp()
    sftp.chdir('Xfer')
    callback_for_filename = functools.partial(my_callback, filename)
    sftp.get(filename, filename, callback=callback_for_filename)

    client.close()


def write_to_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def append_to_file(filename, text):
    with open(filename, 'a') as f:
        f.write(text)


def depipe_and_setify(text):
    return {i for i in text.split('|\n')}


if __name__ == '__main__':
    start = time.time()

    user, password, host = get_credentials(server='production')
    # new_command = """cd Xfer ; ./lz0007 'selitem -lONLINE -oC'"""
    new_command = """cd Xfer ; ./lz0007 'selitem -lONLINE -oC >locationOnline'"""
    new_ssh_command = send_an_ssh_command(host, user, password, new_command)
    new_exit_status, new_stdout, new_stderr = new_ssh_command

    print(time.time() - start)
    # print('Exit status: ', new_exit_status)
    # print('Out: ', depipe_and_setify(new_stdout))
    # print('StdError: ', new_stderr)

    # write_to_file('lONLINE.txt', new_stdout)

    # newer_set_stdout = set()
    # count = 0
    # for i in depipe_and_setify(new_stdout):
    #     print(count, '\t', time.time() - start)
    #     newer_command = """cd Xfer ; echo {} | ./lz0007 'selcatalog -iC -oSe -e020'""".format(i)
    #     newer_ssh_command = send_an_ssh_command(host, user, password, newer_command)
    #     newer_exit_status, newer_stdout, newer_stderr = newer_ssh_command

    #     # print('Exit status: ', newer_exit_status)
    #     # print('Out: ', depipe_and_setify(newer_stdout))
    #     # print('StdError: ', newer_stderr)

    #     newer_set_stdout.add(newer_stdout)
    #     # print(newer_set_stdout)
    #     count += 1

    # newer_text = '\n'.join(i for i in newer_set_stdout)
    # write_to_file('newer.txt', newer_text)

    newer_command = """cd Xfer ; cat locationOnline | ./lz0007 'selcatalog -iC -oSe -e020 > onlineISBN.txt'"""
    newer_ssh_command = send_an_ssh_command(host, user, password, newer_command)
    newer_exit_status, newer_stdout, newer_stderr = newer_ssh_command
    print('Exit status: ', newer_exit_status)
    print('Out: ', depipe_and_setify(newer_stdout))
    print('StdError: ', newer_stderr)

    print(time.time() - start)

    copy_an_ssh_file(host, user, password, "onlineISBN.txt")

    print(time.time() - start)
