# UGPCL

UGPCL (Universal General Purpose Configuration Language) is a minimal interpreted configuration and scripting language designed for simplicity, extensibility, and modular execution.

It is powered by UGPCI (the interpreter) and extended through UGPIP (module import system) using .ugcm packages.

---

# Overview

UGPCL is built around three core ideas:

- Minimal core language
- Section-based execution model
- Extensible runtime via modules

It is not designed to be a full general-purpose programming language. It focuses on predictable structure and modular extension.

---

# File Types

- .ugcpl → program files
- .ugcm → modules

---

# Execution Model

Programs are divided into sections.

Example:
1'2

- Section 1 = configuration
- Section 2 = execution order

---

# Syntax

Format:
section,line:command,arg1,arg2,...

Example:
1'2

1,1:set,mode,normal
1,2:import,extra

2,1:print,str,Hello World
!;

---

# Core Commands

set:
set,key,value

import:
import,module
import,github:user/repo/file.ugcm@version

---

# UGPIP Module System

Modules extend functionality.

Built-in:
import,extra
import,graphic
import,debug

GitHub:
import,github:user/repo/module.ugcm@1.0.0

Modules are:
- downloaded
- cached
- registered into runtime

---

# Official Modules

extra:
- print
- dump
- helpers

graphic:
- text output
- rendering primitives (planned)

debug:
- state inspection
- tracing
- error reporting

---

# Execution Rules

- Section 1 runs first
- Modules must be imported before use
- Execution follows section order
- Unknown commands cause runtime error

---

# Example Programs

Hello World:
1'2

1,1:import,extra
2,1:print,str,Hello World
!;

Debug:
1'2

1,1:import,extra
1,2:import,debug
1,3:set,mode,debug

2,1:dump,state
!;

---

# Philosophy

UGPCL is:
- minimal
- modular
- deterministic
- extensible

---

# Project Structure

ugpci/
  ugpci/
  modules/
  examples/
  cache/

---

# Future Ideas

- chaining
- loops
- dependency resolution
- lockfiles
- sandboxing

---

# Status

Early development. Language, interpreter, and module system are evolving.