# UGPCL

![Language](https://img.shields.io/badge/language-UGPCL-blue)
![Status](https://img.shields.io/badge/status-alpha-orange)
![Runtime](https://img.shields.io/badge/runtime-UGPCI-purple)
![Packages](https://img.shields.io/badge/packages-UGPIP-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

UGPCL (Universal General Purpose Configuration Language) is a minimal interpreted configuration and scripting language designed for simplicity, extensibility, and modular execution.

It is powered by UGPCI (the interpreter) and extended through UGPIP (package import system) using .ugcm modules.

---

# Overview

UGPCL is built around three core ideas:

- Minimal core syntax
- Section-based execution model
- Extensible runtime through modules

It is not intended to be a full general-purpose programming language. Instead, it focuses on predictable structure and modular expansion.

---

# File Types

- .ugcpl → program files  
- .ugcm → modules (UGPIP packages)

---

# Execution Model

UGPCL programs are divided into numbered sections.

Example:

1'2

Section 1 is configuration  
Section 2 is execution order  

---

# Syntax

General format:

section,line:command,arg1,arg2,...

Example:

1'2

1,1:set,mode,normal  
1,2:import,extra  

2,1:print,str,Hello World  
!;

---

# Core Commands

## set

Sets runtime variables.

Format:
set,key,value

Example:
1,1:set,mode,debug

---

## import

Loads modules using UGPIP.

Formats:
import,module  
import,github:user/repo/module.ugcm@version  

Example:
1,2:import,extra  

---

# UGPIP (Package System)

UGPCL uses UGPIP to load external functionality through .ugcm modules.

## Module Sources

Built-in modules:
import,extra  
import,graphic  
import,debug  

GitHub modules:
import,github:user/repo/module.ugcm@1.0.0  

Modules are:
- downloaded on first use
- cached locally
- registered into runtime

---

# Official Modules

## extra.ugcm
Provides basic runtime utilities:
- print
- state utilities
- helper functions

---

## graphic.ugcm
Provides visual output capabilities:
- text rendering
- screen control
- future drawing primitives

---

## debug.ugcm
Provides debugging tools:
- state inspection
- execution tracing
- error reporting

---

# Execution Rules

- Section 1 always executes first
- Modules must be imported before use
- Execution follows section order defined in header
- Unknown commands cause runtime errors

---

# Examples

## Hello World

1'2

1,1:import,extra  

2,1:print,str,Hello World  
!;

---

## Debug Example

1'2

1,1:import,extra  
1,2:import,debug  
1,3:set,mode,debug  

2,1:dump,state  
!;

---

## Multi-module Example

1'2

1,1:import,extra  
1,2:import,graphic  

2,1:print,str,Modules loaded  
!;

---

# Philosophy

UGPCL is:

- minimal  
- modular  
- deterministic  
- extensible through UGPIP  

It avoids unnecessary complexity and focuses on predictable execution.

---

# Project Structure

ugpci/
  ugpci/        interpreter core
  modules/      official UGCM modules
  examples/     sample programs
  cache/        downloaded packages

---

# Status

UGPCL is in early alpha.  
Interpreter, module system, and language specification are actively evolving.