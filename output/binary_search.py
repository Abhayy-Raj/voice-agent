class BinarySearch:
    def __init__(self, array):
        """
        Initialize the BinarySearch class with a sorted array.

        Args:
            array (list): A sorted list of elements.
        """
        self.array = array

    def search(self, target):
        """
        Search for a target element in the sorted array using binary search.

        Args:
            target: The element to be searched.

        Returns:
            int: The index of the target element if found, -1 otherwise.
        """
        # Initialize the low and high pointers
        low = 0
        high = len(self.array) - 1

        # Continue the search until the low pointer is less than or equal to the high pointer
        while low <= high:
            # Calculate the mid index
            mid = (low + high) // 2  # Using integer division to avoid float results

            # If the target element is found at the mid index, return the index
            if self.array[mid] == target:
                return mid
            # If the target element is less than the mid element, update the high pointer
            elif self.array[mid] > target:
                high = mid - 1  # Update the high pointer to mid - 1
            # If the target element is greater than the mid element, update the low pointer
            else:
                low = mid + 1  # Update the low pointer to mid + 1

        # If the target element is not found, return -1
        return -1


def save_file(filename, array):
    """
    Save the array to a file.

    Args:
        filename (str): The name of the file to be saved.
        array (list): The array to be saved.
    """
    # Open the file in write mode
    with open(filename, 'w') as file:
        # Write each element of the array to the file
        for element in array:
            file.write(str(element) + '\n')


def main():
    # Create a sample array
    array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]

    # Create a BinarySearch object
    binary_search = BinarySearch(array)

    # Search for a target element
    target = 23
    index = binary_search.search(target)

    # Print the result
    if index != -1:
        print(f"Target {target} found at index {index}")
    else:
        print(f"Target {target} not found")

    # Save the array to a file
    filename = "binary_search_array.txt"
    save_file(filename, array)
    print(f"Array saved to {filename}")


if __name__ == "__main__":
    main()