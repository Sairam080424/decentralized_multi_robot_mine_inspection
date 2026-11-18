# Coding Standards & Guidelines

## 1. C++ Standards
- **Standard**: C++17 minimum; C++20 allowed for modern concurrency and concepts.
- **Style Guide**: ROS 2 C++ Style Guide / Google C++ Style Guide.
- **Formatter**: `clang-format` using `.clang-format` configuration.
- **Rules**:
  - Use smart pointers (`std::unique_ptr`, `std::shared_ptr`) exclusively; zero manual `new`/`delete`.
  - Always use `const` references for non-primitive inputs.
  - All public classes and functions must include Doxygen comments (`/** ... */`).

## 2. Python Standards
- **Standard**: Python 3.10+.
- **Style Guide**: PEP 8 compliance enforced via `flake8` and `black`.
- **Typing**: 100% static type annotations validated with `mypy`.
- **Docstrings**: Google-style docstrings for all modules, classes, and functions.

## 3. ROS 2 Package Conventions
- Every package must include `package.xml` (Format 3) and `CMakeLists.txt` or `setup.py`.
- Separate interfaces into dedicated interface packages without node source code.
- Node implementations should use ROS 2 Composition (`rclcpp_components`) for zero-copy intra-process transport.
