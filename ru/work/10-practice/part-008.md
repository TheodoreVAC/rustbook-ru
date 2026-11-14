## 10.8 Blockchain

Blockchain is a digital technology that has gained significant attention in recent years. This attention has been due, in part, to the rise in the price of Bitcoin, which is closely tied to blockchain technology, as well as other related concepts such as Ethereum, virtual currencies, and the digital economy. The endorsement of virtual currencies by influential figures such as Tesla CEO Elon Musk has further fueled the development of the field. Additionally, governments around the world have been formulating policies related to blockchain technology, adding to the momentum of the industry. Ultimately, blockchain technology is a tool closely tied to economic development and the trade of commodities. Online transactions rely heavily on financial institutions as third-party intermediaries to process payment information. However, this credit-based model has inherent weaknesses that limit the feasibility of small daily payment transactions, increase the cost of transactions, and prevent completely irreversible transactions due to the involvement of financial intermediaries to coordinate disputes. This limits the potential of internet trade as both parties in a transaction must trust each other, and merchants must guard against potential fraud. In contrast, physical cash transactions do not require third-party intermediaries and thus do not face such limitations. To address these issues, we need an electronic payment system based on cryptographic principles that enables two parties to make payments directly without intermediaries. This eliminates the possibility of rolling back payment transactions, protecting sellers from fraud. We propose a method for generating electronic transaction proofs using a peer-to-peer distributed timestamp server that records transactions in chronological order. The system is secure as long as the total computing power controlled by honest nodes exceeds that of cooperating attackers. The passage above is the introduction to the Bitcoin whitepaper(Bitcoin: A Peer-to-Peer Electronic Cash System [19]), written by Satoshi Nakamoto, the inventor of Bitcoin. It outlines the reason for the invention of Bitcoin, which was to address the practical problem of the global financial crisis of 2008, inflation, and its impact on various countries. Nakamoto was dissatisfied with the existing financial environment and used their professional knowledge to invent the blockchain technology to address this problem.

### 10.8.1 The Principles of Blockchain and Bitcoin

Blockchain and Bitcoin are often mentioned together in media reports, but their relationship is not always clear. Blockchain technology is a new decentralized infrastructure and computing paradigm that

uses a chain data structure to store and verify data, distributed node consensus algorithms to generate and update data, cryptography to ensure data security, and smart contracts to program and operate data. In contrast, Bitcoin is a type of digital currency that was invented using blockchain technology. To put it simply, blockchain is a decentralized distributed ledger, where data is not only stored on each node but replicated and shared across the entire network. Blockchain is a ledger that records transactions and consumes a lot of resources to do so. As transactions are recorded, rewards and transaction fees are generated in the form of digital currency, which is used to maintain the system’s operation. Bitcoin is the first digital currency created using blockchain technology and serves as a guarantee of transactions and a type of incentive. In summary, blockchain is a distributed transaction medium, and Bitcoin is a type of digital currency that serves as a guarantee of transactions and an incentive. Blockchain itself consists of components such as blocks, blockchains, transactions, accounts, miners, transaction fees, and rewards. To implement a blockchain system, one must start by implementing these basic components.

### 10.8.2 A Primary Blockchain

The blockchain structure consists of a block header, block body, and block hash. The header contains the hash of the previous block (pre_hash), the current block transaction hash value (tx_hash), and the block packaging time (time). The block body includes all transaction data (transactions), and the block hash (hash) is calculated from the block header and block body. The block and blockchain structures are shown in the following figure.

pre hash|tx hash|time pre hash|tx hash|time pre hash|tx hash|time transaction 1 transaction 1 transaction 1 transaction 2 transaction 2 transaction 2 transaction 3 transaction 3 transaction 3 ... ... ... hash hash hash

Hash values play a vital role in the blockchain, as evident from the structure discussed above. Thus, the initial step is to compute the hash value, and serialization of the block structure is a more efficient approach. The basic blockchain’s first function is to perform serialization and hash value computation, demonstrated in the following code. To handle blocks with varying transaction numbers, we employ the ”Sized” trait. The serialization process utilizes the ”bincode” library, while the ”crypto’s Sha3” library computes the hash. For better readability, we convert all hashes to strings. The serialized data is of type ”&[u8]”, and ”hash_str” retrieves the data and returns it as a string.

```rust
// serializer.rs

use bincode;
use serde::Serialize;
use crypto::digest::Digest;
use crypto::sha3::Sha3;

// Data serialization
pub fn serialize<T: ?Sized>(value: &T) -> Vec<u8>
    where T: Serialize
{
    bincode::serialize(value).unwrap()
}

// calculate the hash value and return it as a string
pub fn hash_str(value: &[u8]) -> String {
```

```rust
    let mut hasher = Sha3::sha3_256();
    hasher.input(value);

    hasher.result_str()
}
```

The hash computation function can calculate the hash values for the block’s hash, pre_hash, and tx_hash, while the time can be obtained by capturing the block’s generation time. Initially, we simplify the problem by using strings to represent transactions and place them in a Vec to simulate multiple transactions. In Rust, we can utilize the struct to represent blocks and block headers.

```rust
// block.rs

// Block structure
pub struct Block {
    pub header: BlockHeader,
    pub tranxs: String,
    pub hash: String,
}

// Block header structure
pub struct BlockHeader {
    pub time: i64,
    pub pre_hash: String,
    pub txs_hash: String,
}
```

Since hash values are crucial in the blockchain, the first step is to calculate the hash. To achieve this, we serialize the block structure before computing the hash value for efficiency purposes.

```rust
// block.rs

use std::thread;
use std::time::Duration;
use chrono::prelude::*;
use utils::serializer::{serialize, hash_str};
use serde::Serialize;

// Definition of block header
#[derive(Serialize, Debug, PartialEq, Eq)]
pub struct BlockHeader {
    pub time: i64,
    pub pre_hash: String,
    pub txs_hash: String,
}

// Definition of block
#[derive(Debug)]
pub struct Block {
    pub header: BlockHeader,
    pub tranxs: String,
    pub hash: String,
}
```

```rust
impl Block {
    pub fn new(txs: String, pre_hash: String) -> Self {
        // Introduce a 3-second delay for mining
        println!("Start mining .... ");
        thread::sleep(Duration::from_secs(3));

        // Prepare timestamp and calculate transaction hash
        let time = Utc::now().timestamp();
        let txs_ser = serialize(&txs);
        let txs_hash = hash_str(&txs_ser);

        let mut block = Block {
            header: BlockHeader {
                time: time,
                txs_hash: txs_hash,
                pre_hash: pre_hash,
            },
            tranxs: txs,
            hash: "".to_string(),
        };

        block.set_hash();
        println!("Produce a new block!\n");

        block
    }

    // Calculate and set block hash value
    fn set_hash(&mut self) {
        let header = serialize(&(self.header));
        self.hash = hash_str(&header);
    }
}
```

To form a blockchain, we must link the created blocks together, which can be accomplished using a Vec to store multiple blocks. The system should enable the generation of the first block (genesis block) and adding new blocks to the chain. Since the genesis block does not have a pre_hash, it needs to be set manually. We will utilize the base64 value of ”Bitcoin hit $60000” as the pre_hash for the genesis block. Lastly, we will require a function to create a new block and update its hash value.

```rust
// blockchain.rs
use crate::block::Block;

// Genesis block pre_hash
const PRE_HASH: &str = "22caaf24ef0aea3522c13d133912d2b7
                        22caaf24ef0aea3522c13d133912d2b7";
pub struct BlockChain {
    pub blocks: Vec<Block>,
}

impl BlockChain {
    pub fn new() -> Self {
```

```rust
        BlockChain { blocks: vec![Self::genesis_block()] }
    }

    // Generate the genesis block
    fn genesis_block() -> Block {
        Block::new("genesis block".to_string(),PRE_HASH.
           to_string()) }

    // Add blocks to form a blockchain
    pub fn add_block(&mut self, data: String) {
        // Get the hash value of the previous block
        let pre_block = &self.blocks[self.blocks.len() - 1];
        let pre_hash = pre_block.hash.clone();
        // Build a new block and add it to the chain
        let new_block = Block::new(data, pre_hash);
        self.blocks.push(new_block);
    }

    // Print block information
    pub fn block_info(&self) {
        for b in self.blocks.iter() { println!("{:#?}", b); }
    }
}
```

To execute a blockchain system, we must generate transactions to create blocks. In the code below, the string ”tx” represents a transaction, and information is printed after the transaction has been packed and finalized.

```rust
// main.rs
use core::blockchain::BlockChain as BC;

fn main() {
    println!("----------------Mine Info-------------------");

    let mut bc = BC::new();
    let tx = "0xabcd -> 0xabce: 5 btc".to_string();
    bc.add_block(tx);
    let tx = "0xabcd -> 0xabcf: 2.5 btc".to_string();
    bc.add_block(String::from(tx));

    println!("----------------Block Info------------------");
    bc.block_info();
}
```

To ensure that these codes work coherently, we need to arrange them logically. Since the hash calculation is not directly related to the blockchain, it should be included in the ”utils” directory as a tool. On the other hand, the ”block” and ”blockchain” should be stored in the ”core” directory. The main function should call the ”core” directory to execute the creation and addition of blocks. To generate the blockchain project, we can use Cargo, as demonstrated in the blockchain1 repository on GitHub. The code above has facilitated the implementation of a basic blockchain project that can create and add blocks. The program’s output, including mining information and block information, is depicted on next page.

Our implementation is a simplified version of a blockchain. A comprehensive blockchain involves various components such as proof of work, transactions, accounts, hashing, miners, mining, bitcoin rewards, block storage, and many others. Readers can gradually incorporate these features on top of the fundamental blockchain implementation.
