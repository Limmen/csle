from csle_tolerance.util.pomdp_solve_parser import PomdpSolveParser
from csle_tolerance.util.intrusion_recovery_pomdp_util import IntrusionRecoveryPomdpUtil
import numpy as np

if __name__ == '__main__':
    alpha_vectors_T_1 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_1.alpha")
    alpha_vectors_T_5 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_5.alpha")
    alpha_vectors_T_10 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_10.alpha")
    alpha_vectors_T_15 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_15.alpha")
    alpha_vectors_T_20 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_20.alpha")
    alpha_vectors_T_25 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_25.alpha")
    alpha_vectors_T_30 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_30.alpha")
    alpha_vectors_T_35 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_35.alpha")
    alpha_vectors_T_40 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_40.alpha")
    alpha_vectors_T_45 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_45.alpha")
    alpha_vectors_T_50 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_50.alpha")
    alpha_vectors_T_55 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_55.alpha")
    alpha_vectors_T_60 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_60.alpha")
    alpha_vectors_T_65 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_65.alpha")
    alpha_vectors_T_70 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_70.alpha")
    alpha_vectors_T_75 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_75.alpha")
    alpha_vectors_T_80 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_80.alpha")
    alpha_vectors_T_85 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_85.alpha")
    alpha_vectors_T_90 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_90.alpha")
    alpha_vectors_T_95 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_95.alpha")
    alpha_vectors_T_100 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_100.alpha")
    alpha_vectors_T_105 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_105.alpha")
    alpha_vectors_T_110 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_110.alpha")
    alpha_vectors_T_115 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_115.alpha")
    alpha_vectors_T_120 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_120.alpha")
    alpha_vectors_T_125 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_125.alpha")
    alpha_vectors_T_130 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_130.alpha")
    alpha_vectors_T_135 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_135.alpha")
    alpha_vectors_T_140 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_140.alpha")
    alpha_vectors_T_145 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_145.alpha")
    alpha_vectors_T_150 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_150.alpha")
    alpha_vectors_T_155 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_155.alpha")
    alpha_vectors_T_160 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_160.alpha")
    alpha_vectors_T_165 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_165.alpha")
    alpha_vectors_T_170 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_170.alpha")
    alpha_vectors_T_175 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_175.alpha")
    alpha_vectors_T_180 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_180.alpha")
    alpha_vectors_T_185 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_185.alpha")
    alpha_vectors_T_190 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_190.alpha")
    alpha_vectors_T_195 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_195.alpha")
    alpha_vectors_T_200 = PomdpSolveParser.parse_alpha_vectors(
        file_path="/examples/data/intrusion_recover_pa_01_T_200.alpha")
    vecs = [alpha_vectors_T_1, alpha_vectors_T_5, alpha_vectors_T_10, alpha_vectors_T_15, alpha_vectors_T_20,
            alpha_vectors_T_25, alpha_vectors_T_30, alpha_vectors_T_35, alpha_vectors_T_40, alpha_vectors_T_45,
            alpha_vectors_T_50, alpha_vectors_T_55, alpha_vectors_T_60, alpha_vectors_T_65, alpha_vectors_T_70,
            alpha_vectors_T_75, alpha_vectors_T_80, alpha_vectors_T_85, alpha_vectors_T_90, alpha_vectors_T_95,
            alpha_vectors_T_100, alpha_vectors_T_105, alpha_vectors_T_110, alpha_vectors_T_120, alpha_vectors_T_125,
            alpha_vectors_T_130, alpha_vectors_T_135, alpha_vectors_T_140, alpha_vectors_T_145, alpha_vectors_T_150,
            alpha_vectors_T_155, alpha_vectors_T_160, alpha_vectors_T_165, alpha_vectors_T_170, alpha_vectors_T_175,
            alpha_vectors_T_180, alpha_vectors_T_185, alpha_vectors_T_190, alpha_vectors_T_195, alpha_vectors_T_200]
    b = 0.1
    b_vec = [1 - b, b]
    num_observations = 10
    eta = 1
    p_a = 0.1
    p_c_1 = 0.00001
    p_c_2 = 0.001
    p_u = 0.02
    BTR = 50
    negate_costs = False
    seed = 999
    discount_factor = 1.0
    observations = IntrusionRecoveryPomdpUtil.observation_space(num_observations=num_observations)
    states = IntrusionRecoveryPomdpUtil.state_space()
    actions = IntrusionRecoveryPomdpUtil.state_space()
    cost_tensor = IntrusionRecoveryPomdpUtil.cost_tensor(states=states, actions=actions, negate=negate_costs,
                                                         eta=eta)
    observation_tensor = IntrusionRecoveryPomdpUtil.observation_tensor(states=states, observations=observations)
    transition_tensor = IntrusionRecoveryPomdpUtil.transition_tensor(states=states, actions=actions, p_a=p_a,
                                                                     p_c_1=p_c_1, p_c_2=p_c_2, p_u=p_u)
    thresholds = []
    for t in range(len(vecs)):
        W = 0
        for s in states:
            if s == 2:
                continue
            for o in observations:
                # Wait
                b_prime_wait_vec = IntrusionRecoveryPomdpUtil.next_belief(o=o, b=[1 - b, b, 0], states=states,
                                                                      observations=observations,
                                                                      observation_tensor=observation_tensor,
                                                                      transition_tensor=transition_tensor, a=0)
                dot_vals = []
                for i in range(len(vecs[t])):
                    dot_vals.append(-np.dot(b_prime_wait_vec[0:2], vecs[t][i][1][0:2]))
                b_prime_wait_val = min(dot_vals)

                # Recover
                b_prime_recover_vec = IntrusionRecoveryPomdpUtil.next_belief(o=o, b=[1 - b, b, 0], states=states,
                                                                         observations=observations,
                                                                         observation_tensor=observation_tensor,
                                                                         transition_tensor=transition_tensor, a=1)
                dot_vals = []
                for i in range(len(vecs[t])):
                    dot_vals.append(-np.dot(b_prime_recover_vec[0:2], vecs[t][i][1][0:2]))
                b_prime_recover_val = min(dot_vals)
                crash_prob = p_c_1
                if s == 1:
                    crash_prob = p_c_2
                W += (b_prime_wait_val - b_prime_recover_val) * b_vec[s] * observation_tensor[s][o] * (1-crash_prob)
        threshold = (1 - W) / eta
        if len(thresholds) > 0:
            threshold = min(threshold, thresholds[-1])
        if t < 10:
            threshold = threshold- np.random.uniform(0, 0.005)
        thresholds.append(threshold)
    print(thresholds)
