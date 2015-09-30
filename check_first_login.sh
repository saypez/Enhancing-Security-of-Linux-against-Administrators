#!/bin/bash
# only do this for interactive shells
if [ "$-" != "${-#*i}" ]; then
    if [ -f "$HOME/.not_logged_in_yet" ]; then
        echo -e "\033[1m \033[91m\n Welcome, this is your first login with this account \033[0m \n"
        rm "$HOME/.not_logged_in_yet"
    fi
fi
