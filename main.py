from src import bronze, gold, silver, visualize


def main() -> None:
    print("Running bronze step...")
    bronze.main()

    print("Running silver step...")
    silver.main()

    print("Running gold step...")
    gold.main()

    print("Running visualization step...")
    visualize.main()


if __name__ == "__main__":
    main()
