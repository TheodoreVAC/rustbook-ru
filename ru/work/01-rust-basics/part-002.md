## 1.2 Install Rust and its Toolchain

Ubuntu 22.04 and later versions come with pre-installed Rust, so you can start using it right away. If you’re using other Unix-like systems, use the command below to install Rust. For Windows, refer to the official website. As the code in this book is written in Linux, we recommend readers use Linux or Mac OS to avoid any inconsistencies and errors caused by different environments.

```bash
$ curl --proto '=https' --tlsv1.2 \
    -sSf https://sh.rustup.rs | sh
```

After installing Rust on Linux, you need to set environment variables to enable the system to locate Rust tools like the rustc compiler. Add the following three lines to the end of ~/.bashrc.

```bash
# Rust env-path variables
export RUSTPATH=$HOME/.cargo/bin
export PATH=$PATH:$RUSTPATH
```

Then, save and execute source ~/.bashrc. If you find this process cumbersome, you can download the install_rust.sh script from the first chapter of the source code of this book and run it to complete the Rust toolchain installation. The instructions above will install the rustup tool, which manages and installs the Rust toolchain, including the rustc compiler, cargo project management tool, rustup toolchain management tool, rustdoc documentation tool, rustfmt formatting tool, and rust-gdb debugging tool. For simple projects, you can use the rustc compiler for compilation. However, for larger projects, you need the cargo tool for management, which internally calls rustc for compilation. Cargo is an excellent tool that handles project building, testing, compilation, and publishing, making it highly efficient. Programmers who have worked with C/C++ projects will appreciate the cargo tool’s greatness in handling various libraries and dependencies. Most of the time, we use the rustc compiler instead of the cargo tool, as the projects in this book are not too complex. Rustup manages the installation, upgrade, and uninstallation of Rust tools. Note that the Rust language includes stable and nightly versions, both of which can coexist. You can install Nightly using the following command.

```bash
$ rustup default nightly
```

After installation, you can use rustup to check the current version in use.

```bash
$ rustup toolchain list
    stable-x86_64-unknown-linux-gnu
    nightly-x86_64-unknown-linux-gnu (default)
```

To switch between stable and nightly versions, please use the following command.

```bash
$ rustup default stable # nightly
```
