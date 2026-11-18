#include <iostream>
using namespace std;

#define SIZE 5

class CircularQueue {
    int q[SIZE];
    int front, rear;

public:
    CircularQueue() {
        front = -1;
        rear = -1;
    }

    bool isFull() {
        return (rear + 1) % SIZE == front;
    }

    bool isEmpty() {
        return front == -1;
    }

    void enqueue(int x) {
        if (isFull()) {
            cout << "Queue Overflow! Cannot insert " << x << ".\n";
            return;
        }
        if (isEmpty())
            front = 0;
        rear = (rear + 1) % SIZE;
        q[rear] = x;
        cout << x << " inserted successfully.\n";
    }

    void dequeue() {
        if (isEmpty()) {
            cout << "Queue Underflow! Queue is empty.\n";
            return;
        }
        int x = q[front];
        if (front == rear) {
            front = rear = -1;      // queue becomes empty
        } else {
            front = (front + 1) % SIZE;
        }
        cout << x << " deleted successfully.\n";
    }

    void display() {
        if (isEmpty()) {
            cout << "Queue is Empty.\n";
            return;
        }
        cout << "Queue elements: ";
        int i = front;
        while (true) {
            cout << q[i] << " ";
            if (i == rear)
                break;
            i = (i + 1) % SIZE;
        }
        cout << "\nFront = " << front << ", Rear = " << rear << endl;
    }
};

int main() {
    CircularQueue cq;
    int choice, value;

    do {
        cout << "\n----- Circular Queue Menu -----\n";
        cout << "1. Insert (Enqueue)\n";
        cout << "2. Delete (Dequeue)\n";
        cout << "3. Display\n";
        cout << "4. Exit\n";
        cout << "Enter your choice: ";
        if (!(cin >> choice)) break;     // stop cleanly at end of input

        switch (choice) {
            case 1:
                cout << "Enter value to insert: ";
                cin >> value;
                cq.enqueue(value);
                break;
            case 2:
                cq.dequeue();
                break;
            case 3:
                cq.display();
                break;
            case 4:
                cout << "Exiting program.\n";
                break;
            default:
                cout << "Invalid choice! Try again.\n";
        }
    } while (choice != 4);

    return 0;
}
