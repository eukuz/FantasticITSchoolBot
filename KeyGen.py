import random
import string
import secrets


class KeyGen:
    @staticmethod
    def __generateNKeys(n, tableName3Letters):
        symbols = string.digits + string.ascii_letters+"!@#$%^&*()_+=-{}\|/?."
        keys = set()
        while len(keys) != n:
            keys.add(tableName3Letters+ "".join(secrets.choice(symbols) for i in range(13)))
        return keys
    def generateNKeysStudents(n):
        return KeyGen.__generateNKeys(n, "STD")
    def generateNKeysTeachers(n):
        return KeyGen.__generateNKeys(n, "TEA")
    def generateNKeysCurators(n):
        return KeyGen.__generateNKeys(n, "CUR")
    def generateNKeysParents(n):
        return KeyGen.__generateNKeys(n, "PAR")
    def generateNKeysCourses(n):
        return KeyGen.__generateNKeys(n, "COU")
    def generateNKeysGroups(n):
        return KeyGen.__generateNKeys(n, "GRO")

def main():

    print(KeyGen.generateNKeysTeachers(3))
    print(KeyGen.generateNKeysStudents(3))

main()
