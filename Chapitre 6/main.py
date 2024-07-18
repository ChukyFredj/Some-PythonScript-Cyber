import argparse

def process_args(args):
    # Ici, vous pouvez traiter les arguments comme vous le souhaitez
    print("arg1: ", args.arg1)
    print("arg2: ", args.arg2)
    print("arg3: ", args.arg3)

def main():
    # Créer le parser
    parser = argparse.ArgumentParser(description="Ceci est une description de ce que fait le script.")

    parser.add_argument("-l", "--long", help="argument long", required=True)
    parser.add_argument("-c", "--court", help="argument court", required=True)

    # Analyser les arguments
    args = parser.parse_args()

    # Transmettre les arguments à une autre fonction pour le traitement
    process_args(args)

if __name__ == "__main__":
    main()