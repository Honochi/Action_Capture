# Action_Capture
# 鼠标键盘动作录制回放系统

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📖 项目概述

本工具是一个基于Python开发的桌面自动化解决方案，能够完整记录用户的鼠标和键盘操作，并支持精准回放。适用于自动化测试、重复操作批处理、游戏脚本录制等多种场景。

## ✨ 核心功能

- **全操作录制**
  - 🖱️ 精确捕捉鼠标移动轨迹
  - 🎯 记录所有点击（左/中/右键）和滚轮操作
  - ⌨️ 完整记录键盘输入与特殊按键（含组合键）
  
- **智能回放系统**
  - ⏱️ 毫秒级时间精度回放
  - 🔄 支持多线程异步执行
  - 📁 JSON格式存储操作序列

- **便捷命令行界面**
  - 📝 支持命令自动补全（Tab键）
  - 🔍 内置录制文件管理
  - 📚 交互式帮助系统

## 🛠️ 技术栈

- **事件捕获**: `pynput`
- **命令行界面**: `cmd`
- **时间控制**: `time` 模块
- **数据存储**: JSON 序列化
- **异步处理**: 多线程技术

## 📦 安装指南

### 前置需求
- Python 3.7+
- pip 包管理工具

```bash
# 安装依赖库
pip install pynput
