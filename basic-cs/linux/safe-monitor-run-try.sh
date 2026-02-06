#!/bin/bash

# --- Configuration ---
H5AD_DIR="/mnt/sdb/alex/maize-xtma/new_sugar_split_h5ad/"
H5AD_PREFIX="pcmt4-new-sugar"
TRAIT_FILE="/mnt/sdb/alex/maize-xtma/sugar-trait.txt"
LOG_DIR="/mnt/sdb/alex/maize-xtma/outs"
CHECKPOINT_FILE="/mnt/sdb/alex/maize-xtma/finished_traits.txt"
mkdir -p "$LOG_DIR"
touch "$CHECKPOINT_FILE" # Create if not exists

# --- Strict Thresholds ---
MAX_CONCURRENT=5     # Never more than 5 traits at once
MAX_MEM_PCT=75       # Pause if total RAM usage > 75%
MAX_LOAD=120.0       # Pause if Load Average > 120
STAGGER_TIME=600     # 10 mins for Python RAM to "swell"
MIN_AVAIL_GB=150     # Emergency stop if Available RAM < 150GB

check_resources() {
    read -r LOAD1 LOAD5 LOAD15 REST < /proc/loadavg
    MEM_PCT=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    MEM_AVAIL_GB=$(free -g | awk '/^Mem:/ {print $7}')

    if [ "$MEM_AVAIL_GB" -lt "$MIN_AVAIL_GB" ]; then
        echo "Safety Stop: Only ${MEM_AVAIL_GB}GB Available RAM. Waiting..."
        return 2
    elif (( $(echo "$MEM_PCT > $MAX_MEM_PCT" | bc -l) )); then
        echo "Safety Stop: System RAM usage at ${MEM_PCT}%. Waiting..."
        return 2
    fi

    if (( $(echo "$LOAD1 > $MAX_LOAD" | bc -l) )); then
        echo "Soft Wait: Load is $LOAD1. Waiting..."
        return 1
    fi
    return 0 
}

# Cleanup on script exit
trap 'echo "Stopping script..."; kill $(jobs -p) 2>/dev/null; exit' SIGINT SIGTERM

echo "Starting Resume-Aware Multi-Process Run..."
echo "Checkpoint file: $CHECKPOINT_FILE"

while IFS= read -r TRAIT || [[ -n "$TRAIT" ]]; do
    [[ -z "$TRAIT" ]] && continue

    # 1. CHECKPOINT: Check if trait is already finished
    if grep -qx "$TRAIT" "$CHECKPOINT_FILE"; then
        echo "Skipping $TRAIT (Already finished)"
        continue
    fi

    # 2. Wait if 5 traits are already running
    while [ $(jobs -rp | wc -l) -ge $MAX_CONCURRENT ]; do
        sleep 60
    done

    # 3. Check system health
    until check_resources; do
        sleep 60
    done

    echo "-------------------------------------------------------"
    echo "Launching: $TRAIT | Time: $(date)"
    
    (
        {
            echo "--- Job Start: $TRAIT ---"
            # Run 1
            python /mnt/sdb/alex/maize-xtma/batch-run-pcmt-scdrs.py \
              --h5ad ${H5AD_DIR}/${H5AD_PREFIX}.h5ad \
              --gs_dir /mnt/sdb/alex/gwas/magma-re/cor-ana-trait/ \
              --out_dir /mnt/sdb/alex/maize-xtma/scdrs_tmp_files_sugar_split/${H5AD_PREFIX}/ \
              --traits "${TRAIT}" --celltype_label celltype --datatype sc --rundate 20260205_${H5AD_PREFIX}_celltype

            # Run 2
            python /mnt/sdb/alex/maize-xtma/batch-run-pcmt-scdrs.py \
              --h5ad ${H5AD_DIR}/${H5AD_PREFIX}.h5ad \
              --gs_dir /mnt/sdb/alex/gwas/magma-re/cor-ana-trait/ \
              --out_dir /mnt/sdb/alex/maize-xtma/scdrs_tmp_files_sugar_split/${H5AD_PREFIX}/ \
              --traits "${TRAIT}" --celltype_label celltype_old --datatype sc --rundate 20260205_${H5AD_PREFIX}_celltype_old
            
            # 4. SUCCESS RECORDING: Add trait to checkpoint file only after both commands finish
            echo "$TRAIT" >> "$CHECKPOINT_FILE"
            echo "--- Job Finished and Recorded: $TRAIT ---"
        } >> "${LOG_DIR}/${TRAIT}.log" 2>&1
    ) &

    # 5. Stabilize
    echo "Waiting $((STAGGER_TIME/60)) minutes for RAM stabilization..."
    sleep $STAGGER_TIME

done < "$TRAIT_FILE"

wait
echo "All tasks finished."


