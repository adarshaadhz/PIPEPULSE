PIPEPULSE — System Architecture

1. System Overview

PIPEPULSE is designed as an experimental two-sensor acoustic monitoring system for water pipelines.

Its purpose is to capture pipe vibrations, analyse the recorded signals and investigate whether leak conditions can be identified.

2. Proposed Architecture

The system has five main stages:

1. Sensor A: Captures vibration signals at the first measurement point.
2. Sensor B: Captures vibration signals at the second measurement point.
3. Data Acquisition: Records both sensor signals simultaneously using a synchronized two-channel interface.
4. Signal Processing: A computer running Python filters and analyses the recorded signals.
5. Detection Output: The software estimates whether the recorded conditions indicate a possible leak.

3. Proposed Hardware

Component	Purpose
Two piezoelectric contact sensors	Capture pipe vibrations
Two-channel audio interface	Record synchronized signals
Preamplifier	Improve sensor signal levels
PVC pipe and fittings	Experimental pipeline
Low-voltage water pump	Circulate water
Valves	Control flow and simulate leaks
Computer	Process and analyse data

These components are proposed and have not yet been assembled.

4. Software Architecture

Python will initially be used for:

• Signal filtering
• RMS and frequency analysis
• Feature extraction
• Cross-correlation
• Machine-learning experiments
• Performance evaluation

5. Experimental Setup

A controlled water pipeline will be constructed using PVC pipe, a reservoir, a low-voltage pump and adjustable valves.

Two sensors will be attached at known positions.

Experiments will compare:

• Normal water flow
• Controlled leak conditions
• Different flow rates
• Different background noise levels

6. Future Development

If the initial experiments are successful, an ESP32-S3-based edge-processing prototype may be investigated.

7. Current Status

This document describes a proposed architecture. Hardware assembly, signal acquisition and experimental validation are still pending.