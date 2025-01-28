from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    exp = MetastoreFacade.get_experiment_execution(id=5)
    returns = exp.result.avg_metrics["running_average_return"]
    returns_stds = exp.result.std_metrics["running_average_return"]
    compute = exp.result.avg_metrics["runtime"]
    print(returns)
    for i in range(len(returns)):
        print(f"{compute[i]} {-returns[i]} {-returns[i] + returns_stds[i]} {-returns[i] - returns_stds[i]}")
