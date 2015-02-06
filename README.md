ssh_kath
========

This is a work-in-progress Python script for connecting to my VPS, attaching to tmux, and enabling the remote machine to send back alerts in the OS X notification center. It is intended to replace the various ssh scripts in my misc-scripts repository.

This script is designed for use under unreliable network conditions, such as cellular networks. It sets SSH options that detect a connection interruption within five seconds and immediately begins reconnection attempts.

The 'alert' bash script is a very simple work in progress designed to notify me when there is a new IRC private message or highlight. It makes a TCP connection to one of the server threads of `ssh_kath.py` and takes three parameters: the IRC buffer number, the IRC buffer name, and the message that triggered the alert. It separates them with `0xFE` bytes because that is a byte that cannot occur in a UTF-8 encoded byte sequence.
