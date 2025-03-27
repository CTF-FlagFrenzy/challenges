# Solana Dumb Contract Challenge Writeup

## Challenge Overview

This challenge involves interacting with a Solana smart contract to unlock and retrieve a hidden flag. The smart contract has been deployed on the Solana devnet with the program ID `JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z`.

1. Initialize the contract with no instruction data
2. Unlock the flag (instruction data `[1]`) - only the admin can do this
3. Retrieve the flag (instruction data `[2]`) - only works if the flag is unlocked

The flag is stored directly in the contract code, and the contract prints it when requested.

## Solution Method 1: Using Solana CLI

I'll demonstrate how to solve this challenge by directly interacting with the contract using the Solana CLI.

### Step 1: Setup Environment

First, set up the Solana CLI to use the devnet cluster:

```bash
solana config set --url devnet
```

### Step 2: Create a Keypair for the Payer Account

We'll create a keypair file for our payer account that will match the one used in the client code:

```bash
# Save the private key from the client code to a file
echo "[255,6,113,136,24,155,19,63,23,42,109,25,97,109,133,134,100,146,235,249,183,172,98,207,28,225,46,45,150,231,166,30,78,72,190,139,242,73,53,140,32,28,221,233,247,186,121,9,221,13,96,40,52,25,218,16,102,143,129,173,132,45,95,239]" > payer_array.json

# Convert the JSON array to a binary keypair file
solana-keygen recover -o payer.json 'prompt:?key=array:255,6,113,136,24,155,19,63,23,42,109,25,97,109,133,134,100,146,235,249,183,172,98,207,28,225,46,45,150,231,166,30,78,72,190,139,242,73,53,140,32,28,221,233,247,186,121,9,221,13,96,40,52,25,218,16,102,143,129,173,132,45,95,239'
```

### Step 3: Fund the Payer Account

We need SOL in our payer account to pay for transactions:

```bash
solana airdrop 2 $(solana address -k payer.json)
```

### Step 4: Create a Flag Account

Generate a new keypair for the flag account:

```bash
solana-keygen new -o flag_account.json
```

Then create the account and allocate space for the flag state (65 bytes: 32 for admin + 32 for flag hash + 1 for unlocked flag):

> [!IMPORTANT]
> Use the account size 65 (information in description)


```bash
solana create-account \
  --from payer.json \
  --keypair flag_account.json \
  --lamports $(solana minimum-balance-for-rent-exemption 65) \
  --space 65 \
  --program-id JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z
```

### Step 5: Initialize the Contract

Initialize the contract by sending an empty instruction:

```bash
solana program invoke \
  --program-id JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z \
  --keypair payer.json \
  '' \
  $(solana address -k flag_account.json) \
  $(solana address -k payer.json)
```

This calls the contract with no instruction data, which triggers the initialization code path. The contract sets our payer as the admin and initializes the flag state.

### Step 6: Unlock the Flag

Send instruction data `[1]` to unlock the flag:

```bash
solana program invoke \
  --program-id JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z \
  --keypair payer.json \
  '01' \
  $(solana address -k flag_account.json) \
  $(solana address -k payer.json)
```

### Step 7: Retrieve the Flag

Finally, send instruction data `[2]` to retrieve the flag:

```bash
solana program invoke \
  --program-id JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z \
  --keypair payer.json \
  '02' \
  $(solana address -k flag_account.json) \
  $(solana address -k payer.json)
```

The contract will print the flag in the program logs, which can be viewed either in the output of the command or by running:

```bash
solana logs | grep "FF{"
```

### The Flag

After executing the retrieve flag instruction, we can see that the flag is:

```
FF{e7aa71973d5c4703ef39648833eb8c892dfsdf402edc52b7a2944ad9830b22dac}
```

## Solution Method 2: Analyzing the Contract Source Code

Instead of interacting with the contract, we can directly analyze the source code to extract the flag. This approach is much faster and doesn't require going through the initialization and unlocking process.

### Step 1: Dump the Contract Binary

First, we need to download the compiled contract from the blockchain:

```bash
# Create a directory to store the program binary
mkdir -p program_dump

# Dump the program binary from the chain
solana program dump JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z program_dump/dumb_contract.so
```

### Step 2: Disassemble or Analyze the Binary

Once we have the binary, we can use tools to analyze it:

```bash
# For ELF binaries, we can view strings that might contain the flag
strings program_dump/dumb_contract.so | grep -i "FF{"

# Or disassemble the binary to look at its instructions
objdump -d program_dump/dumb_contract.so > program_dump/disassembly.txt
```

### Step 3: Locate the Flag in the Code

In this case, looking through the binary or disassembly, we can find the flag embedded directly in the code:

```
FF{e7aa71973d5c4703ef39648833eb8c892dfsdf402edc52b7a2944ad9830b22dac}
```

This approach bypasses the need to interact with the contract completely, allowing us to extract the flag directly from the program binary. 

If the source code is available (as it was in this challenge), we can also directly examine it to find where the flag might be hidden:

```rust
    if instruction_data.len() == 1 && instruction_data[0] == 2 && flag_state.unlocked {
        msg!("FF{e7aa71973d5c4703ef39648833eb8c892dfsdf402edc52b7a2944ad9830b22dac}");
        return Ok(());
    }
```

### Step 4: Verify the Flag Format

The flag follows the expected format `FF{...}`, confirming that our extraction was correct.