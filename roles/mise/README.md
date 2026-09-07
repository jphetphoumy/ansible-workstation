Role Name
=========

Install and configure [mise](https://mise.jdx.dev/) for the current user, including globally configured mise packages. The role uses a custom `mise_packages` Ansible module for idempotent package management.

Requirements
------------

The role expects a Linux host with a user home directory. It downloads the official mise installer from `https://mise.run`.

Role Variables
--------------

`mise_packages` is a list of packages to install globally. Each item must contain a `name` and a `version`:

```yaml
mise_packages:
  - name: chezmoi
    version: "2.72.1"
```

The role invokes the equivalent of:

```text
mise use --global chezmoi@2.72.1
```

The following variables control the mise installation paths and normally do not need to be changed:

- `mise_installer_path`: defaults to `{{ ansible_user_dir }}/.cache/mise-install.sh`.
- `mise_install_path`: defaults to `{{ ansible_user_dir }}/.local/bin/mise`.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- name: Configure workstation
  hosts: localhost
  connection: local
  roles:
    - role: mise
      vars:
        mise_packages:
          - name: chezmoi
            version: "2.72.1"
```

License
-------

MIT

Author Information
------------------

Jérémy Phetphoumy
