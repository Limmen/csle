# pomdp-solve

This directory contains example scripts for solving pomdps using [pomdp-solve](https://www.pomdp.org/code/index.html).

Command for running pomdp-solve with infinite time horizon with a discount factor:
```bash
nohup pomdp-solve -pomdp intrusion_recovery.pomdp -discount 0.995 -method incprune > inf_gamma_099.log &
```

Command for running pomdp-solve with a fixed time horizon and no discount:
```bash
nohup pomdp-solve -pomdp intrusion_recovery.pomdp -horizon 100 -method incprune > 100_solve.log &
```

## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](../../../LICENSE.md)

Creative Commons

(C) 2020-2025, Kim Hammar