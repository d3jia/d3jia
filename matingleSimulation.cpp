#include <iostream>
#include <random>
#include <map>

using namespace std;

// Return (True/False) randomly.
bool roll_dice()
{
    return rand() > (RAND_MAX / 2);
}

int main(void)
{
    cout << "-----------------------\nWelcome to Casino\n-----------------------\n";

    // Variable for Main Logic:
    int stageNow = 1;          // For whileLoop Stages
    int walletAmount = 0;      // Initial capital
    int maximumRoundLimit = 0; // Maximum game iteration
    int satisfyingAmount = 0;  // If walletAmount == satisfyingAmount, End game;
    int originalBetAmount = 0; // To store bet amount which user sets

    // Variable to Calculate Leading Zero
    int temp_maxRound_toCalculate_leadingZeros = 0;
    int leadingZerosForRounds = 0;

    // Stage 1: Enter Wallet Amount
    while (stageNow == 1)
    {
        cout << "How much did money did you bring?: ";
        cin >> walletAmount;

        // Input Validation
        if (walletAmount <= 0)
        {
            cout << "Amount cannot be <= zero, enter again: ";
            cin >> walletAmount;
        }
        else
        {
            stageNow = 2; // Go to stage 2
        }
    }

    // Stage 2: How much you wanna bet each round?
    while (stageNow == 2)
    {
        cout << "How much you wanna bet each round?: ";
        cin >> originalBetAmount;

        // Input Validation
        if (originalBetAmount <= 0)
        {
            cout << "Betting amount cannot be <= zero, enter again: ";
            cin >> originalBetAmount;
        }
        else
        {
            stageNow = 3; // Go to stage 3
        }
    }

    // Stage 3: Enter Fixed Times Of Betting
    while (stageNow == 3)
    {
        cout << "What is the maximum rounds you intend to play?: ";
        cin >> maximumRoundLimit;

        // Input Validation
        if (maximumRoundLimit <= 0)
        {
            cout << "Invalid round number, enter again: ";
            cin >> maximumRoundLimit;

            // To be used when computing LeadingZeros ("Round #### | ...") output at stage 4:
            temp_maxRound_toCalculate_leadingZeros = maximumRoundLimit;
            while (temp_maxRound_toCalculate_leadingZeros > 0)
            {
                leadingZerosForRounds++;
                temp_maxRound_toCalculate_leadingZeros /= 10;
            }
        }
        else
        {
            stageNow = 4; // Go to stage 3
        }
    }

    // Stage 4: Enter Satisfying Amount to Chicken out
    while (stageNow == 4)
    {
        cout << "Chicken out at how much winning?: ";
        cin >> satisfyingAmount;
        if (satisfyingAmount <= 0)
        {
            cout << "Expected winning cannot be <= zero, enter again: ";
            cin >> satisfyingAmount;
        }
        else
        {
            stageNow = 5; // Go to stage 3
        }
    }

    // Stage 5: Martingle Simulation
    int roundCount = 0;             // To Count Round #
    int theBet = originalBetAmount; // dynamic runtime Bet integer (for doubling down)
    bool lastRoundWin = false;      // Simple Boolean used to determine if need to double down (for each rounds)

    // Main Logic (Stage4 & LessThanMaxRoundCount & WalletHaveMoney & WalletHaveEnoughToBet
    while (stageNow == 5)
    {
        // End Condition #1 - Check round limit reached, Yes? End
        if (roundCount > maximumRoundLimit)
        {
            cout << "Round Limit Reached --> (END)\n";
            stageNow = 502;
            break;
        }
        // End Condition #2 - Check if have sufficient fund, No? End
        if (walletAmount < originalBetAmount)
        {
            cout << "Insufficient Fund for minimum bet --> (END)\n";
            stageNow = 51;
            break;
        }

        roundCount++; // Keep track rounds

        // (If last round won) -> reset Amount / (if last round lose) -> double down the bet
        if (lastRoundWin == true)
        {
            theBet = originalBetAmount;
        }
        else // If last round lose, double down the bet:
        {
            theBet *= 2;
            // Check if doubleDown bet is exceeding total wallet amount.
            if (theBet > walletAmount)
            {
                // if yes, switch back to start betting from original amount.
                theBet = originalBetAmount;
            }
        }

        // Wallet - betAmount (Insert Bet Amount into Casino)
        walletAmount -= theBet; 

        if (roll_dice() == true)
        {
            // If win, receive x2 of what they bet.
            walletAmount = walletAmount + (theBet * 2);
            lastRoundWin = true;
        }
        else
        {
            // If lose, lastRoundWin changed to 0, next round double down.
            lastRoundWin = false;
        }
        // Output Line Spam
        printf("Round %0*d | Wallet Amount: $%d | Target Amount: $%d | Bet Amount: $%d | Stop at: %d | %s \n", leadingZerosForRounds, roundCount, walletAmount, satisfyingAmount, theBet, maximumRoundLimit, lastRoundWin? "True" : "False");
    }
}