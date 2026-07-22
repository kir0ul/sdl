#!/usr/bin/env sh


# # setup vulkan
# mkdir -p "/usr/share/vulkan/icd.d"
# wget -q "https://raw.githubusercontent.com/haosulab/ManiSkill/main/docker/nvidia_icd.json"
# wget -q "https://raw.githubusercontent.com/haosulab/ManiSkill/main/docker/10_nvidia.json"
# mv "nvidia_icd.json" "/usr/share/vulkan/icd.d"
# mv "10_nvidia.json" "/usr/share/glvnd/egl_vendor.d/10_nvidia.json"
# apt install -y --no-install-recommends libvulkan-dev

# dependencies
pip install --upgrade mani_skill tyro


git clone https://github.com/mani-skill/ManiSkill.git

cp -r ManiSkill/examples/baselines/diffusion_policy/ ./diffusion_policy/

# !cd diffusion_policy && pip install -e .
pip install -e diffusion_policy/.


curl -L -O "https://github.com/kir0ul/sdl/raw/refs/heads/main/data/long-task-1.h5"
curl -L -O "https://github.com/kir0ul/sdl/raw/refs/heads/main/data/long-task-2.h5"
