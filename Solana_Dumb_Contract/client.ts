import * as web3 from '@solana/web3.js';

async function main() {
    try {
        const connection = new web3.Connection(web3.clusterApiUrl('devnet'));
        const programId = new web3.PublicKey("JAZcYm2mHoEwuPz7wAv4xG8o48gCtwXv7FNbj7Bt88z"); // Ersetze dies mit deiner Programm-ID, falls sie sich geändert hat
        const payer = web3.Keypair.fromSecretKey(Uint8Array.from(
          [255,6,113,136,24,155,19,63,23,42,109,25,97,109,133,134,100,146,235,249,183,172,98,207,28,225,46,45,150,231,166,30,78,72,190,139,242,73,53,140,32,28,221,233,247,186,121,9,221,13,96,40,52,25,218,16,102,143,129,173,132,45,95,239]
        ));
        const flagAccount = web3.Keypair.generate();

        // Überprüfe das Wallet Guthaben
        const balance = await connection.getBalance(payer.publicKey);
        console.log(`Wallet Balance: ${balance / web3.LAMPORTS_PER_SOL} SOL`);

        // Flag Account erstellen
        const lamports = await connection.getMinimumBalanceForRentExemption(32 + 32 + 1); // 32 + 32 + 1 = FlagState::LEN
        const space = 32 + 32 + 1;

        console.log("Payer Pubkey:", payer.publicKey.toBase58());
        console.log("Flag Account Pubkey:", flagAccount.publicKey.toBase58());
        console.log("Lamports:", lamports);
        console.log("Space:", space);
        console.log("Program ID:", programId.toBase58());

        const createAccountInstruction = web3.SystemProgram.createAccount({
            fromPubkey: payer.publicKey,
            newAccountPubkey: flagAccount.publicKey,
            lamports,
            space,
            programId,
        });

        const transaction1 = new web3.Transaction().add(createAccountInstruction);

        try {
            await web3.sendAndConfirmTransaction(connection, transaction1, [payer, flagAccount]);
        } catch (error) {
            console.error("Fehler bei Account-Erstellung:", error);
            console.error(error);
            return; // Beende die Ausführung, wenn die Account-Erstellung fehlschlägt
        }

        // Flag-Contract initialisieren (Instruction Data leer)
        const initInstruction = new web3.TransactionInstruction({
            keys: [{ pubkey: flagAccount.publicKey, isSigner: false, isWritable: true }, { pubkey: payer.publicKey, isSigner: true, isWritable: true }],
            programId,
            data: Buffer.from([]),
        });

        const transaction2 = new web3.Transaction().add(initInstruction);
        await web3.sendAndConfirmTransaction(connection, transaction2, [payer]);

         //4. flag entsperren.
        const Unlockinstruction = new web3.TransactionInstruction({
          keys :[{pubkey: flagAccount.publicKey, isSigner: false, isWritable:true}, {pubkey: payer.publicKey, isSigner: true, isWritable: true}],
          programId,
          data : Buffer.from([1])
        });
        const transaction3 = new web3.Transaction().add(Unlockinstruction)
        await web3.sendAndConfirmTransaction(connection, transaction3, [payer])

        // 5. Flag abrufen (Instruction Data: [2])
        const retrieveFlagInstruction = new web3.TransactionInstruction({
            keys: [{ pubkey: flagAccount.publicKey, isSigner: false, isWritable: false }, {pubkey: payer.publicKey, isSigner: true, isWritable: true}],
            programId,
            data: Buffer.from([2]),
        });

        const transaction4 = new web3.Transaction().add(retrieveFlagInstruction);
        await web3.sendAndConfirmTransaction(connection, transaction4, [payer]);

        // 6. Account State ausgeben (optional)
        const accountInfo = await connection.getAccountInfo(flagAccount.publicKey);
        if (accountInfo) {
            console.log("Account Size after init:", accountInfo.data.length);
            console.log("Account Data:", accountInfo.data);
        }

    } catch (error) {
        console.error("Fehler:", error);
    }
}

main();