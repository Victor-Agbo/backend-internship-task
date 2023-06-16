from django.contrib.auth.models import Group, Permission

# Create user groups for each role


def create_groups():
    # Create or get the user groups

    manager_group, _ = Group.objects.get_or_create(name="Manager")

    # Assign permissions to the user groups

    manager_group.permissions.add(
        Permission.objects.get(codename="add_user"),
        Permission.objects.get(codename="change_user"),
        Permission.objects.get(codename="delete_user"),
        Permission.objects.get(codename="view_user"),
    )
