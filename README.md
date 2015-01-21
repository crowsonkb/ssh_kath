ssh_kath
========

This is a work-in-progress Python script for connecting to my VPS and attaching to tmux. It is intended to replace the various ssh scripts in my misc-scripts repository.

This script is designed for use under unreliable network conditions, such as cellular networks. It sets SSH options that detect a connection interruption within five seconds and immediately begins reconnection attempts.
