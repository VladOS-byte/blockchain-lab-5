#!/usr/bin/python3

import pytest
import unittest
from brownie import Voter, Token, accounts

def test_transfer():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    assert 100 == t.balanceOf(accounts[0])
    t.transfer(accounts[1], 25, {'from': accounts[0]})
    assert 75 == t.balanceOf(accounts[0])
    assert 25 == t.balanceOf(accounts[1])
    t.transfer(accounts[2], 35, {'from': accounts[0]})
    assert 40 == t.balanceOf(accounts[0])
    assert 35 == t.balanceOf(accounts[2])

def test_empty_proposal():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    assert (0, 0, 0) == v.getProposals()

def test_vote_for_undefined_proposal():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    with pytest.raises(Exception) as _ :
        v.vote(1, 35, False, {'from': accounts[0]})

def test_vote_for_default_proposal():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    with pytest.raises(Exception) as _ :
        v.vote(0, 35, False, {'from': accounts[0]})

def test_propose():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    assert (1, 0, 0) == v.getProposals()

def test_proposes():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.propose(2, {'from': accounts[0]})
    v.propose(3, {'from': accounts[0]})
    assert (1, 2, 3) == v.getProposals()

def test_much_propose():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.propose(2, {'from': accounts[0]})
    v.propose(3, {'from': accounts[0]})
    
    with pytest.raises(Exception) as _ :
        v.propose(4, {'from': accounts[0]})

    assert (1, 2, 3) == v.getProposals()

def test_propose_after_vote():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.propose(2, {'from': accounts[0]})
    v.propose(3, {'from': accounts[0]})
    
    v.vote(1, 55, True, {'from': accounts[0]})

    v.propose(4, {'from': accounts[0]})

    assert (4, 2, 3) == v.getProposals()

def test_vote_for_amount():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.vote(1, 35, True, {'from': accounts[0]})
    assert v.getVotesForAmount(1) == 35
    t.transfer(accounts[1], 25, {'from': accounts[0]})
    v.vote(1, 25, True, {'from': accounts[1]})
    # proposal received
    assert v.getVotesForAmount(1) == 0

def test_vote_already_gained():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.vote(1, 35, False, {'from': accounts[0]})
    assert v.getVotesGainAmount(1) == 35
    t.transfer(accounts[1], 25, {'from': accounts[0]})
    v.vote(1, 25, False, {'from': accounts[1]})
    # proposal gained
    assert v.getVotesGainAmount(1) == 0
    t.transfer(accounts[2], 35, {'from': accounts[0]})
    with pytest.raises(Exception) as _ :
        v.vote(1, 25, False, {'from': accounts[1]})

def test_vote_too_much_amount():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.vote(1, 35, False, {'from': accounts[0]})
    assert v.getVotesGainAmount(1) == 35
    t.transfer(accounts[1], 25, {'from': accounts[0]})
    with pytest.raises(Exception) as _ :
        v.vote(1, 45, False, {'from': accounts[1]})

def test_vote_and_transfer():
    t = Token.deploy("Vlad Voter Token", "VVT", {'from': accounts[0]})
    v = Voter.deploy(t, {'from': accounts[0]})
    v.propose(1, {'from': accounts[0]})
    v.vote(1, 35, False, {'from': accounts[0]})
    assert v.getVotesGainAmount(1) == 35
    t.transfer(accounts[1], 75, {'from': accounts[0]})
    assert v.getVotesGainAmount(1) == 25
    t.transfer(accounts[2], 15, {'from': accounts[0]})
    assert v.getVotesGainAmount(1) == 10
    v.vote(1, 45, True, {'from': accounts[1]})
    assert v.getVotesForAmount(1) == 45



