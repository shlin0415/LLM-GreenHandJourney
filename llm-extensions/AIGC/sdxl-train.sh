#!/bin/bash
# --- 1. SETTINGS ---
MODEL="/source_path/setups/scgsty/model/base/scgsty-base.safetensors"
VAE="/source_path/setups/scgsty/model/vae/liquid111vae_sdxl9745VAE.safetensors"
# DATA="/source_path/setups/scgsty/data/rmp104-ba"
DATA="/source_path/setups/scgsty/data/TRAIN_ME"
TRIGGER="ScgStyClean"
SAFE_TEMP=80 # Kill training if GPU hits 80C
OUTPUT_DIR="/source_path/setups/scgsty/output"

# --- PRE-FLIGHT CHECKS ---
echo "Verifying environment and paths..."

# Check if model and VAE exist
[ ! -f "$MODEL" ] && echo "ERROR: Base model not found at $MODEL" && exit 1
[ ! -f "$VAE" ] && echo "ERROR: VAE not found at $VAE" && exit 1

# Check for crucial libraries
uv run python3 -c "import torch; import accelerate; import xformers; print('Core Libraries: OK')" || exit 1

# Handle WandB (Setting to offline by default to prevent hanging)
export WANDB_MODE=offline 
# export WANDB_API_KEY=your_key_here # Uncomment if you want it online

# --- 2. GPU SAFETY DAEMON ---
python3 -c "
import subprocess, time, os, signal
def get_temp():
    out = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'])
    return int(out.decode().strip())
while True:
    t = get_temp()
    if t > $SAFE_TEMP:
        print(f'\n[DANGER] GPU TEMP {t}C! SHUTTING DOWN.'); os.kill(os.getppid(), signal.SIGTERM)
        subprocess.run(['pkill', '-f', 'sdxl_train_network.py']); exit(1)
    time.sleep(5)
" & 
DAEMON_PID=$!

# --- 3. AUTO-TAGGING & TRIGGER ---
echo "Tagging & Prepending $TRIGGER..."
# uv run finetune/tag_images_by_wd14_tagger.py --batch_size 8 --remove_underscore --caption_extension ".txt" "$DATA"
# uv run /source_path/setups/scgsty/sd-scripts/finetune/tag_images_by_wd14_tagger.py \
#   --onnx \
#   --repo_id "SmilingWolf/wd-swinv2-tagger-v3" \
#   --model_dir "/source_path/setups/scgsty/model/tagger" \
#   --batch_size 8 \
#   --remove_underscore \
#   --caption_extension ".txt" \
#   "$DATA"
# python3 -c "import os; [open(f, 'w').write('$TRIGGER, ' + open(f).read()) for f in [os.path.join('$DATA', x) for x in os.listdir('$DATA')] if f.endswith('.txt')]"

# --- 3. TRIGGER WORD INJECTION (Smart Version) ---
echo "Checking Trigger Words..."
python3 -c "
import os
for x in os.listdir('$DATA'):
    if x.endswith('.txt'):
        p = os.path.join('$DATA', x)
        with open(p, 'r+') as f:
            content = f.read()
            if not content.startswith('$TRIGGER'):
                f.seek(0, 0)
                f.write('$TRIGGER, ' + content)
                print(f'Added trigger to {x}')
"

# --- 4. START TRAINING ---
# Note: Added --vae flag and ensured paths are absolute

mkdir -p "$OUTPUT_DIR"

uv run accelerate launch /source_path/setups/scgsty/sd-scripts/sdxl_train_network.py \
  --pretrained_model_name_or_path="$MODEL" \
  --vae="$VAE" \
  --train_data_dir="$DATA" \
  --output_dir="$OUTPUT_DIR" \
  --output_name="ScgStyClean_v1" \
  --log_with="wandb" \
  --resolution="1024,1024" \
  --train_batch_size=2 \
  --max_train_steps=2500 \
  --save_every_n_steps=500 \
  --network_module=networks.lora \
  --network_dim=32 \
  --network_alpha=16 \
  --learning_rate=1e-4 \
  --mixed_precision="bf16" \
  --save_precision="bf16" \
  --cache_latents \
  --cache_latents_to_disk \
  --gradient_checkpointing \
  --optimizer_type="Adafactor" \
  --optimizer_args "scale_parameter=False" "relative_step=False" "warmup_init=False" \
  --network_train_unet_only \
  --keep_tokens=1 \
  --sample_prompts="sample_prompts.txt" \
  --sample_every_n_steps=500 \
  --xformers

# uv run accelerate launch /source_path/setups/scgsty/sd-scripts/sdxl_train_network.py \
#   --pretrained_model_name_or_path="$MODEL" \
#   --vae="$VAE" \
#   --train_data_dir="$DATA" \
#   --output_dir="$OUTPUT_DIR" \
#   --output_name="ScgStyClean_v1" \
#   --log_with="wandb" \
#   --resolution="1024,1024" \
#   --train_batch_size=4 \
#   --max_train_steps=2500 \
#   --save_every_n_steps=500 \
#   --network_module=networks.lora \
#   --network_dim=32 \
#   --network_alpha=16 \
#   --learning_rate=1e-4 \
#   --mixed_precision="bf16" \
#   --save_precision="bf16" \
#   --cache_latents \
#   --keep_tokens=1 \
#   --sample_prompts="sample_prompts.txt" \
#   --sample_every_n_steps=500 \
#   --xformers

# # --- 4. START TRAINING ---
# uv run accelerate launch /source_path/setups/scgsty/sd-scripts/sdxl_train_network.py \
#   --pretrained_model_name_or_path="$MODEL" \
#   --train_data_dir="$DATA" \
#   --output_dir="/source_path/setups/scgsty/output" \
#   --output_name="ScgStyClean_v1" \
#   --log_with="wandb" \
#   --report_to="wandb" \
#   --resolution="1024,1024" \
#   --train_batch_size=4 \
#   --max_train_steps=2500 \
#   --checkpointing_steps=500 \
#   --network_module=networks.lora \
#   --network_dim=32 \
#   --network_alpha=16 \
#   --learning_rate=1e-4 \
#   --mixed_precision="bf16" \
#   --save_precision="bf16" \
#   --cache_latents \
#   --keep_tokens=1 \
#   --sample_prompts="sample_prompts.txt" \
#   --sample_every_n_steps=500 \
#   --xformers

kill $DAEMON_PID

