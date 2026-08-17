# Estimator Methodology

This document outlines the methodology used in the `estimator` package.

**Important Note:** All cost figures included in the codebase (e.g., in `estimator/compute_cost.py`) are illustrative estimates meant for prototyping and testing. They are not guaranteed to be exact or up-to-date real-world prices.

## Cost Sources

To update these figures with accurate real-world pricing, you should consult the following authoritative sources:

- **GPU Training Costs:**
  - AWS EC2 Pricing: https://aws.amazon.com/ec2/pricing/
  - Google Cloud Platform Compute Engine Pricing: https://cloud.google.com/compute/pricing
  - Microsoft Azure Virtual Machine Pricing: https://azure.microsoft.com/en-us/pricing/details/virtual-machines/
  - Lambda Labs (for bare-metal/A100 instances): https://lambdalabs.com/service/gpu-cloud

- **Inference Costs (LLMs):**
  - OpenAI API Pricing: https://openai.com/pricing
  - Anthropic API Pricing: https://www.anthropic.com/pricing
  - Hugging Face Endpoints: https://huggingface.co/docs/inference-endpoints/pricing
