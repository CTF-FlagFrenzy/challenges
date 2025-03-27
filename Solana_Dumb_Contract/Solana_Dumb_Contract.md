# Solana Dumb Contract Documentation

This document provides a comprehensive guide to understanding, deploying, and interacting with the Solana Dumb Contract.

## Contract Overview

The Solana Dumb Contract is a simple Solana program that manages a flag value with basic access control. The contract stores a hash of a flag and allows only an admin to unlock it. Once unlocked, the flag can be retrieved by anyone.

The contract serves as a good example of:
- Basic Solana program structure
- Account data management
- Simple access control mechanisms
- Instruction processing

## Contract Structure

The contract is written in Rust and uses the Solana Program SDK. Here's the main structure:

```rust
use solana_program::{
    account_info::{next_account_info, AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    program_error::ProgramError,
    pubkey::Pubkey,
    program_pack::{IsInitialized, Pack, Sealed},
    hash::{hash, Hash},
};
use arrayref::{array_ref, array_refs, array_mut_ref, mut_array_refs};
use borsh::{BorshDeserialize, BorshSerialize};

// State structure
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct FlagState {
    pub admin: Pubkey,
    pub flag_hash: [u8; 32],
    pub unlocked: bool,
}

// Program entrypoint
entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    // Instruction processing logic
}
```

## State Management

The contract maintains state in a `FlagState` structure that is stored in a dedicated account. This structure implements the Solana `Pack` trait for serialization and deserialization:

```rust
impl Pack for FlagState {
    const LEN: usize = 32 + 32 + 1; // Admin (32) + Flag Hash (32) + Unlocked (1)

    fn unpack_from_slice(src: &[u8]) -> Result<Self, ProgramError> {
        let src = array_ref![src, 0, 32 + 32 + 1];
        let (admin_bytes, flag_hash_bytes, unlocked_bytes) = array_refs![src, 32, 32, 1];

        Ok(FlagState {
            admin: Pubkey::new_from_array(*admin_bytes),
            flag_hash: *flag_hash_bytes,
            unlocked: unlocked_bytes[0] != 0,
        })
    }

    fn pack_into_slice(&self, dst: &mut [u8]) {
        let dst = array_mut_ref![dst, 0, 32 + 32 + 1];
        let (admin_dst, flag_hash_dst, unlocked_dst) = mut_array_refs![dst, 32, 32, 1];

        admin_dst.copy_from_slice(self.admin.as_ref());
        flag_hash_dst.copy_from_slice(&self.flag_hash);
        unlocked_dst[0] = self.unlocked as u8;
    }
}
```

The state consists of:
- `admin`: The public key of the account that can unlock the flag
- `flag_hash`: A hash of the flag value
- `unlocked`: A boolean indicating whether the flag is unlocked

## Instructions

The contract supports three instructions:

### 1. Initialize (Empty instruction data)

This instruction initializes the contract state:
- Sets the calling account as the admin
- Sets the flag hash
- Sets the unlocked state to false

```rust
if instruction_data.is_empty() {
    msg!("Initializing...");
    flag_state.admin = *signer_account.key;
    flag_state.flag_hash = hash(b"FF{e7aa71973d5c4703ef39648833eb8c892dfsdf402edc52b7a2944ad9830b22dac}").to_bytes();
    flag_state.unlocked = false;
    FlagState::pack_into_slice(&flag_state, &mut flag_account.data.borrow_mut());
    return Ok(());
}
```

### 2. Unlock Flag (Instruction data: `[1]`)

This instruction unlocks the flag, but only if called by the admin:

```rust
if signer_account.key == &flag_state.admin && instruction_data.len() == 1 && instruction_data[0] == 1 {
    msg!("Unlock");
    flag_state.unlocked = true;
    FlagState::pack_into_slice(&flag_state, &mut flag_account.data.borrow_mut());
    return Ok(());
}
```

### 3. Retrieve Flag (Instruction data: `[2]`)

This instruction retrieves the flag, but only if it has been unlocked:

```rust
if instruction_data.len() == 1 && instruction_data[0] == 2 && flag_state.unlocked {
    msg!("FF{e7aa71973d5c4703ef39648833eb8c892dfsdf402edc52b7a2944ad9830b22dac}");
    return Ok(());
}
```

## Deployment Guide

To deploy the Solana Dumb Contract to the Solana blockchain, follow these steps:

### Prerequisites
- Install Rust and Cargo
- Install Solana CLI tools
- Configure Solana CLI to use the desired network (e.g., devnet, testnet)

### Build the Program

1. Clone the repository containing the contract code
2. Build the program using the Solana BPF toolchain:

```bash
# In the directory containing lib.rs
cargo build-bpf
```

This will create a compiled `.so` file in the `target` directory.

### Deploy the Program

Deploy the compiled program to the Solana blockchain:

```bash
solana program deploy target/deploy/solana_dumb_contract.so
```

This command will output the Program ID, which you'll need for client interactions.

## Client Interaction

The contract can be interacted with using the Solana web3.js library. Here's a TypeScript example demonstrating how to interact with the contract:

```typescript
import * as web3 from '@solana/web3.js';

async function interactWithContract() {
    // Connect to the Solana network
    const connection = new web3.Connection(web3.clusterApiUrl('devnet'));
    
    // Replace with your program ID
    const programId = new web3.PublicKey("JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z");
    
    // Create or import a keypair for the payer account
    const payer = web3.Keypair.generate();
    
    // Create a keypair for the flag account
    const flagAccount = web3.Keypair.generate();
    
    // Calculate the minimum lamports needed for rent exemption
    const lamports = await connection.getMinimumBalanceForRentExemption(65); // 32 + 32 + 1 = FlagState::LEN
    
    // Create the flag account
    const createAccountInstruction = web3.SystemProgram.createAccount({
        fromPubkey: payer.publicKey,
        newAccountPubkey: flagAccount.publicKey,
        lamports,
        space: 65,
        programId,
    });
    
    // Send transaction to create the account
    await web3.sendAndConfirmTransaction(
        connection, 
        new web3.Transaction().add(createAccountInstruction), 
        [payer, flagAccount]
    );
    
    // Initialize the contract
    const initInstruction = new web3.TransactionInstruction({
        keys: [
            { pubkey: flagAccount.publicKey, isSigner: false, isWritable: true },
            { pubkey: payer.publicKey, isSigner: true, isWritable: true }
        ],
        programId,
        data: Buffer.from([]),
    });
    
    await web3.sendAndConfirmTransaction(
        connection, 
        new web3.Transaction().add(initInstruction), 
        [payer]
    );
    
    // Unlock the flag
    const unlockInstruction = new web3.TransactionInstruction({
        keys: [
            { pubkey: flagAccount.publicKey, isSigner: false, isWritable: true },
            { pubkey: payer.publicKey, isSigner: true, isWritable: true }
        ],
        programId,
        data: Buffer.from([1]),
    });
    
    await web3.sendAndConfirmTransaction(
        connection, 
        new web3.Transaction().add(unlockInstruction), 
        [payer]
    );
    
    // Retrieve the flag
    const retrieveFlagInstruction = new web3.TransactionInstruction({
        keys: [
            { pubkey: flagAccount.publicKey, isSigner: false, isWritable: false },
            { pubkey: payer.publicKey, isSigner: true, isWritable: true }
        ],
        programId,
        data: Buffer.from([2]),
    });
    
    await web3.sendAndConfirmTransaction(
        connection, 
        new web3.Transaction().add(retrieveFlagInstruction), 
        [payer]
    );
    
    // To see the flag, you need to check the transaction logs
    console.log("Check transaction logs for the flag");
}
```

## Security Considerations

The Solana Dumb Contract, while simple, demonstrates some security patterns but also has limitations:

### Positive Security Aspects
- Validates the program ID in the account ownership check
- Implements access control for the unlock operation

### Security Considerations
1. The flag is hardcoded in the program, which is visible in the blockchain
2. The contract uses a simple boolean for access control rather than more sophisticated mechanisms
3. There's no time-based locking or other advanced security features

### Best Practices for Production
For a production version of this contract, consider:
- Using on-chain encryption for sensitive data
- Implementing multi-signature requirements for critical operations
- Adding time-locks or other security constraints
- Proper error handling with specific error codes

## Conclusion

The Solana Dumb Contract demonstrates fundamental concepts in Solana program development, including account management, state serialization, and instruction processing. While simple, it provides a foundation for understanding more complex Solana programs.

**HAVE FUN**

> [!NOTE]
> If you have any problems solving this challenge, you can find a detailed writeup [here](https://github.com/CTF-FlagFrenzy/challenges/blob/main/Solana_Dumb_Contract/writeup.md)