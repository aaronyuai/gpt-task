from __future__ import annotations

import os
from typing import Any, Dict

import torch
from gpt_task.config import Config, get_config


def load_model_kwargs(config: Config | None = None) -> Dict[str, Any]:
    """
    generate model kwargs from config.
    config may contains:
        - cache_dir
        - proxies
    """
    if config is None:
        config = get_config()

    res = {}
    if config.hf_cache_dir is not None:
        res["cache_dir"] = config.hf_cache_dir
    if config.proxy is not None and config.proxy.host != "":
        if "://" in config.proxy.host:
            scheme, host = config.proxy.host.split("://", 2)
        else:
            scheme, host = "", config.proxy.host

        proxy_str = f"{scheme}://{config.proxy.username}:{config.proxy.password}@{host}:{config.proxy.port}"
        res["proxies"] = {"http": proxy_str, "https": proxy_str}

    return res


def use_deterministic_mode():
    r"""
    use deterministic mode
    """
    os.environ['CUDA_LAUNCH_BLOCKING'] = '1'
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':16:8'
    torch.use_deterministic_algorithms(True)

    if torch.cuda.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
