import gc
import yaml
import torch


def conn_to_(cnf: str):
    """
        Selection of parameters for connection
    """
    if isinstance(cnf, str) and cnf == 'model':
        with open('./config/model_config.yaml', 'r') as file:
            info=yaml.safe_load(file)    
        return info['model']
    
    if isinstance(cnf, str) and cnf == 'svc':
        with open('./config/svc_config.yaml', 'r') as file:
            info=yaml.safe_load(file)    
        return info['svc']        

def cleanup():
    torch.cuda.empty_cache()
    gc.collect()