cmake_minimum_required(VERSION 3.15)
project(factor_core LANGUAGES CXX)

# -----------------------------
# 设置 C++ 标准
# -----------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# -----------------------------
# 检查 pybind11 是否存在
# -----------------------------
set(pybind11_SOURCE_DIR "${CMAKE_SOURCE_DIR}/deps/pybind11-2.12.0" CACHE PATH "Path to pybind11 source")
if(NOT EXISTS ${pybind11_SOURCE_DIR})
    message(FATAL_ERROR "pybind11 not found at ${pybind11_SOURCE_DIR}. Please download it to deps/")
endif()

# -----------------------------
# 配置 pybind11（使用本地源码）
# -----------------------------
set(pybind11_BUILD_EXAMPLES OFF CACHE BOOL "Build pybind11 examples")
set(pybind11_INSTALL OFF CACHE BOOL "Enable installation of pybind11")

add_subdirectory(
    ${pybind11_SOURCE_DIR}
    ${CMAKE_BINARY_DIR}/_deps/pybind11-build
    EXCLUDE_FROM_ALL
)

# -----------------------------
# 定义 Python 扩展模块
# -----------------------------
pybind11_add_module(factor_core
    src/compute_factors.cpp  # ✅ 确保路径正确
)

# -----------------------------
# ✅ 正确：强制输出到当前目录，避免 build/Release/ 下
# -----------------------------
set_target_properties(factor_core PROPERTIES
    PREFIX ""                    # 去掉 lib 前缀
    OUTPUT_NAME "factor_core"    # 强制文件名
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}    # 输出到 cpp_core/ 目录
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}    # 对 .pyd 有效
)