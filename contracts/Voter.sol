pragma solidity ^0.8.0;

import { ERC20 } from "openzeppelin/contracts/token/ERC20/ERC20.sol";

contract Voter {

    uint64 constant delay = 3 * 86400;

    event Receive(uint256 data);

    event Gained(uint256 data);

    event Discard(uint256 data);

    struct Proposal {
        uint256 data;
        uint256 ttl;
        bool discarded;
        Voice[] voices;
    }

    struct Voice {
        address user;
        uint256 amount;
        bool isFor;
    }

    ERC20 public immutable token;

    Proposal[3] proposals;

    constructor(ERC20 _token) 
        public
    {
        token = _token;

        for (uint i = 0; i < 3; i++) {
            proposals[i].discarded = true;
        }
    }

    /// Propose some proposal
    /// @param _data information of proposal
    /// 
    function propose(uint256 _data) 
        public 
    {
        bool add = false;
        for (uint i = 0; i < proposals.length; i++) {
            if (checkProposalDiscard(proposals[i])) {
                proposals[i].data = _data;
                proposals[i].ttl = block.timestamp + delay;
                proposals[i].discarded = false;
                delete proposals[i].voices;
                add = true;
                break;
            }
        }

        require(add, "No available position for proposal");
    }

    /// Vote for some proposal from some user
    /// @param _data target proposal
    /// @param _amount amount of voice
    /// @param _isFor option of voice
    /// 
    function vote(uint256 _data, uint256 _amount, bool _isFor) 
        public
    {
        require(token.balanceOf(msg.sender) >= _amount, "Sender's amount more then sender's balance");
        bool add = false;

        for (uint i = 0; i < proposals.length; i++) {
            Proposal storage proposal = proposals[i];
            if (proposal.data == _data) {
                require(!checkProposalDiscard(proposal), "Proposal have been already discarded.");

                for (uint j = 0; j < proposal.voices.length; j++) {
                    require(proposal.voices[j].user != msg.sender, "User have been already voted.");
                }

                proposal.voices.push(Voice(msg.sender, _amount, _isFor));

                uint256 summaryFor = getVotesForAmount(_data);
                uint256 summaryGain = getVotesGainAmount(_data);

                uint256 t = token.totalSupply();
                if (2 * summaryFor > t) {
                    proposal.discarded = true;
                    emit Receive(_data);
                } else if (2 * summaryGain > t) {
                    proposal.discarded = true;
                    emit Gained(_data);
                }

                add = true;
                break;
            }
        }

        require(add, "No such proposal.");
    }

    /// Check if proposal has been already discarded or proposal time is over
    /// @param proposal target proposal for checking
    /// @return true if target proposal has been already discarded, false otherwise
    function checkProposalDiscard(Proposal storage proposal) 
        internal 
        returns (bool) 
    {
        if (proposal.discarded) {
            return true;
        } else if (proposal.ttl <= block.timestamp) {
            emit Discard(proposal.data);
            return true;
        }

        return false;
    }

    /// Check if contract ready for proposation
    /// 
    /// @return true if some proposal has been already discarded, false otherwise
    function readyForPropose() 
        public
        view
        returns (bool) 
    {
        for (uint i = 0; i < proposals.length; i++) {
            if (proposals[i].discarded || proposals[i].ttl > block.timestamp) {
                return true;
            }
        }

        return false;
    }

    /// Get FOR votes for proposal
    /// @param data proposal
    /// @return total amount of FOR voices
    function getVotesForAmount(uint256 data) 
        public
        view
        returns (uint256)
    {
        return getVotesAmount(data, true);
    }

    /// Get GAIN votes for proposal
    /// @param data proposal
    /// @return total amount of GAIN voices
    function getVotesGainAmount(uint256 data) 
        public
        view
        returns (uint256)
    {
        return getVotesAmount(data, false);
    }

    /// Get votes for proposal
    /// @param _data proposal
    /// @param _isFor true if need 'FOR' voices, false - 'GAIN'
    /// @return total amount of voices
    function getVotesAmount(uint256 _data, bool _isFor) 
        internal
        view
        returns (uint256)
    {
        uint256 summary = 0;

        for (uint i = 0; i < proposals.length; i++) {
            Proposal memory proposal = proposals[i];
            if (proposal.data == _data && !proposals[i].discarded && proposals[i].ttl > block.timestamp) {
                for (uint j = 0; j < proposal.voices.length; j++) {
                    Voice memory v = proposal.voices[j];

                    uint256 a = v.amount;
                    uint256 b = token.balanceOf(v.user);
                    if (a > b) {
                        a = b;
                    }

                    if (v.isFor == _isFor) {
                        summary += a;
                    }
                }
            }
        }

        return summary;
    }

    /// Get proposals data
    ///
    /// @return array of actual proposals data
    function getProposals() 
        public 
        view 
        returns (uint256[3] memory) 
    {
        uint256[3] memory res;

        for (uint i = 0; i < proposals.length; i++) {
            res[i] = proposals[i].data;
        }

        return res;
    }

}