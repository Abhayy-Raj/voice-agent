def binary_search(arr, target):
    """
    Performs a binary search on a sorted array to find the index of a target value.

    Args:
        arr (list): A sorted list of elements.
        target: The value to be searched in the array.

    Returns:
        int: The index of the target value if found, -1 otherwise.
    """
    # Initialize the low and high pointers for the search
    low = 0
    high = len(arr) - 1

    # Continue the search until the low pointer is less than or equal to the high pointer
    while low <= high:
        # Calculate the mid index
        mid = (low + high) // 2  # Using integer division to avoid float results

        # If the target is found at the mid index, return the index
        if arr[mid] == target:
            return mid
        # If the target is less than the mid element, update the high pointer
        elif arr[mid] > target:
            high = mid - 1  # Move the high pointer to the left half
        # If the target is greater than the mid element, update the low pointer
        else:
            low = mid + 1  # Move the low pointer to the right half

    # If the target is not found, return -1
    return -1


def main():
    # Example usage of the binary search function
    arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    result = binary_search(arr, target)

    if result != -1:
        print(f"Target {target} found at index {result}")
    else:
        print(f"Target {target} not found in the array")


if __name__ == "__main__":
    main()