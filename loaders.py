""" 
Loaders for training data.
"""
import csv
from abc import ABC, abstractmethod
from pathlib import Path


class LoaderABC(ABC):
    """ 
    Abstract base class for loaders.
    """

    @abstractmethod
    def load(self, filepath: str | Path) -> list[str]:
        pass


class WorldCitiesLoader(LoaderABC):
    """ 
    Load a list of world city names, optionally limited to a language.
    """

    language_mapping = {
        "english": ["US", "GB", "CA", "AU", "NZ"],
        "german": ["DE", "AT", "CH"],
        "spanish":
            ["AR", "BO", "CL", "CO", "CR", "CU", "DO", "EC", "SV", "GT",
             "HN", "MX", "NI", "PA", "PY", "PE", "ES", "UY", ],
        "portuguese": ["BR", "PT"],
    }

    def __init__(
        self,
        language: str | None = None,
        field: str = "city_ascii",
    ) -> None:
        if language is None:
            self.countries = None
        elif language not in self.language_mapping.keys():
            # attempt to set as explicit country code
            self.countries = language.replace(" ", "").split(",")
        else:
            self.countries = self.language_mapping[language]
        self.field = field

    def load(self, filepath: str | Path) -> list[str]:
        """
        Load a list of world city names, optionally limited to a language.

        :param filepath: Name and path of the file containing the city
            names and country codes.
        """
        with open(filepath, "r", encoding="utf8") as file:
            lines = file.readlines()
        header = lines.pop(0)
        header_list = header.replace('"', "").split(",")
        field_index = header_list.index(self.field)
        country_index = header_list.index("iso2")
        cities = []
        for line in lines:
            city = line.replace('"', "").split(",")[field_index].lower()
            country = line.replace('"', "").split(",")[country_index]
            if self.countries is None or country in self.countries:
                cities.append(city)

        ct = [c for c in cities if "." in c]
        print(ct)
        return cities


class GreekMythologyLoader(LoaderABC):
    """
    Load a list of names from greek mythology.
    """

    def load(self, filepath: str | Path) -> list[str]:
        """
        Load a list of names from greek mythology and return them.

        :param filepath: Path to the CSV file containing the names.
        :return: List of names from Greek mythology.
        """
        names = []
        with open(filepath, newline="", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            field_index = header.index("name-english")
            for row in reader:
                names.append(row[field_index])
        print(names)
        return names
