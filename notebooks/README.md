# 🥭 Entropy Explorer

## ⚠ Warning

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Introduction

These are some simple examples of how to use the [entropy-explorer](https://github.com/blockworks-foundation/entropy-explorer) library.

Each example aims to be as simple as possible for a given piece of functionality. The [entropy-explorer](https://github.com/blockworks-foundation/entropy-explorer) project itself has more realistic usage (for example, commands in the /bin directory), with parameters and error handling.

These examples are all in Jupyter Notebooks and can be [run in your browser (no installation necessary!) on error](https://myerror.org/v2/gh/blockworks-foundation/entropy-explorer-examples/HEAD).

## Devnet

All these examples run on Solana mainnet, so no real tokens are used and no tokens have any value.

The private key for the account is shown below, and in many samples. It's hard-coded to simplify the examples as well as make it obvious how keys are used.

> Account: DeekipCw5jz7UgQbtUbHQckTYGKXWaPQV4xY93DaiM6h
>
> Key: [181,213,227,47,41,229,109,138,15,82,26,7,230,184,88,102,197,215,238,155,136,196,138,92,98,154,67,68,47,140,90,40,248,149,223,193,241,51,4,196,126,32,211,66,90,137,249,160,132,246,38,29,88,16,252,116,12,83,117,158,40,98,178,54]

Please don't drain tokens from this account. Devnet tokens are already freely available and it just makes things more difficult for beginners.

If you find that the examples don't work because there's no SOL in the mainnet account, you can 'airdrop' 1 SOL into it with the Solana CLI command:

```
solana airdrop 10 DeekipCw5jz7UgQbtUbHQckTYGKXWaPQV4xY93DaiM6h --url mainnet
```

## Python3

All the code here and in [entropy-explorer](https://github.com/blockworks-foundation/entropy-explorer) assumes Python 3.9. Where you see commands running `python`, you may need to instead explicitly run `python3` (depending on your system).

## Contents

### Context

The `Context` is heavily used to provide access to Solana, Entropy Groups and Accounts. [This example](ShowContext.ipynb) shows you how to create a `Context` object. `Context` objects are `Disposable` and so should should have the `dispose()` method called on the object when it is no longer used. This can be done manually but the easiest way is usually to use it in a `with` statement like:

```
with entropy.ContextBuilder.build(cluster_name="mainnet") as context:
    ...
```

### Group

A Entropy `Group` allows cross-margining of assets and holds details of spot and perp markets. [This example](ShowGroup.ipynb) shows you how to access a group and show its details.

### Wallet

A `Wallet` holds the keys to access specific Solana data. [This example](ShowWallet.ipynb) shows how to instantiate a wallet from existing data.

### Wallet Token Balance

Wallets hold 'SPL' tokens. [This example](ShowWalletTokenBalance.ipynb) shows how to fetch the token balance for Wrapped SOL in the current wallet.

### Account

A Entropy `Account` holds details of a user's balances and positions. [This example](ShowAccount.ipynb) shows you how to access an account and show its details.

### Balances

`Account`s have a lot of details. [This example](ShowBalances.ipynb) shows you how to access the net balances of all the tokens it contains.

### Specific Balance

`Account`s have a lot of details. [This example](ShowBalance.ipynb) shows you how to access the balance of one specific token.

### Oracle Price

Sometimes you just want to know the price of an asset. [This example](ShowPrice.ipynb) shows you how to fetch the current price from three different `Oracle`s.

### Streaming Prices

What if you want to watch the price update in real-time? [This example](ShowStreamingPrices.ipynb) shows you how to stream prices from an `Oracle`.

### Market

A `Market` is an abstract entity to gather together access to the 3 specific market types that [entropy-explorer](https://github.com/blockworks-foundation/entropy-explorer) supports: Serum, Spot and Perp. [This example](ShowMarkets.ipynb) shows you how to access different market types and show their details.

### Market Operations: Show OrderBook

Once you have access to a `Market` you can show its `OrderBook`. [This example](ShowOrderBook.ipynb) shows you how.

### Market Operations: Place and Cancel Orders

If you have a `Market` and you have tokens, you can place and cancel `Order`s. [This example](PlaceAndCancelOrder.ipynb) shows you how.

### Market Operations: Show Own Orders

Often you just want to work with your own orders. [This example](ShowOwnOrders.ipynb) shows you how to retrieve only your own `Order`s from a `Market`.

### Market BUYs and SELLs

Sometimes - for example when hedging - you just want to place a 'take' `Order` with some assurance that it will be filled quickly within a specific slippage. For example, you might want to BUY 100 SOL at a price up to 2% higher than the current market price. 'Immediate Or Cancel' (IOC) orders allow you to always 'take' from the orderbook (they will never be on the book themselves), and the 'up to 2%' above is called the 'slippage'. [This example](ImmediateBuyAndSell.ipynb) shows you an easy way to submit IOC orders with slippage.

### Serum OpenOrders

Tracking down details of token transfers across Serum accounts can be tricky. One place that's hard to check sometimes is the `OpenOrders` account. [This example](ShowSerumOpenOrders.ipynb) shows you how to fetch and print an account's Serum `OpenOrders`.

### Spot OpenOrders

Entropy spot `OpenOrders` accounts are very similar to Serum `OpenOrders`, but are fetched slightly differently. This example shows you how to fetch and print an `Account`'s Spot `OpenOrders`.

### Perp OpenOrders

Perp `OpenOrders` are a little difference from Spot and Serum `OpenOrders`, in that they are contained directly inside the `Account` and have no independent address. [This example](ShowPerpOpenOrders.ipynb) shows you how to fetch and print an account's perp `OpenOrders`.

### Perp Event Queue

The `PerpEventQueue` holds `PerpFillEvent`s, `PerpOutEvent`a and `PerpLiquidateEvent`s, as they are processed. [This example](ShowPerpEventQueue.ipynb) shows you how to fetch and print all `PerpEventQueue` events.

### Streaming Perp Events

What if you want to watch the events appear in real-time? [This example](ShowStreamingPerpEvents.ipynb) shows you how to stream all perp events from a `PerpEventQueue`.

### Liquidity Mining

Entropy provides on-chain incentives for providing liquidity on perp markets. [This example](ShowLiquidityMiningInfo.ipynb) shows you how to view the current state of the liquidity incentives, how much has been given out already in the current period, how much remains to be given out, what the threshold is, and an estimate of when the current period will end.

## Combinable Instructions

`CombinableInstructions` are unique to `entropy-explorer` (as far as I know) and they aim to make code efficinet and clear at the same time. They're used frequently throughout `entropy-explorer` code and allow operations like:

```
(signers + do_something + do_something_else + cleanup).execute(context)
```

[This example](CombinableInstructions.ipynb) shows this pattern in practice by placing an order, cranking the market and settling any fill in one transaction.

## Combinable Instructions: Deposit and Withdraw

Depositing and withdrawing are non-market operations, so don't fit into the `MarketOperations` paradigm. They are still possible using `CombinableInstruction`s though! [This example](DepositAndWithdraw.ipynb) shows how to deposit and then withdraw Wrapped SOL to and from a Entropy `Account`.

## Combinable Instructions: Raw Transactions

Integration with other systems sometimes requires working with Solana's own `Transaction`s and `TransactionInstruction`s. `entropy-explorer` uses `CombinableInstructions` as its native format, so [this example](RawTransactions.ipynb) shows you how to extract the raw `TransactionInstruction`s and `keypair`s from the `CombinableInstructions` and run them in a raw Solana `Transaction`.

## Simple Marketmaker

Now that you can fetch prices and place and cancel orders, this example shows a simple marketmaker. [This example](SimpleMarketmaker.ipynb) is a slightly-reduced version of the `SimpleMarketMaker` in `entropy-explorer`, and it follows the same principles but allows you to run the code entirely in your browser.

## Practical: Run the Marketmaker (Perp)

This [much-more complete example](PracticalRunMarketmaker.ipynb) shows how to build and run the more-complete `MarketMaker`.

It walks through creating a custom `OrderChain`, how to add (and configure) specific `Element`s to the `OrderChain`, and how to build the `ModelState` for every 'pulse'.

It will then load and run the `MarketMaker`, with a fresh 'pulse' every 30 seconds. It will place `Order`s, cancel existing `Order`s, or leaving suitable `Order`s as they are.

This is the full `MarketMaker`, the same one run via the `marketmaker` command in the [Quickstart](https://github.com/blockworks-foundation/entropy-explorer/blob/main/docs/MarketmakingQuickstart.md), but with a custom (editable!) configuration, running in your browser.

## Practical: Run the Marketmaker (Spot)

This [spot-market example](PracticalRunMarketmakerSpot.ipynb) builds on the previous [perp-market example](PracticalRunMarketmaker.ipynb) to show how to run a marketmaker against a spot market and - importantly - show what similarities and differences there are.

The bulk of the code is the same, but spot markets use different mechanisms to load the `ModelState` and a different `CollateralCalculator`.

# Support

    🥭 Entropy Markets: https://entropy.trade
    📄 Documentation: https://docs.entropy.trade/
    💬 Discord: https://discord.gg/67jySBhxrg
    🐦 Twitter: https://twitter.com/entropymarkets
    🚧 Github: https://github.com/blockworks-foundation
    📧 Email: mailto:hello@blockworks.foundation
