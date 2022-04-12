from stable_baselines3 import PPO
import zipfile
from stable_baselines3.common.save_util import load_from_zip_file, recursive_getattr, recursive_setattr, save_to_zip_file, data_to_json

if __name__ == '__main__':
    path = "/var/log/csle/ppo_model0.zip"
    model = PPO.load(path = path)
    print(model.get_env())
    print(model.gamma)
    print(model.policy_kwargs)
    print(model.policy.features_extractor)
    print(model.gae_lambda)
    print(model.learning_rate)
    print(model.policy_class.__name__)
    print(model.n_steps)

    # Copy parameter list so we don't mutate the original dict
    data = model.__dict__.copy()

    # Exclude is union of specified parameters (if any) and standard exclusions
    exclude = set([]).union(model._excluded_save_params())

    state_dicts_names, torch_variable_names = model._get_torch_save_params()
    all_pytorch_variables = state_dicts_names + torch_variable_names
    for torch_var in all_pytorch_variables:
        # We need to get only the name of the top most module as we'll remove that
        var_name = torch_var.split(".")[0]
        # Any params that are in the save vars must not be saved by data
        exclude.add(var_name)

    # Remove parameter entries of parameters which are to be excluded
    for param_name in exclude:
        data.pop(param_name, None)

    # Build dict of torch variables
    pytorch_variables = None
    if torch_variable_names is not None:
        pytorch_variables = {}
        for name in torch_variable_names:
            attr = recursive_getattr(model, name)
            pytorch_variables[name] = attr

    # Build dict of state_dicts
    params_to_save = model.get_parameters()

    serialized_data = data_to_json(data)
