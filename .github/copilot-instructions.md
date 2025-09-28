# Copilot Instructions for Staubli Experimental (ROS-Industrial)

## Project Overview
This repository contains experimental ROS packages for Staubli industrial manipulators. Packages here are tested and migrated to the main `staubli` repo after stabilization. APIs and contents are subject to change and may be incomplete or unstable.

## Architecture & Key Components
- **Package Structure:**
  - Each Staubli robot family (e.g., `staubli_tx2_60_support`, `staubli_tx90_support`) has its own package directory.
  - The main code for experimental features is in `staubli_experimental/`.
- **Driver Integration:**
  - The `staubli_val3_driver` is now maintained separately ([see repo](https://github.com/ros-industrial/staubli_val3_driver)).
- **Migration Policy:**
  - Packages are migrated to the main repo after sufficient testing. Expect frequent changes and unstable APIs.

## Build & Test Workflows
- **ROS Workspace:**
  - Standard ROS Catkin workspace layout: source code in `src/`, build outputs in `build/`, install in `install/`.
- **Build Tools:**
  - Use `catkin_tools` (`catkin build`) for building. `catkin_make` is also supported but not recommended.
  - Example build:
    ```bash
    cd ~/ros2_ws_robots
    rosdep update
    rosdep install --from-paths src/ --ignore-src --rosdistro <distro>
    catkin build
    source install/setup.bash
    ```
- **CI/CD:**
  - GitHub Actions workflows in `.github/workflows/` use `industrial_ci` for ROS Melodic/Noetic builds.
  - Ccache is used for build acceleration.
  - Upstream workspace is set to `ros-industrial/staubli#indigo-devel` for dependency resolution.

## Conventions & Patterns
- **Branching:**
  - Branches named `<ros-distro>-devel` (e.g., `kinetic-devel`). Releases are made from distribution branches.
- **Support Level:**
  - Community-supported; APIs may change without notice.
- **Licensing:**
  - Apache 2.0 license.

## Integration Points
- **External Dependencies:**
  - Relies on ROS core packages and `industrial_ci` for CI.
  - See `rosdep install` for required dependencies.
- **Testing:**
  - No explicit test directory; tests are run via CI workflows using `industrial_ci`.

## Examples & References
- See `README.md` in root and `staubli_experimental/` for package details and build instructions.
- For driver integration, refer to the external `staubli_val3_driver` repo.

## Quickstart for AI Agents
- Always use `catkin build` unless legacy compatibility is required.
- Source `install/setup.bash` after building to update environment.
- Check `.github/workflows/` for CI patterns and environment variables.
- Expect frequent changes; verify API stability before relying on features.

---
For questions or unclear conventions, consult the ROS wiki: http://wiki.ros.org/staubli_experimental or ask maintainers via GitHub Issues.
