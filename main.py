from manage import create, drop, import_customers, import_products, randomOrder
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [create|drop|import_products|import_customers]")
        return

    command = sys.argv[1]

    if command == "create":
        create()
    elif command == "drop":
        drop()
    elif command == "import_products":
        import_products()
    elif command == "import_customers":
        import_customers()
    elif command == "randomOrder":
        randomOrder()
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
