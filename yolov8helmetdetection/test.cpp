#include <iostream>
using namespace std;

// Function to decrypt a single character
char decryptChar(char cipherChar, char keyChar) {
    int c = toupper(cipherChar) - 'A';
    int k = toupper(keyChar) - 'A';
    int p = (c - k + 26) % 26;
    return p + 'A';
}

int main() {
    string ciphertext, keyword, plaintext = "";

    // Input from user
    cout << "Enter ciphertext (uppercase, no spaces): ";
    cin >> ciphertext;
    cout << "Enter keyword (uppercase, no spaces): ";
    cin >> keyword;

    int keywordLength = keyword.length();

    // Decrypt character by character
    for (int i = 0; i < ciphertext.length(); i++) {
        char cipherChar = ciphertext[i];
        char keyChar = keyword[i % keywordLength];
        char plainChar = decryptChar(cipherChar, keyChar);
        plaintext += plainChar;
    }

    // Output
    cout << "Decrypted plaintext: " << plaintext << endl;

    return 0;
}