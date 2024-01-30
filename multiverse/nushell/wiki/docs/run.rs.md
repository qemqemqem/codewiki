# run.rs

File: [run.rs](/home/keenan/Dev/nushell/src/run.rs)

Num lines: 292

Github history: TODO




`run.rs` is a Rust source file that is part of a larger project, which appears to be a shell or command-line interface (CLI) application, possibly related to the [Nushell](Nushell.md) project. This file contains the core runtime functions that handle the execution of commands, scripts, and the Read-Eval-Print Loop (REPL) within the shell environment. The code is structured to support conditional compilation with features such as "plugin", which suggests a modular design that can be tailored for different build configurations.

## Overview

The `run.rs` file defines three primary public functions:

- `run_commands`: Executes a series of commands within the shell.
- `run_file`: Executes a script file with arguments.
- `run_repl`: Initializes and runs the REPL loop.

These functions are designed to be used by the main entry point of the application, which is typically defined in a file like [main.rs](main.rs.md).

## Functionality

### run_commands

The `run_commands` function takes in several parameters, including the mutable `engine_state`, which likely holds the state of the shell, `parsed_nu_cli_args` for command-line arguments, a boolean `use_color` for ANSI color output, `commands` as a string of commands to execute, and `input` as the initial data to be processed.

The function starts by setting up a new stack and then proceeds to conditionally load plugin, environment, and configuration files based on the provided CLI arguments. It uses the `perf` utility function to log performance metrics, which is a common practice in performance-sensitive applications like shells.

After the setup, it sets the startup time in the `engine_state`, updates the `$nu` constant with the startup time, and evaluates the commands using the `evaluate_commands` function from the `nu_cli` crate. The function concludes by handling the exit code of the commands.

### run_file

The `run_file` function is similar to `run_commands` but is specifically designed to execute a script file. It takes additional parameters for the script name and arguments to pass to the script. The function follows a similar pattern of loading plugins and configuration files, updating the `$nu` constant, and evaluating the script file using the `evaluate_file` function.

### run_repl

The `run_repl` function is responsible for initializing and running the REPL loop. It performs configuration setup and then calls `evaluate_repl` to start the interactive loop. The function also takes care of loading the necessary configuration files and setting up the environment for the REPL.

## Configuration and Environment

The file makes use of several configuration-related functions from the `config_files` module, such as `setup_config`, `read_config_file`, and `read_default_env_file`. These functions are critical for setting up the shell environment according to user preferences and system defaults.

## Error Handling

All three functions return a `Result` type, indicating that they can potentially fail with an error. The errors are wrapped in `miette::ErrReport`, which is a library for diagnostic error reporting in Rust applications.

## Integration with Other Components

The `run.rs` file integrates with various components of the application:

- `nu_protocol`: Provides types and functions related to the shell's protocol, such as `PipelineData` and `Span`.
- `nu_cli`: Contains the logic for evaluating commands and files, as well as running the REPL.
- `nu_utils`: A utility module, likely containing common helper functions like `perf`.

## Conclusion

The `run.rs` file is a central part of the shell's runtime system, handling the execution of commands, scripts, and the REPL. It demonstrates a clear separation of concerns, robust error handling, and performance logging. Understanding this file is crucial for contributors to effectively work on the project's command execution and scripting capabilities.

For further details on specific components or concepts mentioned in this file, refer to related articles such as [Cargo](Cargo.md), [Cargo.toml](Cargo.toml.md), [Logging](Logging.md), [Rust](Rust.md), [Semantic Versioning](Semantic%20Versioning.md), [TOML](TOML.md), [crates.io](crates.io.md), and [nu_protocol::ShellError](nu_protocol::ShellError.md).