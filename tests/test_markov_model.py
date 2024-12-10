"""
Tests for the Markov model module.
"""
import copy
import sys
from pathlib import Path
from typing import Iterator

import pytest
from pytest_subtests import SubTests

sys.path.append(str(Path(__file__).parent))

import markov_model


# type defs
type TrainingDataType = list[str]
type SupportType = list[str]
type PriorType = dict[str, float]
type BaseDataType = tuple[TrainingDataType, SupportType, PriorType]

type MarkovChainType = dict[str, PriorType]
type TestDataType = tuple[
    TrainingDataType, SupportType, PriorType, MarkovChainType
]


@pytest.fixture
def base_data() -> Iterator[BaseDataType]:
    """Provide training data and resulting support & prior.
    Assumes a prior of zero.
    """
    words = ["hamburg", "berlin", "heilbronn", "heidelberg"]
    support = [
        "a", "b", "d", "e", "g", "h", "i", "l", "m", "n", "o", "r", "u"
    ]
    extended_support = copy.copy(support)
    extended_support.append("\n")
    prior = {char: 0 for char in extended_support}
    yield words, support, prior


@pytest.fixture
def markov_chain_1st_order(base_data: BaseDataType) -> Iterator[TestDataType]:
    """Provide the expected result of a 2nd order MC.
        Based on the base data fixture, expecting a prior of zero.
        """
    training_data, support, prior = base_data
    updates = {
        "h": {"a": 1, "e": 2},
        "a": {"m": 1},
        "m": {"b": 1},
        "b": {"u": 1, "e": 2, "r": 1},
        "u": {"r": 1},
        "r": {"g": 2, "l": 1, "o": 1},
        "g": {"\n": 2},
        "e": {"r": 2, "i": 2, "l": 1},
        "l": {"i": 1, "b": 2},
        "i": {"n": 1, "l": 1, "d": 1},
        "n": {"\n": 2, "n": 1},
        "o": {"n": 1},
        "d": {"e": 1}
    }
    mc = {context: copy.copy(prior) for context in updates.keys()}
    for context, update_dict in updates.items():
        mc[context].update(update_dict)
    yield training_data, support, prior, mc


@pytest.fixture
def markov_chain_2nd_order(base_data: BaseDataType) -> Iterator[TestDataType]:
    """Provide the expected result of a 2nd order MC.
    Based on the base data fixture, expecting a prior of zero.
    """
    training_data, support, prior = base_data
    updates = {
        "ha": {"m": 1},
        "am": {"b": 1},
        "mb": {"u": 1},
        "bu": {"r": 1},
        "ur": {"g": 1},
        "rg": {"\n": 2},
        "be": {"r": 2},
        "er": {"l": 1, "g": 1},
        "rl": {"i": 1},
        "li": {"n": 1},
        "in": {"\n": 1},
        "he": {"i": 2},
        "ei": {"l": 1, "d": 1},
        "il": {"b": 1},
        "lb": {"r": 1, "e": 1},
        "br": {"o": 1},
        "ro": {"n": 1},
        "on": {"n": 1},
        "nn": {"\n": 1},
        "id": {"e": 1},
        "de": {"l": 1},
        "el": {"b": 1},
    }
    mc = {context: copy.copy(prior) for context in updates.keys()}
    for context, update_dict in updates.items():
        mc[context].update(update_dict)
    yield training_data, support, prior, mc


@pytest.fixture
def markov_chain_3rd_order(base_data: BaseDataType) -> Iterator[TestDataType]:
    """Provide the expected result of a 3rd order MC.
    Based on the base data fixture, expecting a prior of zero.
    """
    training_data, support, prior = base_data
    updates = {
        "ham": {"b": 1},
        "amb": {"u": 1},
        "mbu": {"r": 1},
        "bur": {"g": 1},
        "urg": {"\n": 1},
        "ber": {"l": 1, "g": 1},
        "erl": {"i": 1},
        "rli": {"n": 1},
        "lin": {"\n": 1},
        "hei": {"l": 1, "d": 1},
        "eil": {"b": 1},
        "ilb": {"r": 1},
        "lbr": {"o": 1},
        "bro": {"n": 1},
        "ron": {"n": 1},
        "onn": {"\n": 1},
        "eid": {"e": 1},
        "ide": {"l": 1},
        "del": {"b": 1},
        "elb": {"e": 1},
        "lbe": {"r": 1},
        "erg": {"\n": 1},
    }
    mc = {context: copy.copy(prior) for context in updates.keys()}
    for context, update_dict in updates.items():
        mc[context].update(update_dict)
    yield training_data, support, prior, mc


@pytest.fixture
def markov_chain_4th_order(base_data: BaseDataType) -> Iterator[TestDataType]:
    """Provide the expected result of a 4th order MC.
    Based on the base data fixture, expecting a prior of zero.
    """
    training_data, support, prior = base_data
    updates = {
        "hamb": {"u": 1},
        "ambu": {"r": 1},
        "mbur": {"g": 1},
        "burg": {"\n": 1},
        "berl": {"i": 1},
        "erli": {"n": 1},
        "rlin": {"\n": 1},
        "heil": {"b": 1},
        "eilb": {"r": 1},
        "ilbr": {"o": 1},
        "lbro": {"n": 1},
        "bron": {"n": 1},
        "ronn": {"\n": 1},
        "heid": {"e": 1},
        "eide": {"l": 1},
        "idel": {"b": 1},
        "delb": {"e": 1},
        "elbe": {"r": 1},
        "lber": {"g": 1},
        "berg": {"\n": 1},
    }
    mc = {context: copy.copy(prior) for context in updates.keys()}
    for context, update_dict in updates.items():
        mc[context].update(update_dict)
    yield training_data, support, prior, mc


def test_markov_chain_class_init() -> None:
    """Test that init of the MarkovChain class"""
    mc = markov_model.MarkovChain(["hamburg"], order=3, prior=0)
    assert mc.order == 3
    assert mc.support == ["a", "b", "g", "h", "m", "r", "u"]
    expected_prior = {
        "a": 0, "b": 0, "g": 0, "h": 0, "m": 0, "r": 0, "u": 0, "\n": 0
    }
    assert mc.prior == expected_prior
    # test the chain is constructed correctly:
    expected = {
        "ham": {"\n": 0, "a": 0, "b": 1, "g": 0, "h": 0, "m": 0, "r": 0, "u": 0},
        "amb": {"\n": 0, "a": 0, "b": 0, "g": 0, "h": 0, "m": 0, "r": 0, "u": 1},
        "mbu": {"\n": 0, "a": 0, "b": 0, "g": 0, "h": 0, "m": 0, "r": 1, "u": 0},
        "bur": {"\n": 0, "a": 0, "b": 0, "g": 1, "h": 0, "m": 0, "r": 0, "u": 0},
        "urg": {"\n": 1, "a": 0, "b": 0, "g": 0, "h": 0, "m": 0, "r": 0, "u": 0},
    }
    assert mc.chain == expected


def test_markov_chain_class_multiple_words(
    markov_chain_3rd_order: TestDataType
) -> None:
    """Test that multiple words lead to correct chains"""
    data, support, prior, expected_mc = markov_chain_3rd_order
    mc = markov_model.MarkovChain(data, order=3, prior=0)
    assert mc.order == 3
    assert mc.support == support
    assert mc.prior == prior
    assert mc.chain == expected_mc


def test_markov_chain_class_prior(
    markov_chain_3rd_order: TestDataType
) -> None:
    """Test that priors are respected"""
    data, support, prior, raw_mc = markov_chain_3rd_order
    mc = markov_model.MarkovChain(data, order=3, prior=0.5)
    # update expected prior
    expected_prior = {k: v + 0.5 for k, v in prior.items()}
    expected_prior.update({"\n": 0})  # not affected by prior
    # update expected MC
    expected_mc = copy.deepcopy(raw_mc)
    for context in raw_mc.keys():
        for char in raw_mc[context].keys():
            if char == "\n":
                continue  # not affected by prior
            expected_mc[context][char] += 0.5
    # test the created MC against the updated test data
    assert mc.order == 3
    assert mc.support == support
    assert mc.prior == expected_prior
    assert mc.chain == expected_mc


def test_markov_chain_class_order(
    subtests: SubTests,
    markov_chain_1st_order: TestDataType,
    markov_chain_2nd_order: TestDataType,
    markov_chain_3rd_order: TestDataType,
    markov_chain_4th_order: TestDataType,
) -> None:
    """Test that order is respected"""
    chains = {
        1: markov_chain_1st_order,
        2: markov_chain_2nd_order,
        3: markov_chain_3rd_order,
        4: markov_chain_4th_order,
    }
    for order in range(1, 4):
        with subtests.test(msg=f"order {order}"):
            data, support, prior, expected_mc = chains[order]
            mc = markov_model.MarkovChain(data, order=order, prior=0)
            assert mc.order == order
            assert mc.support == support
            assert mc.prior == prior
            assert mc.chain == expected_mc


def test_markov_chain_class_sample_method(
    markov_chain_3rd_order: TestDataType
) -> None:
    """Test that the sample method picks a valid follow-up char"""
    # small sample, deterministic outcome
    mc = markov_model.MarkovChain(["hamburg"], order=3, prior=0)
    assert mc.sample("ham") == "b"
    assert mc.sample("mbu") == "r"
    assert mc.sample("urg") == "\n"

    # larger sample, with options
    data = markov_chain_3rd_order[0]
    mc = markov_model.MarkovChain(data, order=3, prior=0)
    assert mc.sample("ham") == "b"  # still deterministic
    assert mc.sample("hei") in ["d", "l"]  # probabilistic
    assert mc.sample("ber") in ["l", "g"]  # probabilistic


def test_markov_model_class_init() -> None:
    """Test that the model is instantiated correctly from simple data"""
    mm = markov_model.MarkovModel(["hamburg"], order=3, prior=0)
    assert mm.order == 3
    assert mm.valid_startpoints == ["ham"]
    # check all chains are present
    assert 1 in mm.model.keys()
    assert 2 in mm.model.keys()
    assert 3 in mm.model.keys()
    # check the chains are built correctly for their order
    for i in range(3):
        assert mm.model[i + 1].order == i + 1


def test_markov_model_class_order() -> None:
    """Test that the order is correctly applied to the model"""
    mm = markov_model.MarkovModel(["hamburg"], order=5, prior=0)
    assert mm.order == 5
    for i in range(5):
        order = i + 1
        assert order in mm.model.keys()
        assert mm.model[order].order == order


def test_markov_model_class_prior() -> None:
    """Test that the prior is correctly applied to the model"""
    mm = markov_model.MarkovModel(["hamburg"], order=3, prior=0.2)
    expected_prior = {
        "a": 0.2,
        "b": 0.2,
        "g": 0.2,
        "h": 0.2,
        "m": 0.2,
        "r": 0.2,
        "u": 0.2,
        "\n": 0,
    }
    for i in range(3):
        assert mm.model[i + 1].prior == expected_prior


def test_markov_model_class_multiple_words(
    markov_chain_1st_order: TestDataType,
    markov_chain_2nd_order: TestDataType,
    markov_chain_3rd_order: TestDataType,
    markov_chain_4th_order: TestDataType,
) -> None:
    """Test model instantiation with multiple words"""
    mcs = {
        1: markov_chain_1st_order[-1],
        2: markov_chain_2nd_order[-1],
        3: markov_chain_3rd_order[-1],
        4: markov_chain_4th_order[-1],
    }
    words = ["hamburg", "berlin", "heilbronn", "heidelberg"]
    mm = markov_model.MarkovModel(words, order=4, prior=0)
    # test model MCs
    assert mm.order == 4
    assert mm.valid_startpoints == ["hamb", "berl", "heil", "heid"]
    # check the chains are built correctly for their order
    for i in range(3):
        order = i + 1
        assert mm.model[order].order == order
        assert mm.model[order].chain == mcs[order]


def test_markov_model_class_generate_method() -> None:
    """Test the generate method of the model class"""
    words = ["hamburg", "berlin", "heilbronn", "heidelberg"]
    mm = markov_model.MarkovModel(words, order=4, prior=0)
    # model is such that only original names can be recreated
    possible_outcomes = [w.title() for w in words]
    output = mm.generate(max_length=20)
    assert output in possible_outcomes
    # check that the max length is respected
    output = mm.generate(max_length=4)
    assert len(output) == 4


def test_markov_model_class_generate_method_more_options() -> None:
    """Show that the method can generate words not the training data"""
    words = ["hamburg", "berlin", "heilbronn", "heidelberg"]
    mm = markov_model.MarkovModel(words, order=3, prior=0)
    output = mm.generate(max_length=20)
    possible_outcomes = [
        "Hamburg", "Berlin", "Heilbronn", "Heidelberg", "Berg"
    ]
    assert output in possible_outcomes


def test_markov_model_class_sample_method() -> None:
    """Test the sample method of the model class"""
    words = ["hamburg", "berlin", "heilbronn", "heidelberg"]
    mm = markov_model.MarkovModel(words, order=4, prior=0)
    # Test that available terms give correct result
    assert mm.sample("ambu", 4) == "r"
    assert mm.sample("erli", 4) == "n"
    assert mm.sample("burg", 4) == "\n"
    assert mm.sample("ham", 3) == "b"
    assert mm.sample("il", 2) == "b"
    # Test back-off with available low-order fallback
    assert mm.sample("xmbu", 4) == "r"
    assert mm.sample("yrg", 3) == "\n"
    # Test with multiple back-offs
    assert mm.sample("xyzg", 4) == "\n"
    # Test back-off fall-through with unsupported combination
    assert mm.sample("xyzq", 4) == "\n"
