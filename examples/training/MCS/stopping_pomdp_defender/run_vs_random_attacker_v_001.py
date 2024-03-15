# def MCS(init_list, s_max, local_search_state):
# for i = 1, ... , n do
# x = best of (x^j)_{j=1}^L_i
# split current box B along i'th coord at x_i^j and point determined by golden ratio
# B = the box that has best fcn value of the boxes containing x
# while there are boxes of level s < s_max do
# for all non-empty levels s= 2:s_max - 1 do
# choose the box B at level s with the best function value
# i = nr of spklit times the coordinate used least often when producing box B
# if s > 2n(i+1) then
# split box B along i'th coordinate
# else if s > 2n(i+1) then
# determine most promising spitting coordinate i
# compute minimal exp. fcn value f_exp at new point
# if f_exp < f_best then
# split B along i'th coordinate
# else
# tag B as not promising and increase its level by 1
# for base points x, of all the new boxes at level s?max, do
# start a local search from x if improvement is expected

# output x_best, f_best


def f(x):
    return (x[0] - 1) ** 2 + (x[1] - 3) ** 2
