class SystemUser:
    def __init__(self, user_id, username, password, role, campus_id=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        self.campus_id = campus_id

    def get_role(self):
        return self.role

    def __str__(self):
        return f"{self.username} ({self.role})"


class AcademicStaff(SystemUser):
    def __init__(self, user_id, username, password, campus_id):
        super().__init__(user_id, username, password, "Lecturer", campus_id)

    def request_booking(self, resource_id, date, start_time, duration):
        pass


class CampusManager(SystemUser):
    def __init__(self, user_id, username, password, campus_id):
        super().__init__(user_id, username, password, "CampusAdmin", campus_id)

    def create_resource(self, name, resource_type):
        pass

    def delete_resource(self, resource_id):
        pass


class GlobalOperator(SystemUser):
    def __init__(self, user_id, username, password):
        super().__init__(user_id, username, password, "SystemOperator", campus_id=None)

    def audit_all_campuses(self):
        pass