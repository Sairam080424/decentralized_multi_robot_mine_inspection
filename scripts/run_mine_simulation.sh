#!/usr/bin/env bash
# ==============================================================================
# Script: run_mine_simulation.sh
# Description: Developer execution script for Milestone M1 subterranean mine simulation.
#              Configures resource paths, validates SDF files, and launches Gazebo Sim.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

WORLD_FILE="${REPO_ROOT}/simulation/worlds/mine_world.sdf"
MODELS_DIR="${REPO_ROOT}/simulation/models"
WORLDS_DIR="${REPO_ROOT}/simulation/worlds"

# Environment configuration for Gazebo Harmonic / SDFormat 14
export GZ_SIM_RESOURCE_PATH="${MODELS_DIR}:${WORLDS_DIR}:${GZ_SIM_RESOURCE_PATH:-}"
export SDF_PATH="${MODELS_DIR}:${SDF_PATH:-}"
export GZ_LOG_PATH="${GZ_LOG_PATH:-/tmp}"

MODE="headless"
ITERATIONS=""
VALIDATE_ONLY=0
USE_ROS2=0

print_usage() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

Options:
  --headless         Run Gazebo Sim in headless mode (default, no GUI)
  --gui              Run Gazebo Sim with GUI enabled
  --validate         Validate all SDF models and world file with 'gz sdf -k' then exit
  --iterations <N>   Run headless simulation for exactly N iterations, then exit
  --ros              Launch via ROS 2 launch system (launch/mine_simulation.launch.py)
  -h, --help         Display this help message and exit

Examples:
  ./scripts/run_mine_simulation.sh --validate
  ./scripts/run_mine_simulation.sh --headless
  ./scripts/run_mine_simulation.sh --iterations 100
  ./scripts/run_mine_simulation.sh --gui
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --headless)
            MODE="headless"
            shift
            ;;
        --gui)
            MODE="gui"
            shift
            ;;
        --validate)
            VALIDATE_ONLY=1
            shift
            ;;
        --iterations)
            ITERATIONS="$2"
            shift 2
            ;;
        --ros)
            USE_ROS2=1
            shift
            ;;
        -h|--help)
            print_usage
            exit 0
            ;;
        *)
            echo "Error: Unknown option '$1'" >&2
            print_usage >&2
            exit 1
            ;;
    esac
done

validate_sdf() {
    echo "=== Validating Subterranean Mine Simulation SDF Files ==="
    local failed=0

    echo "Checking world: ${WORLD_FILE}"
    if gz sdf -k "${WORLD_FILE}"; then
        echo "  [PASS] mine_world.sdf"
    else
        echo "  [FAIL] mine_world.sdf"
        failed=$((failed + 1))
    fi

    echo "Checking models in ${MODELS_DIR}..."
    for model_dir in "${MODELS_DIR}"/*; do
        if [ -d "${model_dir}" ] && [ -f "${model_dir}/model.sdf" ]; then
            model_name="$(basename "${model_dir}")"
            if gz sdf -k "${model_dir}/model.sdf" > /dev/null 2>&1; then
                echo "  [PASS] ${model_name}"
            else
                echo "  [FAIL] ${model_name}"
                failed=$((failed + 1))
            fi
        fi
    done

    if [ ${failed} -eq 0 ]; then
        echo "=== All SDF models and world validated successfully! ==="
        return 0
    else
        echo "=== Validation failed: ${failed} errors found ===" >&2
        return 1
    fi
}

if [ ${VALIDATE_ONLY} -eq 1 ]; then
    validate_sdf
    exit $?
fi

echo "=========================================================="
echo " Starting Subterranean Mine Simulation (Milestone M1)    "
echo " World: ${WORLD_FILE}                                     "
echo " Mode:  ${MODE}                                           "
echo "=========================================================="

if [ ${USE_ROS2} -eq 1 ]; then
    if [ -f "/opt/ros/humble/setup.bash" ]; then
        # shellcheck disable=SC1091
        source /opt/ros/humble/setup.bash
    fi
    exec ros2 launch "${REPO_ROOT}/launch/mine_simulation.launch.py" headless:=$([[ "${MODE}" == "headless" ]] && echo "true" || echo "false")
fi

CMD=(gz sim)
if [ "${MODE}" == "headless" ]; then
    CMD+=("-s")
fi
CMD+=("-r")

if [ -n "${ITERATIONS}" ]; then
    CMD+=("--iterations" "${ITERATIONS}")
fi

CMD+=("${WORLD_FILE}")

echo "Executing: ${CMD[*]}"
exec "${CMD[@]}"
