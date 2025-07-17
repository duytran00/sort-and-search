/*
 * Starter code
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define P 10000
#define L 50

void insertionSort(char **words, int W);
void toLowerCase(char *word);
int binarySearch(char **sortedWords, int W, char *searchWord, int mode);

int main(int argc, char** argv) {
    FILE *fname = NULL;
    int mode = 0; // 0 - normal, 1 - verbose

    if (argc < 3 ) {
        perror("Not enough arguments. Need mode and filename, e.g.: 0 caps.txt");
        return 0;
    }
    else {
        fname = fopen(argv[2],"r");
        mode = atoi(argv[1]);
    }

    printf("mode: %d  file: %s\n", mode, argv[2]);  // KEEP THIS LINE

    if(fname == NULL){
        perror("error: file not found");
        exit(1);
    }

    // gets paragraph from file
    char paragraph[P];
    fgets(paragraph, sizeof(paragraph), fname);
    

    const char *delimiters = ": )(.,?!-/\t\n";
    int W = 0;  // Number of words in the paragraph
    char *ogParagraph[P];

    //makes words list from paragraph
    char *paragraphWords = strtok(paragraph,delimiters);
    while(paragraphWords != NULL){
        ogParagraph[W++] = paragraphWords;
        //get next token, returns NULL when there are no more tokens
        paragraphWords = strtok(NULL, delimiters);
    }

    // Tokenized words from the original paragraph will diaplay
    printf("\n-- Original data --\n");
    if(mode == 1){
        printf("i  | pointers[i]  | word\n");
        printf("---|--------------|--------\n");
    }
    for (int i = 0; i < W; i++){
        if (mode == 1) {
            // verbose mode
            printf("%d  | %p | %s\n", i,(void*)ogParagraph[i], ogParagraph[i]);
        }else {
            printf("%d\t%s\n", i, ogParagraph[i]);
        }
    }

    // Set up indirect sorting, modify pointers instead of original
    char *pointers[P];
    for (int i = 0; i < W; i++){
        pointers[i]=ogParagraph[i];
        //"cleaning" the words, make them all lowercase
        toLowerCase(pointers[i]);
    }

    insertionSort(pointers, W);

    // Display results of insertion sort
    printf("\n-- Clean and sorted data --\n");
    if (mode == 1) {
        printf("i  | pointers[i]  | word\n");
        printf("---|--------------|--------\n");
        for (int i = 0; i < W; i++) {
            printf("%d  | %p | %s\n", i, (void*)pointers[i], pointers[i]);
        }
    } else {
        // Normal mode
        for (int i = 0; i < W; i++) {
            printf("%d\t%s\n", i, pointers[i]);
        }
    }

    // Read search words from the file
    char searchWord[L];
    int S = 0; // Number of search words
    printf("\n-- Binary search --\n");

    while (fgets(searchWord, sizeof(searchWord), fname)) {
        // Remove newline character at the end
        searchWord[strcspn(searchWord, "\n")] = '\0';
        //"cleaning" the words, make them all lowercase
        toLowerCase(searchWord);

        //binary search output results
        binarySearch(pointers, W, searchWord, mode);
    }

    fclose(fname);

    return 0;
}

void insertionSort(char **words, int W){
     for (int i = 1; i < W; i++) {
        char *key = words[i];
        int j = i - 1;
        while (j >= 0 && strcmp(words[j], key) > 0) {
            words[j + 1] = words[j];
            j--;
        }
        words[j + 1] = key;
    }
}

void toLowerCase(char *word) {
    for (int i = 0; word[i]; i++) {
        word[i] = tolower(word[i]);
    }
}

int binarySearch(char **sortedWords, int W, char *searchWord, int mode) {
    int left = 0, right = W - 1;
    int iteration = 0;
    int found = 0;

    printf("%s\n", searchWord);

    while (left <= right) {
        iteration++;
        int mid = left + (right - left) / 2;

        // Print mid index for each iteration
        printf("%d", mid);
        if (left < right) printf(", ");

        int cmp = strcmp(sortedWords[mid], searchWord);
        if (cmp == 0) {
            found = 1;
            break;
        } else if (cmp < 0) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    printf(" (%d iterations) ", iteration);
    if (found) {
        printf("found");
    } else {
        printf("not found");
    }
    printf("\n");
}
