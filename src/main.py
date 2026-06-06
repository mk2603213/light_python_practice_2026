import sys

def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        print(path)
    else:
        print("Ошибка, аргумент не передан")

if __name__ == "__main__":
    main()