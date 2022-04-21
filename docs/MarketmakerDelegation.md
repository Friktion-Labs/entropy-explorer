# 🥭 Entropy Explorer

# 🔥 Delegation

Entropy Account Delegation is a feature that allows a separate account limited access to the Entropy Account's features.

A delegated account _can_, for example:

- Deposit funds
- Place orders
- Cancel orders

A delegated account _cannot_, for example:

- Withdraw funds
- Close the Entropy Account

Using a delegate account allows you to keep your powerful Entropy Account keys off your server (and possibly in a hardware or cold wallet) and use a more limited delegated account to sign and pay for transactions.

This walkthrough will show you how to set up delegation for a Entropy Account used by a marketmaker.

# 1. Create An 'AccountRunner' Account

First thing to do - create the Solana 'account runner' account. This is the limited-privilege account that will sign and pay SOL for your marketmaker transactions, but won't be able to withdraw tokens.

Let's be fancy and ask for an account whose address starts with 'Dgt' so we can remember it's a delegate account. Run the command:

```
solana-keygen grind --starts-with Dgt:1
```

This should give a response like:

```
Searching with 8 threads for:
	1 pubkey that starts with 'Dgt' and ends with ''
Wrote keypair to DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y.json
```

The account address your command generates will (obviously) be different, but this walkthrough will use `DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y` as the Delegate Account address, and `Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ` as the Entropy Account address. Substitute your own delegate and entropy account addresses in commands.

# 2. Fund 'AccountRunner' Account

The marketmaker will be 'running' as this account. Since the delegate account will be signing transactions, it needs SOL to pay the transaction fees.

There are lots of ways to transfer SOL to the account runner. Most folks will probably use Phantom or Sollet to send SOL, and that works just fine.

Here we'll use a command to transfer 1 SOL since that's simpler to show:

_Run as whatever account has the SOL you want to send_

```
send-sols --address DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y --quantity 1
```

# 3. Set 'AccountRunner' As Delegate

A Entropy Account can have _at most one_ delegate. This command will grant the Delegate Account limited access to the Entropy Account, removing any existing delegate on that Entropy Account:

_Run as Owner of the Entropy Account_

```
delegate-account --account-address Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ --delegate-address DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y
```

# 4. Verify 'AccountRunner' Is Shown As Delegate

It's always worth checking to see if the command worked as expected. If you examine the account now, you should see `DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y` listed as the delegate.

_Run as Owner of the Entropy Account_

```
show-accounts
```

This should sow the address of the AccountRunner Delegate in the 'Delegated To' line (abridged):

```
« Account (un-named), Version.V3 [Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ]
...
    Delegated To: DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y
...
```

(If it _doesn't_ show `DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y` in the 'Delegated To:' line, something has probably gone wrong with Step 3 above.)

# 5. Update Marketmaker Account Credentials

The marketmaker needs to load the 'AccountRunner' secret keys now instead of the Entropy Account owner's secret keys.

What needs to be done here depends greatly on how you are currently loading the secret keys.

**IMPORTANT!** Take a backup of your current Entropy Account owner credentials and keep that backup safe! If you lose access to these credentials you will lose access to your Entropy Account. These are the keys that allow you to close your Entropy Account and withdraw tokens from it - this is the account you need to keep safe! We're using a delegate account here specifically so we can protect these credentials and get them off the marketmaker server!

For instance, if you followed the [Marketmaking Quickstart](MarketmakingQuickstart.md), you would:

- take a copy of your current `~/entropy-explorer/id.json` file.
- keep that copy safe, preferably not on the server running your marketmaker.
- copy your new `DgtBbuXgmmdHvbcXusQWFmJPToCo1Ump3E3h8scP3A7y.json` file to `~/entropy-explorer/id.json`, overwriting the old contents.

# 6. Update Marketmaker Command

The marketmaker needs to be told which Entropy Account to use. The AccountRunner delegate account has no Entropy Accounts of its own (probably...) so it won't automatically find the right account to work with. We need to explicitly tell the marketmaker which Entropy Account address to use.

This is done by passing the `--account-address` parameter.

To tell your marketmaker to load the Entropy Account `Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ`, update the command used to start your marketmaker with the following:

```
--account-address Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ
```

# 7. Run Your Marketmaker!

That's it - your marketmaker should now be configured to run using a lower-privilege Account Runner delegate account.

You can still use your Entropy Account owner credentials to manage your Entropy Account and withdraw tokens, but the day-to-day running of the marketmaker transactions can be done using the Account Runner delegate account. (Remember to keep it topped up with enough SOL)

# (Optional) Revoke Delegation

If you want to disable the Account Runner's ability to trade using your Entropy Account, you can revoke its access:

_Run as Owner of the Entropy Account_

```
delegate-account --account-address Mngpjk8KJR5uPs6UvYefvzReahdjTeYcqKin1WgVGNZ --revoke
```

This will return the account to its regular state where only the Entropy Account owner can use it.
