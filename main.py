from export_data import export_data
from import_data import import_data
from config import data_csv




def main():
    export_data(data_csv)
    print(data_csv)


if __name__ == "__main__":
    main()
