#!/usr/bin/python
"""Manage globally configured mise packages."""

import json

from ansible.module_utils.basic import AnsibleModule


def configured_package_is_ready(records, version):
    """Return whether the requested version is configured and installed."""
    return any(
        record.get("requested_version") == str(version)
        and record.get("installed", False)
        for record in records
        if isinstance(record, dict)
    )


def main():
    module = AnsibleModule(
        argument_spec={
            "packages": {
                "type": "list",
                "elements": "dict",
                "default": [],
            },
            "mise_path": {
                "type": "path",
                "default": "mise",
            },
        },
        supports_check_mode=True,
    )

    packages = module.params["packages"]
    mise_path = module.params["mise_path"]

    for package in packages:
        if not package.get("name") or package.get("version") is None:
            module.fail_json(
                msg="Each mise package must contain a name and a version",
                package=package,
            )

    if not packages:
        module.exit_json(
            changed=False,
            installed_packages=[],
            skipped_packages=[],
        )

    rc, stdout, stderr = module.run_command(
        [mise_path, "ls", "--global", "--json"],
        check_rc=False,
    )
    if rc != 0:
        module.fail_json(
            msg="Unable to read globally configured mise packages",
            rc=rc,
            stdout=stdout,
            stderr=stderr,
        )

    try:
        configured_packages = json.loads(stdout or "{}")
    except ValueError as exc:
        module.fail_json(
            msg="mise returned invalid JSON while listing global packages",
            error=str(exc),
            stdout=stdout,
        )

    installed_packages = []
    skipped_packages = []

    for package in packages:
        name = package["name"]
        version = str(package["version"])
        records = configured_packages.get(name, [])

        if configured_package_is_ready(records, version):
            skipped_packages.append(f"{name}@{version}")
            continue

        package_ref = f"{name}@{version}"
        if module.check_mode:
            installed_packages.append(package_ref)
            continue

        rc, stdout, stderr = module.run_command(
            [mise_path, "use", "--global", package_ref],
            check_rc=False,
        )
        if rc != 0:
            module.fail_json(
                msg=f"Unable to install mise package {package_ref}",
                package=package_ref,
                rc=rc,
                stdout=stdout,
                stderr=stderr,
                installed_packages=installed_packages,
            )
        installed_packages.append(package_ref)

    module.exit_json(
        changed=bool(installed_packages),
        installed_packages=installed_packages,
        skipped_packages=skipped_packages,
    )


if __name__ == "__main__":
    main()
