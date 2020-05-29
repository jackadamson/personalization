# Linux System Personalization

## Setup

1. Install python3-pip and the python requirements with `pip3 install --user -r requirements.txt`
2. Pick one of the playbooks from below
3. Create an inventory called hosts.ini if using on a remote machine, else use local.ini
See: https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html
4. Run the playbook with
Local usage:
```
ansible-playbook --ask-become-pass -i local.ini PLAYBOOK
```
Remote usage:
```
ansible-playbook -i hosts.ini PLAYBOOK
```
Where PLAYBOOK is the yaml file

## Playbooks

### gnome.yaml

The main playbook that configures everything, very opinionated

### i3.yaml

WIP Graphical themeing for i3 tiling window manager + all of remote


### remote.yaml

Only CLI configuration, no gnome themeing

### remotelite.yaml

Only CLI configuration, no gnome themeing and less opinionated customizations


## Usage (CLI System)
```bash
pip install -r requirements.txt
# if debian or ubuntu
sudo apt install python-apt
ansible-playbook remote.yaml
```

## Usage (Gnome System)
```bash
pip install -r requirements.txt
# if debian or ubuntu
sudo apt install python-apt
ansible-playbook gnome.yaml
```

## Current Features

- Setup powerline fonts
- Install oh my zsh
- Setup nano syntax highlighting and tabs to spaces
- Installs gnome themes and icon sets
- Makes several usability tweaks to gnome
- And much much more...
