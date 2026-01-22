"""
System Requirements Checker for Gospel Parser.
Detects if system can handle Mixtral 7B or should use Gemini API.
"""

import os
import sys
import platform
import subprocess
from typing import Dict, Tuple, Optional

# --- SYSTEM REQUIREMENTS ---

MIXTRAL_7B_REQUIREMENTS = {
    "min_ram_gb": 8,  # Minimum RAM for running Mixtral 7B
    "recommended_ram_gb": 16,  # Recommended RAM
    "min_vram_gb": 4,  # Minimum GPU VRAM (if using GPU)
    "recommended_vram_gb": 8,  # Recommended GPU VRAM
    "min_disk_gb": 10,  # Disk space for model storage
}

# --- SYSTEM DETECTION ---

def get_ram_gb() -> float:
    """Get total system RAM in GB"""
    try:
        if platform.system() == "Linux":
            # Read from /proc/meminfo
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if 'MemTotal' in line:
                        # MemTotal:       65842464 kB
                        kb = int(line.split()[1])
                        return kb / (1024 * 1024)  # KB to GB

        elif platform.system() == "Darwin":  # macOS
            output = subprocess.check_output(['sysctl', 'hw.memsize']).decode()
            bytes_ram = int(output.split(':')[1].strip())
            return bytes_ram / (1024 ** 3)  # Bytes to GB

        elif platform.system() == "Windows":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulong = ctypes.c_ulong
            class MEMORYSTATUS(ctypes.Structure):
                _fields_ = [
                    ('dwLength', c_ulong),
                    ('dwMemoryLoad', c_ulong),
                    ('dwTotalPhys', c_ulong),
                    ('dwAvailPhys', c_ulong),
                    ('dwTotalPageFile', c_ulong),
                    ('dwAvailPageFile', c_ulong),
                    ('dwTotalVirtual', c_ulong),
                    ('dwAvailVirtual', c_ulong),
                ]
            memory_status = MEMORYSTATUS()
            memory_status.dwLength = ctypes.sizeof(MEMORYSTATUS)
            kernel32.GlobalMemoryStatus(ctypes.byref(memory_status))
            return memory_status.dwTotalPhys / (1024 ** 3)  # Bytes to GB

    except Exception as e:
        print(f"Warning: Could not detect RAM: {e}")
        return 0.0

    return 0.0


def get_gpu_info() -> Dict:
    """Get GPU information (NVIDIA only for now)"""
    gpu_info = {
        "has_gpu": False,
        "gpu_name": None,
        "vram_gb": 0.0,
        "cuda_available": False
    }

    try:
        # Try nvidia-smi
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines and lines[0]:
                parts = lines[0].split(',')
                gpu_info["has_gpu"] = True
                gpu_info["gpu_name"] = parts[0].strip()
                gpu_info["vram_gb"] = float(parts[1].strip()) / 1024  # MB to GB

                # Check CUDA availability
                try:
                    import torch
                    gpu_info["cuda_available"] = torch.cuda.is_available()
                except ImportError:
                    gpu_info["cuda_available"] = False

    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass  # No nvidia-smi or timeout

    return gpu_info


def get_disk_space_gb(path: str = ".") -> float:
    """Get available disk space in GB"""
    try:
        if platform.system() == "Windows":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path),
                None,
                None,
                ctypes.pointer(free_bytes)
            )
            return free_bytes.value / (1024 ** 3)
        else:
            stat = os.statvfs(path)
            return (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
    except Exception:
        return 0.0


# --- SYSTEM CAPABILITY ASSESSMENT ---

def check_system_requirements() -> Dict:
    """
    Check if system meets requirements for Mixtral 7B.

    Returns:
        Dict with system info and recommendations
    """
    ram_gb = get_ram_gb()
    gpu_info = get_gpu_info()
    disk_gb = get_disk_space_gb()

    result = {
        "system": {
            "os": platform.system(),
            "os_version": platform.release(),
            "ram_gb": round(ram_gb, 1),
            "has_gpu": gpu_info["has_gpu"],
            "gpu_name": gpu_info["gpu_name"],
            "vram_gb": round(gpu_info["vram_gb"], 1),
            "cuda_available": gpu_info["cuda_available"],
            "disk_space_gb": round(disk_gb, 1),
        },
        "requirements": MIXTRAL_7B_REQUIREMENTS,
        "assessment": {},
        "recommendation": ""
    }

    # Assess RAM
    if ram_gb >= MIXTRAL_7B_REQUIREMENTS["recommended_ram_gb"]:
        result["assessment"]["ram"] = "excellent"
    elif ram_gb >= MIXTRAL_7B_REQUIREMENTS["min_ram_gb"]:
        result["assessment"]["ram"] = "adequate"
    else:
        result["assessment"]["ram"] = "insufficient"

    # Assess GPU
    if gpu_info["has_gpu"]:
        if gpu_info["vram_gb"] >= MIXTRAL_7B_REQUIREMENTS["recommended_vram_gb"]:
            result["assessment"]["gpu"] = "excellent"
        elif gpu_info["vram_gb"] >= MIXTRAL_7B_REQUIREMENTS["min_vram_gb"]:
            result["assessment"]["gpu"] = "adequate"
        else:
            result["assessment"]["gpu"] = "insufficient"
    else:
        result["assessment"]["gpu"] = "none"

    # Assess disk space
    if disk_gb >= MIXTRAL_7B_REQUIREMENTS["min_disk_gb"]:
        result["assessment"]["disk"] = "sufficient"
    else:
        result["assessment"]["disk"] = "insufficient"

    # Overall recommendation
    ram_ok = result["assessment"]["ram"] in ["adequate", "excellent"]
    disk_ok = result["assessment"]["disk"] == "sufficient"

    if ram_ok and disk_ok:
        result["recommendation"] = "mixtral"
        result["reason"] = "Your system meets the requirements for running Mixtral 7B locally."
    else:
        result["recommendation"] = "gemini"
        if not ram_ok:
            result["reason"] = f"Insufficient RAM ({ram_gb:.1f} GB). Mixtral 7B requires at least {MIXTRAL_7B_REQUIREMENTS['min_ram_gb']} GB."
        elif not disk_ok:
            result["reason"] = f"Insufficient disk space ({disk_gb:.1f} GB). Mixtral 7B requires at least {MIXTRAL_7B_REQUIREMENTS['min_disk_gb']} GB."

    return result


# --- DISPLAY FUNCTIONS ---

def print_system_info(result: Dict):
    """Pretty-print system information"""
    print("=" * 60)
    print("SYSTEM INFORMATION")
    print("=" * 60)

    sys_info = result["system"]
    print(f"\nOperating System: {sys_info['os']} {sys_info['os_version']}")
    print(f"RAM:              {sys_info['ram_gb']} GB")

    if sys_info['has_gpu']:
        print(f"GPU:              {sys_info['gpu_name']}")
        print(f"VRAM:             {sys_info['vram_gb']} GB")
        print(f"CUDA Available:   {'Yes' if sys_info['cuda_available'] else 'No'}")
    else:
        print(f"GPU:              Not detected")

    print(f"Disk Space:       {sys_info['disk_space_gb']} GB available")

    print("\n" + "=" * 60)
    print("ASSESSMENT FOR MIXTRAL 7B")
    print("=" * 60)

    assessment = result["assessment"]

    # RAM
    ram_status = {
        "excellent": "✓ Excellent",
        "adequate": "✓ Adequate",
        "insufficient": "✗ Insufficient"
    }
    print(f"\nRAM:   {ram_status.get(assessment['ram'], '?')} ({sys_info['ram_gb']} GB)")

    # GPU
    if assessment['gpu'] == "none":
        print(f"GPU:   ⓘ None detected (CPU-only mode available)")
    else:
        gpu_status = {
            "excellent": "✓ Excellent",
            "adequate": "✓ Adequate",
            "insufficient": "⚠ Low VRAM"
        }
        print(f"GPU:   {gpu_status.get(assessment['gpu'], '?')} ({sys_info['vram_gb']} GB VRAM)")

    # Disk
    disk_status = "✓ Sufficient" if assessment['disk'] == "sufficient" else "✗ Insufficient"
    print(f"Disk:  {disk_status} ({sys_info['disk_space_gb']} GB free)")

    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60 + "\n")

    if result["recommendation"] == "mixtral":
        print("✓ Your system CAN run Mixtral 7B locally with Ollama")
        print(f"  {result['reason']}")
    else:
        print("⚠ Your system may struggle with Mixtral 7B locally")
        print(f"  {result['reason']}")
        print("\n  ALTERNATIVE: Use Google Gemini API (cloud-based, no local requirements)")

    print()


# --- MAIN ---

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("AI GOSPEL PARSER - SYSTEM REQUIREMENTS CHECKER")
    print("=" * 60 + "\n")

    print("Analyzing your system...\n")

    result = check_system_requirements()
    print_system_info(result)

    print("=" * 60)
    print()
