# Python Interfaces to emulated "minigames" 

This folder contains a set of Open-AI-gym Python Environments for interfacing with emulated minigames and for generating correlated simulations.
The Python environments expose MDP/POMDP interfaces to emulated infrastructures that can be used to optimize policies for autonomous controllers. 

Generally the control problems implemented in the infrastructures that the python environments interface to are a subset of all of the control problems
related to self-learning systems and control of a computer infrastructure. Hence they are referred to as "minigames".
Thet set of minigames that are planned to be implemented are listed below. Note that some minigames are overlapping;
for example the CTF minigame subsumes many other minigames.

- **DoS** ([dos](./dos)): 
     - *BotNet* ([botnet](./dos/botnet)): TODO
- **Malware** ([malware](./malware)): 
     - *Self replicating malware* ([self_replicating_malware](./malware/self_replicating_malware)): TODO
- **Network intrusion** ([network_intrusion](./network_intrusion)):
     - *Man-in-the-Middle* ([mitm](./network_intrusion/mitm)): TODO
     - *Network protocol attack* ([network_protocol_attack](./network_intrusion/network_protocol_attack)): TODO
     - *Network sniffing* ([network_sniffing](./network_intrusion/network_sniffing)): TODO
     - *Capture the flag* ([ctf](./network_intrusion/ctf)): A general interface to the CTF minigame is implemented which supports: System identification, policy optimization (PPO, Reinforce, DQN, DDPG, Q-Learning, A2C), generalization, parallel training, domain randomization.
     - *Spoofing* ([spoofing](./network_intrusion/spoofing)): TODO                    
- **Server exploit** ([server_exploit](./server_exploit)): TODO
     - *Advanced persistent threats* ([apt](./server_exploit/apt)): TODO
     - *Binary exploit* ([binary_exploit](./server_exploit/binary_exploit)): TODO          
- **Web Hacking** ([web_hacking](./web_hacking)): TODO     
     - *SQL Injection* ([sql_injection](./web_hacking/sql_injection)): TODO
 
## Author & Maintainer

Kim Hammar <kimham@kth.se>

## Copyright and license

[LICENSE](LICENSE.md)

Creative Commons

(C) 2021, Kim Hammar