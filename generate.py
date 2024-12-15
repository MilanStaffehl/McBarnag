"""
Name generator module.
"""

import argparse

import loaders
import markov_model


def main(args: argparse.Namespace) -> None:
    """
    Generate a name or names according to the received args.

    :param args: Namespace from the argument parser.
    :return: None.
    """
    if args.dataset == "cities":
        loader = loaders.WorldCitiesLoader(args.language)
        filepath = "./resources/worldcities.csv"
    elif args.dataset == "greek-mythology":
        loader = loaders.GreekMythologyLoader()
        filepath = "./resources/greek_mythology.csv"
    else:
        raise KeyError(f"Unknown dataset: {args.dataset}")

    training_data = loader.load(filepath)
    model = markov_model.MarkovModel(
        training_data, args.order, args.prior, args.max_backoff
    )

    for i in range(args.number):
        name = model.generate(args.max_length)
        print(f"{i:02d}: {name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a random name from a sample of training data "
            "using Markov chains"
        ),
        prog='python generate.py',
    )
    parser.add_argument(
        "dataset",
        help=(
            "The dataset to choose for the training of the Markov model."
        ),
        choices=["cities", "greek-mythology"],
    )
    parser.add_argument(
        "-o",
        "--order",
        help="Order of the Markov model. Defaults to 3.",
        default=3,
        type=int,
    )
    parser.add_argument(
        "-p",
        "--prior",
        help="Prior value for the probability distribution. Defaults to 0.",
        default=0.0,
        type=float,
    )
    parser.add_argument(
        "-m",
        "--max-length",
        help="Maximum length of the generated word in characters.",
        default=10,
        type=int,
    )
    parser.add_argument(
        "-b",
        "--max-backoff",
        help=(
            "The maximum MC order to fall back to when a higher order does "
            "not contain a set of characters."
        ),
        default=1,
        type=int,
    )
    parser.add_argument(
        "-n",
        "--number",
        help="How many names to generate and display.",
        default=1,
        type=int,
    )
    parser.add_argument(
        "-l",
        "--language",
        help=(
            "Only works for city names: choose the language from which the "
            "training data shall be drawn. Only cities from countries with "
            "that language will be considered for training. Can also be a "
            "comma-separated list of ISO 3166-1 alpha-2 country codes."
        ),
        default=None,
    )
    return parser


if __name__ == '__main__':
    parser_ = build_parser()
    args_ = parser_.parse_args()
    try:
        main(args_)
    except KeyboardInterrupt:
        print("Execution forcefully stopped.")
