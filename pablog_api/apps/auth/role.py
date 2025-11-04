from enum import IntEnum


class Role(IntEnum):
    ADMIN = 0
    EDITOR = 1
    READER = 2


class Permission(IntEnum):
    CREATE_POST = 1 << 0
    EDIT_POST = 1 << 1
    DELETE_POST = 1 << 2


class RolePermissions:

    __ROLE_PERMISSIONS_MAP: dict[Role, int] = {
        Role.ADMIN: Permission.CREATE_POST | Permission.EDIT_POST | Permission.DELETE_POST,
        Role.EDITOR: Permission.CREATE_POST | Permission.EDIT_POST | Permission.DELETE_POST,
        Role.READER: 0
    }

    @classmethod
    def is_allowed(cls, role: Role, permission: Permission) -> bool:
        granted_permissions = cls.__ROLE_PERMISSIONS_MAP[role]
        return (granted_permissions & permission) != 0
