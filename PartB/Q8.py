get_primes_desc = lambda lst: sorted((x for x in lst if all(x % i != 0 for i in range(2, int(x**0.5) + 1)) and x > 1), reverse=True)
