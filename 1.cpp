/*
 * Student Database using Dynamic Memory (malloc / realloc / free)
 * Operations: Add student, Display, Linear Search by ID, Binary Search by ID
 */
#include <iostream>
#include <iomanip>
#include <cstdlib>      // malloc, realloc, free
#include <cstring>      // strncpy
#include <limits>
using namespace std;

// Plain struct (fixed-size char array, no std::string) so that
// realloc() can safely move it to a new memory block.
struct Student {
    int id;
    char name[50];
    float cgpa;
};

Student* list = NULL;   // dynamically allocated array of students
int countS = 0;         // number of students stored
int capacity = 0;       // number of slots allocated
bool sortedByID = false;

// ---------- input helpers ----------
int readInt(const char* prompt) {
    int x;
    while (true) {
        cout << prompt;
        if (cin >> x) return x;
        if (cin.eof()) {                      // input ended: clean exit
            free(list);
            exit(0);
        }
        cout << "Invalid number. Try again.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

float readFloat(const char* prompt) {
    float x;
    while (true) {
        cout << prompt;
        if (cin >> x) return x;
        if (cin.eof()) {                      // input ended: clean exit
            free(list);
            exit(0);
        }
        cout << "Invalid number. Try again.\n";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
}

// ---------- memory expansion using realloc ----------
bool expandList() {
    int newCapacity = (capacity == 0) ? 2 : capacity * 2;
    Student* temp = (Student*) realloc(list, newCapacity * sizeof(Student));
    if (temp == NULL) {                       // old block is still valid
        cout << "Memory allocation failed!\n";
        return false;
    }
    cout << "[Memory expanded: " << capacity << " -> " << newCapacity
         << " slots, " << newCapacity * sizeof(Student) << " bytes]\n";
    list = temp;
    capacity = newCapacity;
    return true;
}

// ---------- 1. Add student ----------
void addStudent() {
    int id = readInt("Enter Student ID   : ");
    if (id <= 0) {
        cout << "ID must be a positive number.\n";
        return;
    }
    for (int i = 0; i < countS; i++) {
        if (list[i].id == id) {
            cout << "Student with ID " << id << " already exists.\n";
            return;
        }
    }

    char name[50];
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Enter Student Name : ";
    cin.getline(name, 50);
    if (cin.fail()) {                         // name longer than 49 chars
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    float cgpa = readFloat("Enter CGPA (0-10)  : ");
    if (cgpa < 0 || cgpa > 10) {
        cout << "CGPA must be between 0 and 10.\n";
        return;
    }

    if (countS == capacity && !expandList())
        return;

    list[countS].id = id;
    strncpy(list[countS].name, name, sizeof(list[countS].name) - 1);
    list[countS].name[sizeof(list[countS].name) - 1] = '\0';
    list[countS].cgpa = cgpa;
    countS++;
    sortedByID = false;                       // new entry may break order
    cout << "Student added. Total students: " << countS << "\n";
}

// ---------- 2. Display ----------
void printHeader() {
    cout << left << setw(8) << "ID" << setw(25) << "Name" << "CGPA\n";
    cout << string(38, '-') << "\n";
}

void printStudent(const Student& s) {
    cout << left << setw(8) << s.id << setw(25) << s.name
         << fixed << setprecision(2) << s.cgpa << "\n";
}

void displayAll() {
    if (countS == 0) {
        cout << "No students in the database.\n";
        return;
    }
    printHeader();
    for (int i = 0; i < countS; i++)
        printStudent(list[i]);
    cout << "Stored: " << countS << " / Capacity: " << capacity << "\n";
}

// ---------- 3. Linear Search: O(n), works on unsorted data ----------
int linearSearch(int key, int& comparisons) {
    comparisons = 0;
    for (int i = 0; i < countS; i++) {
        comparisons++;
        if (list[i].id == key)
            return i;
    }
    return -1;
}

// ---------- Sort by ID (insertion sort) for Binary Search ----------
void sortByID() {
    for (int i = 1; i < countS; i++) {
        Student key = list[i];
        int j = i - 1;
        while (j >= 0 && list[j].id > key.id) {
            list[j + 1] = list[j];
            j--;
        }
        list[j + 1] = key;
    }
    sortedByID = true;
}

// ---------- 4. Binary Search: O(log n), needs data sorted by ID ----------
int binarySearch(int key, int& comparisons) {
    int low = 0, high = countS - 1;
    comparisons = 0;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        comparisons++;
        cout << "  low=" << low << " high=" << high << " mid=" << mid
             << " (ID " << list[mid].id << ")\n";
        if (list[mid].id == key)
            return mid;
        else if (list[mid].id < key)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}

void searchMenu(bool binary) {
    if (countS == 0) {
        cout << "No students in the database.\n";
        return;
    }
    int key = readInt("Enter Student ID to search: ");
    int comparisons, pos;

    if (binary) {
        if (!sortedByID) {
            sortByID();
            cout << "List sorted by ID for Binary Search.\n";
        }
        pos = binarySearch(key, comparisons);
    } else {
        pos = linearSearch(key, comparisons);
    }

    if (pos != -1) {
        cout << "Record found at index " << pos << ":\n";
        printHeader();
        printStudent(list[pos]);
    } else {
        cout << "Student with ID " << key << " not found.\n";
    }
    cout << (binary ? "Binary" : "Linear") << " search comparisons: "
         << comparisons << "\n";
}

int main() {
    int choice;
    do {
        cout << "\n===== Student Database =====\n";
        cout << "1. Add Student\n";
        cout << "2. Display All Students\n";
        cout << "3. Linear Search by ID\n";
        cout << "4. Binary Search by ID\n";
        cout << "5. Exit\n";
        choice = readInt("Enter your choice: ");

        switch (choice) {
            case 1: addStudent(); break;
            case 2: displayAll(); break;
            case 3: searchMenu(false); break;
            case 4: searchMenu(true); break;
            case 5: cout << "Exiting program.\n"; break;
            default: cout << "Invalid choice! Try again.\n";
        }
    } while (choice != 5);

    free(list);                                // release dynamic memory
    list = NULL;
    return 0;
}
