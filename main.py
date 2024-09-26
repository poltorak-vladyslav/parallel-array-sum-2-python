import concurrent.futures
import os
import threading

def main():
    array = [1, 2, 3, 4, 5, 6]  # Початковий масив
    processors = os.cpu_count() # Кількість доступних процесорів

    while len(array) > 1:
        length = len(array) // 2
        current_array = array[:]
        latch = threading.Semaphore(0)

        def process_pair(index):
            array[index] = current_array[index] + current_array[len(current_array) - 1 - index]
            latch.release()

        with concurrent.futures.ThreadPoolExecutor(max_workers=processors) as executor:
            for i in range(length):
                executor.submit(process_pair, i)

            # Очікування завершення всіх потоків в ітерації
            for _ in range(length):
                latch.acquire()

        # Оновлення масиву для наступної ітерації
        new_array = [array[i] for i in range(length)]

        if len(array) % 2 == 1:
            new_array.append(array[length])

        array = new_array

    print(f"Sum of array elements: {array[0]}")


if __name__ == "__main__":
    main()
