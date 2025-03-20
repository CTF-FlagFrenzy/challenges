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

#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub struct FlagState {
    pub admin: Pubkey,
    pub flag_hash: [u8; 32],
    pub unlocked: bool,
}

impl Sealed for FlagState {}

impl IsInitialized for FlagState {
    fn is_initialized(&self) -> bool {
        true
    }
}

impl Pack for FlagState {
    const LEN: usize = 32 + 32 + 1; // Admin (32) + Flag Hash (32) + Unlocked (1)

    fn unpack_from_slice(src: &[u8]) -> Result<Self, ProgramError> {
        let src = array_ref![src, 0, 32 + 32 + 1]; // Ersetzt Self::LEN
        let (admin_bytes, flag_hash_bytes, unlocked_bytes) = array_refs![src, 32, 32, 1];

        Ok(FlagState {
            admin: Pubkey::new_from_array(*admin_bytes),
            flag_hash: *flag_hash_bytes,
            unlocked: unlocked_bytes[0] != 0,
        })
    }

    fn pack_into_slice(&self, dst: &mut [u8]) {
        let dst = array_mut_ref![dst, 0, 32 + 32 + 1]; // Ersetzt Self::LEN
        let (admin_dst, flag_hash_dst, unlocked_dst) = mut_array_refs![dst, 32, 32, 1];

        admin_dst.copy_from_slice(self.admin.as_ref());
        flag_hash_dst.copy_from_slice(&self.flag_hash);
        unlocked_dst[0] = self.unlocked as u8;
    }
}

entrypoint!(process_instruction);

pub fn process_instruction(
    program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("Program started");
    let accounts_iter = &mut accounts.iter();
    let flag_account = next_account_info(accounts_iter)?;
    let signer_account = next_account_info(accounts_iter)?;

    if flag_account.owner != program_id {
        msg!("Incorrect program ID");
        return Err(ProgramError::IncorrectProgramId);
    }
    msg!("Program ID correct");

    let mut flag_state = FlagState::unpack_unchecked(&flag_account.data.borrow())?;

    if instruction_data.is_empty() {
        msg!("Initializing...");
        flag_state.admin = *signer_account.key;
        flag_state.flag_hash = hash(b"RkZ7N2FhNzE5NzNkNWM0NzAzZWYzOTY0ODgzM2ViOGM4OTJkZnNkZjQwMmVkYzUyYjdhMjk0NGFkOTgzMGIyMmRhY30=").to_bytes();
        flag_state.unlocked = false;
        FlagState::pack_into_slice(&flag_state, &mut flag_account.data.borrow_mut());
        return Ok(());
    }

    if signer_account.key == &flag_state.admin && instruction_data.len() == 1 && instruction_data[0] == 1 {
        msg!("Unlock");
        flag_state.unlocked = true;
        FlagState::pack_into_slice(&flag_state, &mut flag_account.data.borrow_mut());
        return Ok(());
    }

    if instruction_data.len() == 1 && instruction_data[0] == 2 && flag_state.unlocked {
        msg!("Flag parts:");
        print_flag_part_1();
        print_flag_part_2();
        print_flag_part_3();
        print_flag_part_4();
        return Ok(());
    }

    Err(ProgramError::InvalidInstructionData)
}

fn print_flag_part_1() {
    msg!("RkZ7N2FhNzE5NzNk");
}

fn print_flag_part_2() {
    msg!("NWM0NzAzZWYzOTY0");
}

fn print_flag_part_3() {
    msg!("ODgzM2ViOGM4OTJk");
}

fn print_flag_part_4() {
    msg!("ZnNkZjQwMmVkYzUyYjdhMjk0NGFkOTgzMGIyMmRhY30=");
}