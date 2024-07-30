def get_gpu_metrics():
    # Run the nvidia-smi command and capture the output
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=memory.total,memory.used,power.draw', '--format=csv,noheader,nounits'], 
        capture_output=True, text=True
    )
    
    # Process the output
    metrics_list = result.stdout.strip().split('\n')
    gpu_data = []
    total_memory_used = 0
    total_power_draw = 0

    for index, metrics in enumerate(metrics_list):
        memory_total, memory_used, power_draw = metrics.split(', ')
        memory_used = float(memory_used.strip())
        power_draw = float(power_draw.strip())
        
        gpu_data.append({
            'gpu_index': index,
            'memory_used': f'{memory_used} MiB',
            'power_draw': f'{power_draw} W', 
        })
        
        total_memory_used += memory_used
        total_power_draw += power_draw

    gpu_data.append({
        'memory_total': f'{memory_total.strip()} MiB',
        'total_memory_used': f'{total_memory_used} MiB',
        'total_power_draw': f'{total_power_draw}'
    })
    
    return gpu_data