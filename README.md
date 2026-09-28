# genpark-csp-channel-multiplexing-pipeline-skill

Agent Skill implementing **Communicating Sequential Processes (CSP)** Go-style buffered/unbuffered channels with nonblocking `select` multiplexing.

## Architectural Overview
```mermaid
flowchart LR
    ProducerA["Producer A"] --> ChannelA["Channel A (Buffered)"]
    ProducerB["Producer B"] --> ChannelB["Channel B (Buffered)"]
    ChannelA & ChannelB --> Select["Nonblocking CSP Select Multiplexer"]
    Select --> Consumer["Consumer Pipeline Processor"]
```
