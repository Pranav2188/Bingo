class Order:
    def __init__(self, order_id, item, time):
        self.order_id = order_id
        self.item = item
        self.time = time                       # estimated delivery time (minutes)

    def __str__(self):
        return f"{self.order_id:<9}{self.item:<14}{self.time:>6} min"


def times(orders):
    return "[" + " ".join(str(o.time) for o in orders) + "]"


def merge(a, temp, low, mid, high, stats):
    """Merge sorted runs a[low..mid] and a[mid+1..high] using buffer temp."""
    i, j, k = low, mid + 1, low
    while i <= mid and j <= high:
        stats["comparisons"] += 1
        if a[i].time <= a[j].time:             # '<=' keeps equal times in input order
            temp[k] = a[i]
            i += 1
        else:
            temp[k] = a[j]
            j += 1
        k += 1
    while i <= mid:                            # copy rest of left run
        temp[k] = a[i]
        i += 1
        k += 1
    while j <= high:                           # copy rest of right run
        temp[k] = a[j]
        j += 1
        k += 1
    for k in range(low, high + 1):             # copy merged run back
        a[k] = temp[k]


def _merge_sort(a, temp, low, high, depth, trace, stats):
    if low >= high:                            # one order: already sorted
        return
    mid = (low + high) // 2
    pad = "  " * depth
    if trace:
        print(f"{pad}Divide: {times(a[low:high + 1])} -> "
              f"{times(a[low:mid + 1])} {times(a[mid + 1:high + 1])}")
    _merge_sort(a, temp, low, mid, depth + 1, trace, stats)          # conquer left
    _merge_sort(a, temp, mid + 1, high, depth + 1, trace, stats)     # conquer right
    stats["comparisons"] += 1
    if a[mid].time <= a[mid + 1].time:         # runs already in order: skip merge
        if trace:
            print(f"{pad}Merge : {times(a[low:high + 1])} (already in order)")
        return
    merge(a, temp, low, mid, high, stats)                            # combine
    if trace:
        print(f"{pad}Merge : {times(a[low:high + 1])}")


def merge_sort(orders, trace=True):
    """Returns a new list sorted by delivery time; input list is unchanged."""
    a = orders[:]
    temp = [None] * len(a)                     # one buffer reused by every merge
    stats = {"comparisons": 0}
    _merge_sort(a, temp, 0, len(a) - 1, 0, trace, stats)
    return a, stats


def display(orders, title):
    print(f"\n{title}")
    print(f"{'No.':<5}{'Order ID':<9}{'Item':<14}{'Time':>10}")
    print("-" * 38)
    for n, o in enumerate(orders, start=1):
        print(f"{n:<5}{o}")


def sample_orders():
    data = [("ORD101", "Groceries", 45), ("ORD102", "Pizza", 30),
            ("ORD103", "Medicines", 15), ("ORD104", "Electronics", 120),
            ("ORD105", "Books", 60), ("ORD106", "Clothes", 30),
            ("ORD107", "Flowers", 25), ("ORD108", "Shoes", 90)]
    return [Order(i, item, t) for i, item, t in data]


def main():
    orders = sample_orders()
    while True:
        print("\n===== Online Order Delivery Sorter =====")
        print("1. Display orders")
        print("2. Add an order")
        print("3. Sort by delivery time (Merge Sort)")
        print("4. Exit")
        try:
            ch = int(input("Enter your choice: "))
            if ch == 1:
                display(orders, "Orders (as received):")
            elif ch == 2:
                oid = input("Order ID: ").strip().upper()
                if not oid or any(o.order_id == oid for o in orders):
                    print("Order ID must be new and not empty.")
                    continue
                item = input("Item: ").strip() or "Item"
                t = int(input("Estimated delivery time (minutes): "))
                if t <= 0:
                    print("Delivery time must be positive.")
                    continue
                orders.append(Order(oid, item, t))
                print(f"Order {oid} added.")
            elif ch == 3:
                if not orders:
                    print("No orders to sort.")
                    continue
                print("\nMerge sort steps (delivery times):")
                result, stats = merge_sort(orders)
                display(result, "Delivery priority (quickest first):")
                print(f"Comparisons = {stats['comparisons']}")
            elif ch == 4:
                print("Exiting program.")
                break
            else:
                print("Invalid choice! Try again.")
        except ValueError:
            print("Invalid input. Please enter a whole number.")


if __name__ == "__main__":
    main()
