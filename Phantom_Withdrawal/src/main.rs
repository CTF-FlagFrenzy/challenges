use anchor_lang::prelude::*;

//! Passphrase 3qEXWbmfcNeD45W6JHqs9sxqKwxzUHpiYhfjpM5EZJ3f
//! Keypair phrase 5knmdBUdEy5dFdVQ2UA6jWiCohc792YvZyW9UhGKCfJH
// Signature 22ge66F2haDSzLZ88JQRaiDpYuANsU5M2S1ek6WC363A3jFkcXfsvPtn5tesxRVcTDYesCSLLPu1qQR6cZBRED5m

// Programm-ID (ersetze mit deiner echten Programm-ID)
declare_id!("2hqzq3E2y3i3RBWTQsSHm8kLyHUzKue8wB1kDLkASw8z");

#[program]
pub mod solana_bank_ctf {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        ctx.accounts.bank_account.balance = 0;
        Ok(())
    }

    pub fn deposit(ctx: Context<Deposit>, amount: u64) -> Result<()> {
        ctx.accounts.bank_account.balance += amount;
        Ok(())
    }

    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
        // SCHWACHSTELLE: Keine echte Token-Überprüfung, nur interner Wert
        if amount > ctx.accounts.bank_account.balance {
            // Ermöglicht es, mehr abzuheben, als eingezahlt wurde
            ctx.accounts.bank_account.balance = ctx.accounts.bank_account.balance.wrapping_sub(amount);
        } else {
            ctx.accounts.bank_account.balance -= amount;
        }
        Ok(())
    }

    pub fn get_flag(ctx: Context<GetFlag>) -> Result<()> {
        if ctx.accounts.bank_account.balance > 1_000_000 {
            msg!("Glückwunsch! Hier ist deine Flag: FF{180045c7c83eb69bc245539f76b1bbf14a25e071f63d0e3bf4ab83b56b2b9642}");
        } else {
            msg!("Noch nicht genug Guthaben, versuch es weiter!");
        }
        Ok(())
    }
}

#[account]
pub struct BankAccount {
    pub balance: u64,
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 8)]
    pub bank_account: Account<'info, BankAccount>,
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Deposit<'info> {
    #[account(mut)]
    pub bank_account: Account<'info, BankAccount>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    #[account(mut)]
    pub bank_account: Account<'info, BankAccount>,
}

#[derive(Accounts)]
pub struct GetFlag<'info> {
    #[account(mut)]
    pub bank_account: Account<'info, BankAccount>,
}
