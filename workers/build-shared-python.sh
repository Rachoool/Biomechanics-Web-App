#!/usr/bin/env bash
set -o errexit
set -o nounset

echo ">>>>> START building shared Python 3.10..."

# 安装必要工具和依赖
echo ">>>>> Installing system packages..."
apt update
apt install --yes software-properties-common vim git wget curl lsb-release gnupg

# 启用源码源（为 build-dep 提供支持）
echo ">>>>> Enabling deb-src entries..."
grep -q '^deb-src' /etc/apt/sources.list || {
  sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list
}
apt update

# 安装 Python 编译依赖
echo ">>>>> Installing build dependencies..."
apt-get build-dep --yes python3

# 安装额外依赖
apt install --yes \
  build-essential gdb lcov pkg-config \
  libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
  libncurses5-dev libreadline-dev libsqlite3-dev libssl-dev \
  zlib1g-dev uuid-dev tk-dev libmpdec-dev libzstd-dev

# 下载并构建 Python 源码
cd /workspace/
PYTHON_VERSION="3.10.18"
PYTHON_DIR="Python-${PYTHON_VERSION}"

echo ">>>>> Downloading Python ${PYTHON_VERSION}..."
wget https://www.python.org/ftp/python/${PYTHON_VERSION}/${PYTHON_DIR}.tar.xz
tar -xf ${PYTHON_DIR}.tar.xz
cd ${PYTHON_DIR}

echo ">>>>> Configuring Python build..."
mkdir -p ./MyPython/
./configure --prefix="${PWD}/MyPython/" \
            --enable-shared \
            --enable-optimizations \
            --with-lto

echo ">>>>> Building Python (this may take a few minutes)..."
make -s -j "$(nproc)"
make altinstall

# 设置 Python 环境变量（后续用）
export LD_LIBRARY_PATH="${PWD}:${LD_LIBRARY_PATH}"

# 检查是否成功
echo ">>>>> Python build complete:"
./python --version
./python -m pip --version

echo ">>>>> DONE build-shared-python.sh"
