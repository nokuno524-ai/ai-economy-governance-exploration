"""
Compute Cost Estimator

Provides functions to estimate AI model training costs,
project inference costs over time, and compare total cost of ownership (TCO)
across different deployment strategies.
"""

def estimate_training_cost(params_billions: float, tokens_trillions: float,
                           hardware_flops: float = 3.12e14,
                           gpu_cost_per_hour: float = 3.0,
                           power_kw_per_gpu: float = 0.4,
                           tpu_v4_pod_flops: float = 275e15,
                           mfu: float = 0.4) -> dict:
    """
    Estimate the training cost, time, energy, and TPU usage for an AI model.

    Args:
        params_billions (float): Number of model parameters in billions.
        tokens_trillions (float): Number of training tokens in trillions.
        hardware_flops (float): Peak hardware FLOPs per GPU (default: 312 TFLOPs for A100).
        gpu_cost_per_hour (float): Cost per GPU hour in USD.
        power_kw_per_gpu (float): Power consumption in kilowatts per GPU (default: 0.4 kW or 400W).
        tpu_v4_pod_flops (float): Peak FLOPs of a TPU v4 pod (default: 275 PFLOPs).
        mfu (float): Model FLOPs Utilization (fraction of peak FLOPs achieved, typically 0.3-0.5).

    Returns:
        dict: A dictionary containing estimated compute (FLOPs), training time (hours),
              energy consumption (kWh), TPU pod years, and total cost (USD).
    """
    params = params_billions * 1e9
    tokens = tokens_trillions * 1e12

    # Standard formula for transformer training compute: ~6 * params * tokens
    total_flops = 6 * params * tokens

    # Effective FLOPs per second (GPU)
    effective_flops_per_sec = hardware_flops * mfu

    # Total time in seconds and hours
    time_seconds = total_flops / effective_flops_per_sec
    time_hours = time_seconds / 3600

    # Cost
    cost = time_hours * gpu_cost_per_hour

    # Energy consumption (assuming 1 GPU running for time_hours)
    energy_kwh = time_hours * power_kw_per_gpu

    # TPU Pod years
    effective_tpu_flops_per_sec = tpu_v4_pod_flops * mfu
    tpu_time_seconds = total_flops / effective_tpu_flops_per_sec
    tpu_pod_years = tpu_time_seconds / (3600 * 24 * 365)

    return {
        "total_flops": total_flops,
        "gpu_hours": time_hours,
        "energy_consumption_kwh": energy_kwh,
        "tpu_pod_years": tpu_pod_years,
        "total_cost_usd": cost
    }

def project_inference_cost(initial_cost_per_m_tokens: float, years: int) -> dict:
    """
    Project future inference costs based on the historical "LLMflation" trend
    (inference cost dropping 10x per year for equivalent performance).

    Args:
        initial_cost_per_m_tokens (float): Current cost per million tokens.
        years (int): Number of years to project.

    Returns:
        dict: A dictionary mapping year offset to projected cost per million tokens.
    """
    projections = {}
    current_cost = initial_cost_per_m_tokens
    for year in range(years + 1):
        projections[year] = current_cost
        current_cost /= 10.0
    return projections

def compare_tco(monthly_tokens_millions: float,
                cloud_api_cost_per_m: float,
                self_hosted_hardware_monthly: float,
                self_hosted_ops_monthly: float,
                hybrid_api_percent: float = 0.2) -> dict:
    """
    Compare Total Cost of Ownership (TCO) across different deployment strategies.

    Args:
        monthly_tokens_millions (float): Expected monthly usage in millions of tokens.
        cloud_api_cost_per_m (float): Cloud API cost per million tokens.
        self_hosted_hardware_monthly (float): Monthly cost for self-hosted hardware (e.g., GPU instances).
        self_hosted_ops_monthly (float): Monthly operational cost for self-hosting (personnel, maintenance).
        hybrid_api_percent (float): Fraction of tokens handled by the cloud API in a hybrid setup (0.0 to 1.0).

    Returns:
        dict: TCO comparison for Cloud API, Self-Hosted, and Hybrid strategies.
    """
    cloud_cost = monthly_tokens_millions * cloud_api_cost_per_m

    self_hosted_cost = self_hosted_hardware_monthly + self_hosted_ops_monthly

    hybrid_api_tokens = monthly_tokens_millions * hybrid_api_percent
    hybrid_self_tokens = monthly_tokens_millions * (1 - hybrid_api_percent)
    hybrid_cost = (hybrid_api_tokens * cloud_api_cost_per_m) + self_hosted_hardware_monthly + self_hosted_ops_monthly

    return {
        "Cloud API": cloud_cost,
        "Self-Hosted": self_hosted_cost,
        "Hybrid": hybrid_cost
    }
