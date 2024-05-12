# 📚 Literature on the Solana Blockchain

<br>

## 📙 General Knowledge

<br>

* [The Solana Bet, by Toly](https://www.youtube.com/watch?v=dnKc5IvD88Q)
* [Solana's Ultimate Vision, by Toly](https://www.youtube.com/watch?v=cDXG2RFDIjM&t=2s)
* [Solana Whitepaper, by Solana Foundation](https://github.com/solana-labs/whitepaper)
* [Solana Documentation, by Solana Foundation](https://solana.com/docs)
* [Solana Developer Resources, by Solana Foundation](https://solana.com/developers)
* [A Deep Dive into Solana 2.0, by Toly](https://www.youtube.com/watch?v=4MufOKIeuFY)
* [Solana End Game, by Toly and Buffalu](https://www.youtube.com/watch?v=ayC1bgELR8E)
* [Moving from EVM to SVM, by Solana Foundation](https://solana.com/news/evm-to-svm)

<br>

---

## 📘 Solana Architecture

<br>

### 1️⃣ Consensus and Proof of Stake

* [Consensus on Solana, by Helius](https://www.helius.dev/blog/consensus-on-solana)

<br>

### 2️⃣ Proof of History

* [Proof of History, by Toly](https://medium.com/solana-labs/proof-of-history-a-clock-for-blockchain-cf47a61a9274)

<br>

### 3️⃣ Turbine and Data Availability

* [Turbine Block Propagation, by Solana Foundation](https://docs.solanalabs.com/consensus/turbine-block-propagation)
* [Turbine: Block Propagation on Solana, by Helius](https://www.helius.dev/blog/turbine-block-propagation-on-solana)

<br>

### 4️⃣ Sealevel and Parallelism

* [Sealevel, Parallel Processing Thousands of Smart Contracts, by Toly](https://medium.com/solana-labs/sealevel-parallel-processing-thousands-of-smart-contracts-d814b378192)

<br>

### 5️⃣ QUIC (Network Layer)

* [Quinn (rust implementation of QUIC)](https://quinn-rs.github.io/quinn/networking-introduction.html)
* [How to Mitigate Spam QUICkly, by Helius](https://www.helius.dev/blog/all-you-need-to-know-about-solana-and-quic)

<br>

### 6️⃣ Solana Transactions

* [Lifecycle of a Solana Transaction, by ShitTrader and Buffalu](https://www.umbraresearch.xyz/writings/lifecycle-of-a-solana-transaction)
* [Why Are Transactions Dropping?, by Mert Mumtaz, Dan Smith](https://www.youtube.com/watch?v=FwuQupayblk)
* [How to Land Transactions on Solana, by Anam Ansari](https://www.helius.dev/blog/how-to-land-transactions-on-solana)

<br>

##### Compute Usage

* [How to Optimize Compute Usage on Solana, by Solana Foundation](https://solana.com/developers/guides/advanced/how-to-optimize-compute)

<br>

### 7️⃣ Solana Fees

<br>

<p align="center">
<img src="https://github.com/urani-labs/solana-mev-fee-markets-literature/assets/1130416/a84bbe69-a9a9-4d2a-8cab-c038a3d32963" width="80%" align="center" style="padding:1px;border:1px solid black;"/>
</p>

<br>

* [Transaction Fees, by Solana Foundation](https://solana.com/docs/core/transactions/fees)
* [How to use Priority Fees on Solana, by Solana Foundation](https://solana.com/developers/guides/advanced/how-to-use-priority-fees)
* [Solana Fees I, by ShitTrader](https://www.umbraresearch.xyz/writings/solana-fees-part-1)
* [Solana Fees in Theory and Practice, by Helius](https://www.helius.dev/blog/solana-fees-in-theory-and-practice)
* [Solana's Fee Markets Aren't Real, by ShitTrader](https://www.youtube.com/watch?v=Bhh4chj-J0I)
* [Priority Fees: Understanding Solana's Transaction Fee Mechanics, by Helius](https://www.helius.dev/blog/priority-fees-understanding-solanas-transaction-fee-mechanics)
* [Toward Multidimensional Solana Fees, by Theo Diamandis et al](https://www.umbraresearch.xyz/writings/toward-multidimensional-solana-fees)
* [Solana vs Ethereum Fee Markets, with Mert Mumtaz and Dan Smith](https://www.youtube.com/watch?v=tqMX3_CxaYQ)
* [Helius Priority Fee API](https://docs.helius.dev/solana-rpc-nodes/alpha-priority-fee-api)


<br>

----

## 📗 Solana Validators

<br>

### 1️⃣ Running a Solana Validator

<br>

<p align="center">
<img src="https://github.com/urani-labs/solana-mev-literature/assets/1130416/f149e8fe-bba3-4a9e-be39-b5bde7fbde81" width="70%" align="center" style="padding:1px;border:1px solid black;"/>
</p>

<br>

* [Setup a Solana Validator, by Solana Labs](https://docs.solanalabs.com/operations/setup-a-validator)
* [How to Set Up a Solana Validator, by Helius](https://www.helius.dev/blog/how-to-set-up-a-solana-validator)
* [Solana Validator Documentation, by Solana Labs](https://docs.solanalabs.com/)
* [Understanding Slots, Blocks, and Epochs on Solana, by Helius](https://www.helius.dev/blog/solana-slots-blocks-and-epochs)
* [Solana Validator Education, Jito-Solana Concepts + Setup](https://www.youtube.com/watch?v=owLlIRXQvo8)

<br>

### 2️⃣ Clients


##### Jito
* [Jito-Solana, Jito's client in Rust](https://github.com/jito-foundation/jito-solana)

##### Firedancer

* [Firedancer, Jump's high-performance client in C++](https://jumpcrypto.com/firedancer/)
* [What's Firedancer, by Helius](https://www.helius.dev/blog/what-is-firedancer)

<p align="center">
<img src="https://github.com/urani-labs/solana-mev-literature/assets/1130416/b3cc893e-d260-4329-b6d1-0dd6e28d0563" width="60%" align="center" style="padding:1px;border:1px solid black;"/>
</p>

<br>

##### Others
* [Solana-MEV, ChorusOne's modification of Solana's validator](https://github.com/ChorusOne/solana-mev?tab=readme-ov-file)


<br>

### 3️⃣ Stake Weighted QoS

* [Stake Weighted QoS, by Solana Foundation](https://solana.com/developers/guides/advanced/stake-weighted-qos)

<br>

### 4️⃣ Stats and Dashboards

* [Dune's Solana Staking, Validators, and LSTs](https://dune.com/ilemi/solana-staking)
* [Solana.compass Validator Metrics](https://solanacompass.com/)
* [Solana Validator.app Metrics](https://www.validators.app/)

<br>

---

## 📒 Solana Ecosystem

<br>

##### Wormhole

* [List of Wormhole Case Studies](https://wormhole.com/case-studies)


<br>

---

## 📕 Join the Decentralized Finance Revolution

<br>

* [Jupiter's Solana Welcome Guide](https://welcome.jup.ag/)
* [Superteam Communities](https://superteam.fun/)
* [Solana Jobs](https://jobs.solana.com/jobs)
