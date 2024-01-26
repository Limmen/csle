import json
import io
import time

from csle_agents.agents.pomcp.pomcp_util import POMCPUtil

if __name__ == '__main__':
    with io.open(f"/home/kim/particle_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        temp = json.loads(json_str)
    particle_model = {}
    for k, v in temp.items():
        v_2 = [int(x) for x in v]
        particle_model[int(k)] = v_2

    print("creating state to obs model")
    state_to_obs_model = {}
    for k, v in particle_model.items():
        for s in v:
            if s not in state_to_obs_model:
                state_to_obs_model[s] = []
            state_to_obs_model[s].append(k)
    print("state to obs model done")

    with io.open(f"/home/kim/transition_model.json", 'r', encoding='utf-8') as f:
        json_str = f.read()
        temp = json.loads(json_str)
    transition_model = {}
    for k, v in temp.items():
        transition_model[int(k)] = {}
        for k2, v2 in v.items():
            transition_model[int(k)][int(k2)] = {}
            for k3, v3 in v2.items():
                transition_model[int(k)][int(k2)][int(k3)] = int(v3)
    print("going through files")
    filenames = [
        "/home/kim/transition_model_ppo_2.json",
        "/home/kim/transition_model_ppo_3.json",
        "/home/kim/transition_model_ppo_4.json",
        "/home/kim/transition_model_ppo_5.json",
        "/home/kim/transition_model_ppo_6.json",
        "/home/kim/transition_model_ppo_7.json",
        "/home/kim/transition_model_ppo_8.json",
        "/home/kim/transition_model_ppo_9.json",
        "/home/kim/transition_model_ppo_10.json",
        "/home/kim/transition_model_r1.json",
        "/home/kim/transition_model_r2.json",
        "/home/kim/transition_model_r3.json",
        "/home/kim/transition_model_r4.json",
        "/home/kim/transition_model_r5.json",
        "/home/kim/transition_model_r6.json",
        "/home/kim/transition_model_r7.json",
        "/home/kim/transition_model_r8.json",
        "/home/kim/transition_model_r9.json",
        "/home/kim/transition_model_r10.json",
        "/home/kim/transition_model_r11.json",
        "/home/kim/transition_model_r12.json",
        "/home/kim/transition_model_r13.json",
        "/home/kim/transition_model_r14.json",
        "/home/kim/transition_model_r15.json",
        "/home/kim/transition_model_r16.json",
        "/home/kim/transition_model_r17.json",
        "/home/kim/transition_model_r18.json",
        "/home/kim/transition_model_r19.json",
        "/home/kim/transition_model_r20.json",
        "/home/kim/transition_model_r21.json",
        "/home/kim/transition_model_r22.json",
        "/home/kim/transition_model_r23.json",
        "/home/kim/transition_model_r24.json",
        "/home/kim/transition_model_r25.json",
        "/home/kim/transition_model_r26.json",
        "/home/kim/transition_model_r27.json",
        "/home/kim/transition_model_r28.json",
        "/home/kim/transition_model_r29.json",
        "/home/kim/transition_model_r30.json",
        "/home/kim/transition_model_r31.json",
        "/home/kim/transition_model_r32.json",
        "/home/kim/transition_model_r33.json",
        "/home/kim/transition_model_r34.json",
        "/home/kim/transition_model_r35.json",
        "/home/kim/transition_model_r36.json",
        "/home/kim/transition_model_r37.json",
        "/home/kim/transition_model_r38.json",
        "/home/kim/transition_model_r39.json",
        "/home/kim/transition_model_r40.json",
        "/home/kim/transition_model_r41.json",
        "/home/kim/transition_model_r42.json",
        "/home/kim/transition_model_r43.json",
        "/home/kim/transition_model_r44.json",
        "/home/kim/transition_model_r45.json",
        "/home/kim/transition_model_r46.json",
        "/home/kim/transition_model_r47.json",
        "/home/kim/transition_model_r48.json",
        "/home/kim/transition_model_r49.json",
        "/home/kim/transition_model_r50.json",
        "/home/kim/transition_model_r51.json",
        "/home/kim/transition_model_r52.json",
        "/home/kim/transition_model_r53.json",
        "/home/kim/transition_model_r54.json",
        "/home/kim/transition_model_r55.json",
        "/home/kim/transition_model_r56.json",
        "/home/kim/transition_model_r57.json",
        "/home/kim/transition_model_r58.json",
        "/home/kim/transition_model_r59.json",
        "/home/kim/transition_model_r60.json",
        "/home/kim/transition_model_r61.json",
        "/home/kim/transition_model_r62.json",
        "/home/kim/transition_model_r63.json",
        "/home/kim/transition_model_r64.json",
        "/home/kim/transition_model_r65.json",
        "/home/kim/transition_model_r66.json",
        "/home/kim/transition_model_r67.json",
        "/home/kim/transition_model_r68.json",
        "/home/kim/transition_model_r69.json",
        "/home/kim/transition_model_r70.json",
        "/home/kim/transition_model_r71.json",
        "/home/kim/transition_model_r72.json",
        "/home/kim/transition_model_r73.json",
        "/home/kim/transition_model_r74.json",
        "/home/kim/transition_model_r75.json",
        "/home/kim/transition_model_r76.json",
        "/home/kim/transition_model_r77.json",
        "/home/kim/transition_model_r78.json",
        "/home/kim/transition_model_r79.json",
        "/home/kim/transition_model_r80.json"
    ]
    for i, filename in enumerate(filenames):
        print(f"file {i}/{len(filenames)}")
        try:
            with io.open(filename, 'r', encoding='utf-8') as f:
                json_str = f.read()
                temp = json.loads(json_str)
        except:
            print(f"fail, file: {filename}")
            time.sleep(20)
            try:
                with io.open(filename, 'r', encoding='utf-8') as f:
                    json_str = f.read()
                    temp = json.loads(json_str)
            except:
                time.sleep(20)
                with io.open(filename, 'r', encoding='utf-8') as f:
                    json_str = f.read()
                    temp = json.loads(json_str)
        for k, v in temp.items():
            if int(k) not in transition_model:
                transition_model[int(k)] = {}
            for k2, v2 in v.items():
                if int(k2) not in transition_model[int(k)]:
                    transition_model[int(k)][int(k2)] = {}
                for k3, v3 in v2.items():
                    if int(k3) not in transition_model[int(k)][int(k2)]:
                        transition_model[int(k)][int(k2)][int(k3)] = int(v3)
                    else:
                        transition_model[int(k)][int(k2)][int(k3)] = transition_model[int(k)][int(k2)][int(k3)] + int(v3)


    print("creating new transition model")
    transition_model_1 = {}
    for k, v in transition_model.items():
        if k not in transition_model_1:
            transition_model_1[k] = {}
        for k2, v2 in v.items():
            # if k2 not in transition_model_1:
            #     # transition_model_1[k2] = {}
            for k3, v3 in v2.items():
                if k3 not in transition_model_1[k]:
                    transition_model_1[k][k3] = []
                if len(list(v3.keys())) == 1:
                    transition_model_1[k][k3] = [k2]*(100)
                else:
                    transition_model_1[k][k3] = transition_model_1[k][k3] + [k2]*(int(v3)+1)

    print(f"sampled state_from_obs: {POMCPUtil.rand_choice(particle_model[list(particle_model.keys())[0]])}")

    print(f"sampled obs from state: {POMCPUtil.rand_choice(state_to_obs_model[list(state_to_obs_model.keys())[0]])}")
    print(f"sampled obs from state: {POMCPUtil.rand_choice(state_to_obs_model[list(state_to_obs_model.keys())[1]])}")
    print(f"sampled obs from state: {POMCPUtil.rand_choice(state_to_obs_model[list(state_to_obs_model.keys())[1912]])}")

    s = POMCPUtil.rand_choice(list(transition_model_1.keys()))
    print(s)
    a = POMCPUtil.rand_choice(list(transition_model_1[s].keys()))
    print(a)
    print(transition_model_1[s][a])
    print(f"sampled state transition: {POMCPUtil.rand_choice(transition_model_1[s][a])}")


    json_str = json.dumps(state_to_obs_model, indent=4, sort_keys=True)
    with io.open(f"/home/kim/observation_model.json", 'w', encoding='utf-8') as f:
        f.write(json_str)

    json_str = json.dumps(transition_model_1, indent=4, sort_keys=True)
    with io.open(f"/home/kim/new_transition_model.json", 'w', encoding='utf-8') as f:
        f.write(json_str)
