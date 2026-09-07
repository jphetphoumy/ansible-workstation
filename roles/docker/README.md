Docker Role
===========

Install Docker Engine on Ubuntu using Docker's official APT repository.

Requirements
------------

- Ubuntu 22.04 or newer.
- Ansible facts must be gathered.
- The remote user must be allowed to use privilege escalation for package and service management.

Role Variables
--------------

- `docker_packages`: Docker Engine packages to install.
- `docker_conflicting_packages`: packages removed before installation, matching Docker's installation guidance.
- `docker_users`: users to add to the `docker` group. The default is an empty list.
- `docker_apt_keyring_path`: path for Docker's repository signing key.
- `docker_apt_repository`: Docker APT repository definition.
- `docker_service_name`: Docker service name.

Example Playbook
----------------

```yaml
- name: Install Docker
  hosts: workstation
  become: false
  gather_facts: true
  roles:
    - role: docker
      vars:
        docker_users:
          - "{{ ansible_user_id }}"
```

License
-------

Internal Use Only

Author Information
------------------

Jérémy Phetphoumy, Ecritel France
