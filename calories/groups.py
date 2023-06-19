from django.contrib.auth.models import Group, Permission

# Create user groups for each role


def create_groups():
    # Create or get the user groups

    manager_group, _ = Group.objects.get_or_create(name="Manager")
    admin_group, _ = Group.objects.get_or_create(name="Administrator")

    # Assign permissions to the user groups

    manager_group.permissions.add(
        Permission.objects.get(codename="add_user"),
        Permission.objects.get(codename="change_user"),
        Permission.objects.get(codename="delete_user"),
        Permission.objects.get(codename="view_user"),
    )

    for permission in manager_group.permissions.all():
        admin_group.permissions.add(permission)
    admin_group.permissions.add(
        Permission.objects.get(codename="add_entry"),
        Permission.objects.get(codename="change_entry"),
        Permission.objects.get(codename="delete_entry"),
        Permission.objects.get(codename="view_entry"),
    )
