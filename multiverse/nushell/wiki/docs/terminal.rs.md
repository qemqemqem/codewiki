# terminal.rs

File: [terminal.rs](/home/keenan/Dev/nushell/src/terminal.rs)

Num lines: 149

Github history: TODO




The `terminal.rs` module is a critical component of the [Nushell](Nushell.md) project, which is a modern shell written in the [Rust](Rust.md) programming language. This module is responsible for handling terminal interactions, particularly when Nushell operates in interactive mode. It ensures that the shell can properly manage terminal control, signal handling, and process group management.

## Overview

The `terminal.rs` file contains Rust code that interfaces with low-level system functionalities, primarily through the `nix` crate, which provides Unix-specific APIs. It includes functions for acquiring and relinquishing control of the terminal, setting up signal handlers, and restoring the terminal state upon exit.

## Key Components

### Global Variables

- `INITIAL_PGID`: A static `AtomicI32` variable that stores the initial process group ID (PGID) when Nushell takes control of the terminal. This value is used to restore the terminal's state upon the shell's exit.

### Functions

#### `acquire(interactive: bool)`

This function is called to acquire control of the terminal when Nushell is running in interactive mode. It performs several checks and operations:

1. Registers `restore_terminal` as an exit function using `libc::atexit`.
2. Calls `take_control` to attempt to take control of the terminal and store the initial PGID.
3. Sets up signal handlers to ignore certain signals (`SIGQUIT`, `SIGTSTP`, `SIGTTIN`, `SIGTTOU`) and to handle `SIGTERM` with a custom handler.
4. Ensures that Nushell runs in its own process group and takes control of the terminal if necessary.

#### `take_control() -> Pid`

This function attempts to take control of the terminal and returns the original PGID. It performs the following actions:

1. Resets all signal handlers to their default actions.
2. Attempts to take control of the terminal by setting the process group of the terminal to Nushell's process group.
3. Handles cases where the terminal is not owned or when the shell is running under conditions like `sudo`.
4. If unable to take control after several attempts, it exits the process, indicating that the shell might be orphaned.

#### `restore_terminal()`

An `extern "C"` function that is registered to be called upon exit. It restores the terminal's process group to the initial PGID if it has been changed.

#### `sigterm_handler(_signum: libc::c_int)`

Another `extern "C"` function that acts as a custom signal handler for `SIGTERM`. It restores the terminal and then re-raises the `SIGTERM` signal with the default action to ensure proper termination of the process.

## Signal Handling

The `terminal.rs` module sets up custom signal handling to ensure that Nushell can manage its own terminal state and respond to signals in a controlled manner. The use of `sigaction` allows for the specification of signal handlers and flags for different signals.

## Process Group Management

The module contains logic to manage process groups, which is essential for a shell that can run jobs in the foreground and background. It uses `unistd::setpgid` and `unistd::tcsetpgrp` to manipulate the process group of Nushell and the terminal, respectively.

## Error Handling

Throughout the `terminal.rs` module, error handling is performed using `eprintln!` for printing error messages and `std::process::exit(1)` for terminating the process in case of critical failures.

## Conclusion

The `terminal.rs` module is a foundational part of the Nushell project, providing the necessary functionalities for terminal control and signal management. Understanding this module is crucial for developers working on Nushell, especially when dealing with interactive features and process control.

For further information on related topics, developers may refer to articles such as [main.rs](main.rs.md), [run.rs](run.rs.md), and [nu_protocol::ShellError](nu_protocol::ShellError.md). Additionally, understanding the [Rust](Rust.md) programming language and the [nix](nix.md) crate will be beneficial for contributing to this module.