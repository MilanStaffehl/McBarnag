"""
Generator for random names, employing Markov chains.
"""

import random
import copy


type MarkovChainType = dict[str, dict[str, float]]


class MarkovChain:
    """
    Markov chain for a set of given words.
    """

    def __init__(self, data: list[str], order: int, prior: float) -> None:
        self.order = order
        self.support = list(set("".join(data)))
        self.support.sort()
        self.prior = {x: prior for x in self.support}
        self.prior.update({"\n": 0})
        self.chain: MarkovChainType = dict()
        for word in data:
            self.learn(word)

    def __str__(self) -> str:
        s = ""
        for context, pb in self.chain.items():
            s += f"{context}:\n"
            for next_char, count in pb.items():
                if next_char == "\n":
                    s += f"    \\n: {count}\n"
                    continue
                s += f"    {next_char}: {count}\n"
        return s

    def learn(self, word: str) -> None:
        """
        Learn the given word by adding it to the chain.

        :param word: Any word that shall be learned.
        :return: None.
        """
        length = len(word)
        if length == self.order:
            self.update(word, "\n")
        elif length < self.order:
            return  # cannot learn words that are too short
        pos = 0
        while (pos + self.order) < length:
            context = word[pos:pos + self.order]
            next_char = word[pos + self.order]
            self.update(context, next_char)
            pos += 1
        # update with end-of-word character
        self.update(word[-self.order:], "\n")

    def update(self, context: str, next_char: str) -> None:
        """
        Update the Markov Chain context with the given follow-up char.

        :param context: The context currently being observed.
        :param next_char: The char immediately following the context, 
            that is to be learned.
        :return: None.
        """
        if context not in self.chain.keys():
            self.chain.update({context: copy.copy(self.prior)})
        self.chain[context][next_char] += 1

    def sample(self, context: str) -> str | None:
        """
        Sample the Markov chain for a follow-up char probabilistically.

        :param context: The context for which to find the follow-up char.
        :return: The next char if one is found, otherwise None.
        """
        if context not in self.chain.keys():
            return None
        counts = self.chain[context]
        total = sum(list(counts.values()))
        roll = random.uniform(0, total)
        for char, occurrences in counts.items():
            if roll <= occurrences:
                return char
            roll -= occurrences

    
class MarkovModel:
    """
    A model, trained to create random names from a set of training data.
    """

    def __init__(self, data: list[str], order: int, prior: float) -> None:
        self.order = order
        self.valid_startpoints = self._valid_startpoints(data)
        self.model = {i: MarkovChain(data, i, prior) for i in range(1, self.order + 1)}

    def generate(self, max_length: int) -> str:
        """
        Generate a random word from the learned data.

        :param max_length: The maximum number of characters in the word.
        :return: A random word, inspired by the learned data.
        """
        word = random.choice(self.valid_startpoints)
        while len(word) < max_length:
            context = word[-self.order:]
            next_char = self.sample(context, self.order)
            if next_char == "\n":
                break
            word += next_char
        return word.title()
    
    def sample(self, context: str, order: int) -> str:
        """
        Sample the MC of the given order for the next char for the context.

        If the context does not exist in the given MC, a Katz-Back-Off
        is automatically performed, sampling the next lower order MC
        until a next char can be determined, or the end-of-word char
        is returned.

        :param context: The context for which to find the next char.
        :param order: The order of the Markov Chain to sample from.
        :return: The next char, determined probabilistically, using a
            back-off scheme if the current order yields no result.
        """
        if order == 0:
            return "\n"
        next_char = self.model[order].sample(context)
        if next_char is None:
            next_context = "" if order == 1 else context[1:]
            return self.sample(next_context, order - 1)
        return next_char

    def _valid_startpoints(self, data: list[str]) -> list[str]:
        """
        Return a list of the starting characters of the given data.

        :param data: List of training data words.
        :return: A list of the first N chars of the training data, 
            where N is the order of the model.
        """
        valid = []
        for word in data:
            if len(word) < self.order:
                continue
            valid.append(word[:self.order])
        return valid
