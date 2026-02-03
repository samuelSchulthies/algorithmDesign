import matplotlib.pyplot as plt

import time

data = {
    10: .0003,
    100: .0027,
    1000: .0253,
    10000: .2620,
    20000: .5098,
    40000: 1.0578,
    50000: 1.3178
}

k = [y / n for n, y in data.items()]
linear_k = sum(k)/len(k)

kk = [y / n**2 for n, y in data.items()]
quad_k = sum(kk)/len(kk)
# print(sum(kk)/len(kk))

kkk = [y / n**3 for n, y in data.items()]
cubic_k = sum(kkk)/len(kkk)
# print(sum(kkk)/len(kkk))



kkkk = [y / n**4 for n, y in data.items()]
quartic_k = sum(kkkk)/len(kkkk)
# print(sum(kkkk)/len(kkkk))
# plt.bar(range(len(k)), k)
# print(sum(k)/len(k))

# plt.scatter(
#     data.keys(),
#     data.values(),
#     marker='o'
# );

plt.plot(
    data.keys(),
    data.values(),
    marker='o'
);

plt.plot(
    data.keys(),
    [n * linear_k for n in data],
    c='red',
    ls=':',
    lw=2,
    alpha=0.5
)

# plt.plot(
#     data.keys(),
#     [n ** 2 * quad_k for n in data],
#     c='red',
#     ls=':',
#     lw=2,
#     alpha=0.5
# )

# plt.plot(
#     data.keys(),
#     [n ** 3 * cubic_k for n in data],
#     c='blue',
#     ls=':',
#     lw=2,
#     alpha=0.5
# )

# plt.plot(
#     data.keys(),
#     [n ** 4 * quad_k for n in data],
#     c='purple',
#     ls=':',
#     lw=2,
#     alpha=0.5
# )

plt.xlabel("Size of Input N (points)", fontsize=18)
plt.ylabel("Time (ms)", fontsize=18)
plt.legend(['Observed', 'O(n)']);
plt.show()