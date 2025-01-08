# HSVI c++

This directory contains example scripts for solving OS-POSGs using [hsvi](https://www.sciencedirect.com/science/article/pii/S0004370222001783).

Command for running hsvi with game file "apt_game.posg", 0.01 epsilon (target precision), 
4 pDelta (presolve delta which determined the lenght of the presolve phase), and 2000 pLimit (presolve time-limit)
```bash
./StochasticGamesCpp games/apt_game.posg 0.01 4 2000
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar