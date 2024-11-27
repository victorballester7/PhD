#!/bin/bash

# Define installation directory
INSTALL_DIR=$HOME/local
BIN_DIR=$INSTALL_DIR/bin
LIB_DIR=$INSTALL_DIR/lib
CONFIG_DIR=$HOME/.config/nvim
TMP_DIR=$HOME/tmp


LUA_VERSION=5.4.7

# Print a message (and wait for user confirmation) to make sure we are using the lastest verison of lua
echo "Please make sure that the latest version of Lua is $LUA_VERSION. To check that you can visit https://www.lua.org/download.html. Press Enter to continue... or Ctrl+C to exit if that's not the case."
read -r

# Create necessary directories
mkdir -p $INSTALL_DIR $BIN_DIR $LIB_DIR $CONFIG_DIR $TMP_DIR


# Function to download and build a package
build_and_install() {
    local name=$1
    local repo=$2
    local build_cmds=$3

    echo "Installing $name..."
    git clone --depth 1 $repo $name
    cd $name
    eval "$build_cmds"
    cd ..
    rm -rf $name
}

# Add install dir to PATH and other environment variables
export PATH=$BIN_DIR:$PATH
export LD_LIBRARY_PATH=$LIB_DIR:$LD_LIBRARY_PATH
export PKG_CONFIG_PATH=$LIB_DIR/pkgconfig:$PKG_CONFIG_PATH

# Update shell profile
echo "export PATH=$BIN_DIR:\$PATH" >> $HOME/.bashrc
echo "export LD_LIBRARY_PATH=$LIB_DIR:\$LD_LIBRARY_PATH" >> $HOME/.bashrc
echo "export PKG_CONFIG_PATH=$LIB_DIR/pkgconfig:\$PKG_CONFIG_PATH" >> $HOME/.bashrc

# Install packages
cd $TMP_DIR

# Install Rust (if not already installed)
if ! command -v cargo &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
    export PATH=$HOME/.cargo/bin:$PATH
    echo "export PATH=\$HOME/.cargo/bin:\$PATH" >> $HOME/.bashrc
fi

# Install lua (if not already installed)
if ! command -v lua &> /dev/null; then
    echo "Installing Lua..."
    curl -L -R -O https://www.lua.org/ftp/lua-${LUA_VERSION}.tar.gz
    tar zxf lua-${LUA_VERSION}.tar.gz
    cd lua-${LUA_VERSION}

    make linux MYCFLAGS="-I$INSTALL_DIR/include" MYLDFLAGS="-L$INSTALL_DIR/lib -Wl,-rpath,$INSTALL_DIR/lib"
    make INSTALL_TOP=$INSTALL_DIR install
fi

source $HOME/.bashrc

# 1. Bat
build_and_install "bat" "https://github.com/sharkdp/bat.git" \
    "cargo install --path . --root $INSTALL_DIR"

# 2. fswatch
build_and_install "fswatch" "https://github.com/emcrisostomo/fswatch.git" \
    "./autogen.sh && ./configure --prefix=$INSTALL_DIR && make && make install"

# 3. LuaRocks
build_and_install "luarocks" "https://github.com/luarocks/luarocks.git" \
    "./configure --prefix=$INSTALL_DIR && make && make install"

# 4. Neovim
build_and_install "neovim" "https://github.com/neovim/neovim.git" \
    "make CMAKE_BUILD_TYPE=Release CMAKE_INSTALL_PREFIX=$INSTALL_DIR && make install"

# 5. npm (via Node.js)
curl -fsSL https://nodejs.org/dist/latest/node-v$(curl -sL https://nodejs.org/dist/latest/ | grep -oP 'v\d+\.\d+\.\d+' | head -1)-linux-x64.tar.xz | tar -xJf -
mv node-v*-linux-x64 $INSTALL_DIR/node
ln -s $INSTALL_DIR/node/bin/npm $BIN_DIR/npm
ln -s $INSTALL_DIR/node/bin/node $BIN_DIR/node

# 6. Python pynvim
pip install --target=$LIB_DIR pynvim

# 7. Ripgrep
build_and_install "ripgrep" "https://github.com/BurntSushi/ripgrep.git" \
    "cargo build --release && cp target/release/rg $BIN_DIR"

# 8. Tree-sitter
build_and_install "tree-sitter" "https://github.com/tree-sitter/tree-sitter.git" \
    "cargo build --release && cp target/release/tree-sitter $BIN_DIR"

# 9. Tree-sitter CLI
npm install -g tree-sitter-cli


cd
rm -rf $TMP_DIR
