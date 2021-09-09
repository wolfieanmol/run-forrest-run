import random
from PersistanceLayer.db_handler import DbHandler


def main():
    db = DbHandler()

    with open("names.txt", "r") as f:
        lines = f.readlines()
        names = [name.split(" ")[0] for name in lines]

    for i in range(1000):
        for name in names:
            for j in range(random.randint(5, 20)):
                print(name + "_" + str(i))
                db.insert_user_point(name + "_" + str(i))


if __name__ == '__main__':
    main()
