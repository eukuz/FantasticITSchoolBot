import string
import secrets
from db.app_db import *

class KeyGen:
    _db = Database()

    @staticmethod
    def __generateNKeys(n, tableName):
        symbols = string.digits + string.ascii_letters
        keys = set()
        field_name = tableName[:-1] + '_key' if tableName != 'homework' else 'hw_key'
        while len(keys) != n:
            key = "".join(secrets.choice(symbols) for i in range(13))
            print({field_name : key})
            if KeyGen._db.get(tableName, **{field_name : key}) is None:
                keys.add(key)
        return keys

    @staticmethod
    def __writeKeysToDB(keys, tableName):
        field_name = tableName[:-1] + '_key' if tableName != 'homework' else 'hw_key'
        for key in keys:
            KeyGen._db.register(tableName, **{field_name : key})

    @staticmethod
    def __getKeys(n, tableName):
        keys = KeyGen.__generateNKeys(n, tableName)
        KeyGen.__writeKeysToDB(keys, tableName)
        control = tableName[0:3].upper()
        controlsKeys = set()
        for key in keys:
            controlsKeys.add(control + key)
        return controlsKeys

    @staticmethod
    def generateNKeysStudents(n):
        return KeyGen.__getKeys(n, "students")
    @staticmethod
    def generateNKeysTeachers(n):
        return KeyGen.__getKeys(n, "teachers")

    @staticmethod
    def generateNKeysTutors(n):
        return KeyGen.__getKeys(n, "tutors")

    @staticmethod
    def generateNKeysParents(n):
        return KeyGen.__getKeys(n, "parents")

    @staticmethod
    def generateNKeysCourses(n):
        return KeyGen.__getKeys(n, "courses")

    @staticmethod
    def generateNKeysGroups(n):
        return KeyGen.__getKeys(n, "groups")

    @staticmethod
    def generateNKeysHomework(n):
        return KeyGen.__getKeys(n, "homework")

    @staticmethod
    def generateNKeys(n, tableName):
        return KeyGen.__getKeys(n, tableName)

def main():
    app_db = Database()
    app_db.map_student_group('Nk3gD9jziJHjR', 'wBFcxRDmUFol0')
    app_db.map_student_group('rQoITHLQYcLh5', 'wBFcxRDmUFol0')
    app_db.map_student_group('XHXetJGPKSTSQ', 'wBFcxRDmUFol0')
    app_db.map_student_group('fQm1MY1pavKZv', 'wBFcxRDmUFol0')
    print(app_db.get_student(group_key='wBFcxRDmUFol0'))
main()