<h1 align="center">
  McBarnag
</h1>
<p align="center">
    <b>M</b>arkov-<b>c</b>hain-<b>Ba</b>sed <b>r</b>andom <b>na</b>me <b>g</b>enerator
</p>
<hr />

Another one of these random name generators that employs Markov-chains to create random names and curious accidents from training data. This one has nothing extraordinary going on, and you can probably find better and more versatile implementations out there. But this one is mine.

## Usage

### Installation

The code runs directly, no fancy installation required. Clone the repository anywhere onto your machine using 

```shell
git clone https://github.com/MilanStaffehl/McBarnag.git
```

or 

```shell
git clone git@github.com:MilanStaffehl/McBarnag.git
```

or download it directly as a .zip file from the [GitHub page](https://github.com/MilanStaffehl/McBarnag). _McBarnag_ has no third-party requirements and runs on all versions of Python 3.12 and higher. 

### Usage

In the cloned repository, you can run the `generate.py` script to get some random names. Type

```shell
python generate.py -h
```

To view the help text for the script. It tells you how to use the current version of the script best.

## Roadmap

This project was more of a proof-of-concept and a fun afternoon project. I don't expect to work much more on it, but the few things that came to mind and that would be nice to test are gathered in the [GitHub issues](https://github.com/MilanStaffehl/McBarnag/issues) of the project.

## License

This project is licensed under the MIT license. 

## Acknowledgements

This project uses training data from publicly available sources:

- The list of city names is from the "[World Cities Database](https://simplemaps.com/data/world-cities)" by [simplemaps.com](https://simplemaps.com/data), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- The list of greek mythological is from "[List of Greek Gods and Goddesses](https://github.com/katkaypettitt/greek-gods)" by [Katrina Pettitt](https://github.com/katkaypettitt), licensed under the [MIT license](https://mit-license.org/).

This project was largely inspired by an [article](https://benhoyt.com/writings/markov-chain/) by Ben Hoyt and shaped by a similar implementation displayed on [RogueBasin](https://www.roguebasin.com/index.php?title=Names_from_a_high_order_Markov_Process_and_a_simplified_Katz_back-off_scheme). 