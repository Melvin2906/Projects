def odd_even(num):
    res = ["even", "odd"]
    print(res[num % 2])

if __name__ == "__main__":
    num = int(input())
    odd_even(num)