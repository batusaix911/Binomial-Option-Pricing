#attempt to multithread the binomial tree plotting. absolutely no speedup noticeable, but a useful concept check.
#pyplot seems thread safe. no manual locking necessary.

import numpy as np
import matplotlib
print(matplotlib.get_backend())
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
from threading import Thread
from queue import Queue

printer_queue = Queue()


def eur_option_price(sigma=0.3, T=1, t=0, steps=5, r=0.03, S=100, K=100):
    S = [[S]]
    dt = T / steps
    u = np.exp(sigma * dt ** 0.5)
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    for i in range(int(T / dt)):
        S.append([S[len(S) - 1][0] * u, *list(np.array(S[len(S) - 1]) * d)])

    puts = [list(map(max, np.zeros(len(S[len(S) - 1])), [K - x for x in S[len(S) - 1]]))]
    calls = [list(map(max, np.zeros(len(S[len(S) - 1])), [x - K for x in S[len(S) - 1]]))]

    for index in range(len(S) - 2, -1, -1):
        puts.append([p * np.exp(-r * dt) * puts[len(puts) - 1][index1] +
                     (1 - p) * np.exp(-r * dt) * puts[len(puts) - 1][index1 + 1]
                     for index1 in range(len(S[index + 1]) - 1)])
        calls.append([p * np.exp(-r * dt) * calls[len(calls) - 1][index1] +
                      (1 - p) * np.exp(-r * dt) * calls[len(calls) - 1][index1 + 1]
                      for index1 in range(len(S[index + 1]) - 1)])

    return calls[len(calls) - t - 1], puts[len(puts) - t - 1], S, puts, calls


def this_gon_be_fun(stock_price_branches, ax):
    # printer_queue.put('branch size ' + str(len(stock_price_branches)))
    for ind in range(len(stock_price_branches)-1):
        # printer_queue.put(len(stock_price_branches[ind]))
        for ind1 in range(len(stock_price_branches[ind])):
            x_coords = [len(stock_price_branches[ind])-1, len(stock_price_branches[ind])]
            try:
                y_coords1 = [stock_price_branches[ind][ind1], stock_price_branches[ind + 1][ind1]]
            except IndexError:
                printer_queue.put('Error at branch {0:d} node {1:d}'.format(len(stock_price_branches[ind]), ind1))
                continue
            y_coords2 = [stock_price_branches[ind][ind1], stock_price_branches[ind + 1][ind1 + 1]]

            ax.plot(x_coords, y_coords1)
            ax.plot(x_coords, y_coords2)


def plot_tree(stock_price_tree, ax, fig):
    processes = []
    steps = 10
    for ind in range(len(stock_price_tree)-1, 0, -steps):
        if ind-steps < 0:
            steps = ind
        printer_queue.put('{}, {}, {}, {}'.format(ind-steps, ind-1, ind-1, ind+1))
        processes.append(Thread(target=this_gon_be_fun, args=(stock_price_tree[ind-steps:ind], ax)))
        processes[-1].start()
        processes.append(Thread(target=this_gon_be_fun, args=(stock_price_tree[ind-1:ind+1], ax)))
        processes[-1].start()

    for p in processes:
        p.join()

    ax.set_xlabel('Steps')
    ax.set_ylabel('Stock Price')
    fig.suptitle('Stock Price Tree')


def printer_func():
    while True:
        new_val = printer_queue.get()
        print(new_val)


def main():
    finalised_steps = 150

    printer_proc = Thread(target=printer_func, daemon=True)
    printer_proc.start()

    put_price, call_price, stock_price_tree, put_tree, call_tree = eur_option_price(steps=finalised_steps)
    print('Put price with %i steps: %.2f' % (finalised_steps, put_price[0]))
    print('Call price with %i steps: %.2f' % (finalised_steps, call_price[0]))

    start_time = time.time()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    fig.set_size_inches(10, 10)
    plot_tree(stock_price_tree, ax, fig)
    printer_queue.put('Time taken: %.2f seconds' % (time.time() - start_time))
    # plt.show()
    plt.savefig('chart.png')


if __name__ == '__main__':
    main()